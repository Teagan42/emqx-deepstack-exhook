import json
import logging
import io
from PIL import Image
from typing import Any, Dict, Optional
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
    known_topics: Dict[str, CPAITopic]

    def __init__(
        self, config: Config, session: Optional[aiohttp.ClientSession] = None
    ) -> None:
        self.known_topics: Dict[str, CPAITopic] = {}
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
                value.subscribe,
                [
                    self.pipelines[pipeline]
                    for pipeline in value.pipelines
                    if pipeline in self.pipelines
                ],
            )
            for value in config.topics
        ]

    def find_topic(self, topic: str) -> Optional[CPAITopic]:
        cpai_topic = self.known_topics.get(topic, None)
        if cpai_topic is not None:
            return cpai_topic
        for t in self.topics:
            if t.matches_subscription(topic):
                self.known_topics[topic] = t
                return t

        return None

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
            return image_bytes.getvalue()

    async def process_message(
        self, topic: str, message: Message
    ) -> Optional[Dict[str, Any]]:
        cpai_topic = self.find_topic(topic)
        if cpai_topic is None:
            self._logger.warn("Unable to match topic to pipeline: %s", topic)
            return None
        self._logger.info(
            f"Using topic {topic} match: {cpai_topic.subscribe} regex: {cpai_topic.topic_pattern}"
        )
        before_after = json.loads(message.payload)
        if before_after.get("after", None) is None:
            return None
        event = FrigateEvent(**before_after["after"])
        try:
            snapshot = await self.get_snapshot(event)
            event = await cpai_topic.process_event(self._session, event, snapshot)

            before_after["after"] = event.__dict__
            return before_after
        except Exception as exc:
            self._logger.error(
                "Error processing message on %s: %s" % (topic, str(exc)), exc_info=exc
            )
            return None
