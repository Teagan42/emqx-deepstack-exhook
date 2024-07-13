import json
import logging
import io
from PIL import Image
from typing import Any, Dict, List, Optional
import jq

import aiohttp
from emqx_deepstack_exhook.config import Config
from emqx_deepstack_exhook.config.const import ATTR_FRIGATE
from emqx_deepstack_exhook.cpai.types import (
    CPAIPipeline,
    CPAIServer,
    CPAITopic,
    FrigateEvent,
)
from emqx_deepstack_exhook.pb2.exhook_pb2 import Message


class CPAIProcess:

    def __init__(
        self, config: Config, session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        self._logger = logging.getLogger(CPAIProcess.__name__)
        self._session = session or aiohttp.ClientSession()
        self.frigate = config.frigate
        self.servers = {
            key: CPAIServer(key, value.host, value.port)
            for key, value in config.servers.items()
        }
        invalid_pipelines = [
            key
            for key, value in config.pipelines.items()
            if value.server not in self.servers
        ]
        if len(invalid_pipelines) > 0:
            self._logger.error(
                "Invalid pipeline configurations, server not present in list: %s",
                json.dumps(invalid_pipelines),
            )
            raise Exception(
                "Invalid pipeline configurations, server not present in list: %s"
                % json.dumps(invalid_pipelines)
            )
        self.pipelines = {
            key: CPAIPipeline(
                key,
                pipeline_type=value.pipeline_type,
                server=self.servers[value.server],
                model=value.model,
                threshold=value.threshold,
                result_topic=value.result_topic,
                filter=jq.compile(value.filter),
                frigate=self.frigate,
            )
            for key, value in config.pipelines.items()
            if value.server in self.servers
        }
        invalid_topics = [
            value.subscribe
            for value in config.topics
            if len(
                [
                    pipeline
                    for pipeline in value.pipelines
                    if pipeline not in self.pipelines
                ]
            )
        ]
        if len(invalid_topics) > 0:
            self._logger.error(
                "Invalid topic configurations, pipeline not present in list: %s",
                json.dumps(invalid_topics),
            )
            raise Exception(
                "Invalid topic configurations, pipeline not present in list: %s"
                % json.dumps(invalid_topics)
            )
        self.topics = [
            CPAITopic(
                subscribe=value.subscribe,
                filter=jq.compile(value.filter) if value.filter is not None else None,
                pipelines=[
                    self.pipelines[pipeline]
                    for pipeline in value.pipelines
                    if pipeline in self.pipelines
                ],
            )
            for value in config.topics
        ]

    def find_topics(self, topic: str) -> List[CPAITopic]:
        matching_topics: List[CPAITopic] = []
        for t in self.topics:
            if t.matches_subscription(topic):
                matching_topics.append(t)

        return matching_topics

    async def get_snapshot(self, event: FrigateEvent) -> bytes:
        self._logger.debug("Getting snapshot...")
        async with self._session.get(
            f"{self.frigate}/api/events/{event.id}/snapshot.jpg?crop=0"
        ) as resp:
            img_bytes = await resp.read()
            img = Image.open(io.BytesIO(img_bytes))
            width, height = img.size
            image_bytes = io.BytesIO()
            img.save(image_bytes, format="JPEG")
            self._logger.debug(f"{width, height}")
            return image_bytes.getvalue()

    async def process_message(
        self, topic: str, message: Message
    ) -> Optional[Dict[str, Any]]:
        before_after = json.loads(message.payload)
        if (
            before_after is None
            or not isinstance(before_after, dict)
            or before_after.get("after", None) is None
        ):
            return None
        event = FrigateEvent(**before_after["after"])
        self._logger.debug(
            [
                {
                    "topic": t,
                    "event": {"id": event.id, "label": event.label},
                    "filter": t.filter,
                    "filterResult": t.filter is not None
                    and t.filter.input_value(event.__dict__).first(),
                }
                for t in self.topics
            ]
        )
        cpai_topics = [
            t
            for t in self.find_topics(topic)
            if t.filter is None or t.filter.input_value(event.__dict__).first()
        ]
        if len(cpai_topics) == 0:
            return None

        snapshot = await self.get_snapshot(event)
        for cpai_topic in cpai_topics:
            self._logger.info(
                f"Using topic {topic} match: {cpai_topic.subscribe} regex: {cpai_topic.topic_pattern}"
            )

            try:
                event, success = await cpai_topic.process_event(
                    self._session, event, snapshot
                )
                if not success:
                    continue
            except Exception as exc:
                self._logger.error(
                    "Error processing message on %s: %s" % (topic, str(exc)),
                    exc_info=exc,
                )
                continue
        before_after["after"] = event.__dict__
        return before_after
