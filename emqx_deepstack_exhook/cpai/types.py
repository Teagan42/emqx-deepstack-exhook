import asyncio
import json
import logging
import concurrent.futures
from codeprojectai.core import process_image, get_stored_faces, CodeProjectAIObject
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import re
import jq
from jq import _Program


import aiohttp

from emqx_deepstack_exhook.config.const import (
    PIPELINE_FACE_DETECT,
    PIPELINE_FACE_RECOGNIZE,
    PIPELINE_OBJECT,
    PIPELINE_VISION,
)
from emqx_deepstack_exhook.pb2.exhook_pb2 import Message

URL_BASE_VISION = "http://{ip}:{port}/v1/vision"
URL_CUSTOM = "/custom/{custom_model}"
URL_OBJECT_DETECTION = "/detection"
URL_FACE_DETECTION = "/face"
URL_FACE_REGISTER = "/face/register"
URL_FACE_RECOGNIZE = "/face/recognize"
URL_FACE_LIST = "/face/list"
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_IP = "localhost"
DEFAULT_PORT = 32168
DEFAULT_MIN_CONFIDENCE = 0.45

## HTTP codes
HTTP_OK = 200
BAD_URL = 404


def apply_anchors(pattern: str) -> str:
    return f"^{pattern}$"


class InferenceError(Exception):
    def __init__(self, *args: object, inferences: List["CPAIInference"]) -> None:
        super().__init__(*args)
        self.inferences = inferences


class CodeProjectAIException(Exception):
    pass


class CodeProjectAIFace:
    """Work with objects"""

    def __init__(
        self,
        ip: str = DEFAULT_IP,
        port: int = DEFAULT_PORT,
        timeout: int = DEFAULT_TIMEOUT,
        min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    ):
        self.port = port
        self.timeout = timeout
        self.min_confidence = min_confidence

        self._url_base = URL_BASE_VISION.format(ip=ip, port=port)
        self._url_detect = self._url_base + URL_FACE_DETECTION
        self._url_recognize = self._url_base + URL_FACE_RECOGNIZE
        self._url_register = self._url_base + URL_FACE_REGISTER
        self._url_face_list = self._url_base + URL_FACE_LIST

    def detect(self, image_bytes: bytes):
        """Process image_bytes and detect."""
        response = process_image(
            url=self._url_detect,
            image_bytes=image_bytes,
            min_confidence=self.min_confidence,
            timeout=self.timeout,
        )
        return response["predictions"]

    def register(self, name: str, image_bytes: bytes):
        """
        Register a face name to a file.
        """
        response = process_image(
            url=self._url_register,
            image_bytes=image_bytes,
            min_confidence=self.min_confidence,
            timeout=self.timeout,
            data={"userid": name},
        )

        if response["success"] == True:
            return response["message"]

        elif response["success"] == False:
            error = response["error"]
            raise CodeProjectAIException(
                f"CodeProject.AI Server raised an error registering a face: {error}"
            )

    def recognize(self, image_bytes: bytes):
        """Process image_bytes, performing recognition."""
        response = process_image(
            url=self._url_recognize,
            image_bytes=image_bytes,
            min_confidence=self.min_confidence,
            timeout=self.timeout,
        )

        return response["predictions"]

    def get_registered_faces(self):
        """Get the name of the registered faces"""
        response = get_stored_faces(url=self._url_face_list, timeout=self.timeout)
        return response["faces"]  # type: ignore


@dataclass
class FrigateEvent:
    id: str = field(init=True)
    camera: str = field(init=True)
    frame_time: Optional[float] = field(default=None, init=True)
    snapshot_time: Optional[float] = field(default=None, init=True)
    snapshot: Optional[Dict[str, Any]] = field(default_factory=lambda: {}, init=True)
    label: Optional[str] = field(default=None, init=True)
    sub_label: Optional[Tuple[str, float]] = field(default=None, init=True)
    top_score: Optional[float] = field(default=None, init=True)
    false_positive: bool = field(default=False, init=True)
    start_time: float = field(default=0, init=True)
    end_time: Optional[float] = field(default=None, init=True)
    score: Optional[float] = field(default=None, init=True)
    box: Optional[List[int]] = field(default=None, init=True)
    area: Optional[int] = field(default=None, init=True)
    ratio: Optional[float] = field(default=None, init=True)
    region: Optional[List[int]] = field(default=None, init=True)
    current_zones: Optional[List[str]] = field(default=None, init=True)
    entered_zones: Optional[List[str]] = field(default=None, init=True)
    thumbnail: Any | None = field(default=None, init=True)
    has_snapshot: bool = field(default=False, init=True)
    has_clip: bool = field(default=False, init=True)
    stationary: Optional[bool] = field(default=None, init=True)
    motionless_count: Optional[int] = field(default=None, init=True)
    position_changes: Optional[int] = field(default=None, init=True)
    attributes: Dict[str, float] = field(default_factory=lambda: {}, init=True)
    current_attributes: List[Dict[str, Any]] = field(
        default_factory=lambda: [],
        init=True,
    )


@dataclass
class CPAIPrediction:
    confidence: float
    label: str
    x_min: int
    y_min: int
    x_max: int
    y_max: int


@dataclass
class CPAIInference:
    predictions: List[CPAIPrediction] = field(init=True)

    @classmethod
    def parse(cls, resp: Dict[str, Any], label="") -> "CPAIInference":
        return CPAIInference(
            predictions=[
                CPAIPrediction(
                    confidence=prediction["confidence"],
                    label=(
                        label
                        if prediction.get("label", None) is None
                        else prediction.get("label", None)
                    ),
                    y_min=prediction["y_min"],
                    x_min=prediction["x_min"],
                    y_max=prediction["y_max"],
                    x_max=prediction["x_max"],
                )
                for prediction in resp.get("predictions", [])
            ],
        )


@dataclass
class CPAIServer:
    name: str
    host: str
    port: int


@dataclass
class CPAIPipeline:
    name: str
    pipeline_type: str
    server: CPAIServer
    frigate: str
    model: Optional[str]
    threshold: float
    result_topic: Optional[str]
    filter: Optional[_Program]
    inference_api: Union[CodeProjectAIObject, CodeProjectAIFace] = field(
        init=False, repr=False
    )

    def __post_init__(self):
        if self.pipeline_type == PIPELINE_OBJECT:
            self.inference_api = CodeProjectAIObject(
                ip=self.server.host,
                port=self.server.port,
                min_confidence=self.threshold,
                custom_model=self.model or "",
            )
        elif (
            self.pipeline_type == PIPELINE_FACE_DETECT
            or self.pipeline_type == PIPELINE_FACE_RECOGNIZE
        ):
            self.inference_api = CodeProjectAIFace(
                ip=self.server.host,
                port=self.server.port,
                min_confidence=self.threshold,
            )

    async def infer(
        self, session: aiohttp.ClientSession, event: FrigateEvent, snapshot: bytes
    ) -> Tuple[Optional[CPAIInference], FrigateEvent]:
        if (
            self.filter is not None
            and not self.filter.input_value(event.__dict__).first()
        ):
            return None, event
        logging.getLogger(CPAIPipeline.__name__).info(
            f"Detect {self.inference_api.detect} Recognize {self.inference_api.recognize}"
        )
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            if "detect" in self.pipeline_type:
                result = await loop.run_in_executor(
                    pool, self.inference_api.detect, snapshot  # type: ignore
                )
            else:
                result = await loop.run_in_executor(
                    pool, self.inference_api.recognize, snapshot  # type: ignore
                )
        inference = CPAIInference.parse(
            {
                "predictions": result,
                "label": "face" if "face" in self.pipeline_type else "",
            }
        )
        logging.getLogger("CPAIPipeline.infer").warn(f"RESULTS {inference}")
        if len(inference.predictions) == 0:
            return None, event
        if self.pipeline_type == PIPELINE_FACE_DETECT:
            for p in inference.predictions:
                p.label = "face"
        return inference, await self.set_sub_label(
            session, event, inference.predictions
        )

    async def set_sub_label(
        self,
        session: aiohttp.ClientSession,
        event: FrigateEvent,
        predictions: List[CPAIPrediction],
    ) -> FrigateEvent:
        if len(predictions) == 0:
            return event
        sorted_attributes = sorted(
            predictions, key=lambda x: x.confidence, reverse=True
        )
        top_label = sorted_attributes[0]
        _, sub_score = event.sub_label or (None, None)
        if sub_score is None or sub_score < top_label.confidence:
            async with session.post(
                f"{self.frigate}/api/events/{event.id}/sub_label",
                json={
                    "subLabel": top_label.label,
                    "subLabelScore": top_label.confidence,
                },
            ) as resp:
                resp.raise_for_status()
            event.sub_label = (top_label.label, top_label.confidence)
        attributes = {k: v for k, v in event.attributes.items()}
        attributes.update(
            {
                p.label: p.confidence
                for p in predictions
                if p.confidence > attributes.get(p.label, 0.0)
            }
        )
        all_attributes = [
            *event.current_attributes,
            *[
                {
                    "label": p.label,
                    "score": p.confidence,
                    "box": [p.y_min, p.x_min, p.y_max, p.x_max],
                }
                for p in sorted_attributes
            ],
        ]

        def key(a: Dict[str, Any]) -> str:
            return f"{a['box'][0]} {a['box'][1]} {a['box'][2]}{a['box'][3]}"

        current_attributes: Dict[str, Dict[str, Any]] = {}
        [
            current_attributes.update({key(a): a})
            for a in all_attributes
            if key(a) not in current_attributes
        ]
        event.current_attributes = list(current_attributes.values())
        return event


@dataclass
class CPAITopic:
    subscribe: str
    pipelines: List[CPAIPipeline]
    filter: Optional[_Program]
    topic_pattern: re.Pattern = field(init=False)
    _logger: logging.Logger = field(
        default=logging.getLogger("CPAITopic"), init=False, repr=False
    )

    def __post_init__(self):
        self.topic_pattern = re.compile(
            apply_anchors(
                self.subscribe.replace("/", r"\/")
                .replace("+", r"[^\/]+?")
                .replace("#", r".+")
            )
        )

    def matches_subscription(self, topic: str) -> bool:
        if topic is None or len(topic.strip()) == 0:
            return False
        if self.subscribe == topic:
            return True
        if "$" in [topic[0], self.subscribe[0]] and topic[0] != self.subscribe[0]:
            return True

        if not self.topic_pattern.match(topic):
            return False
        return True

    async def process_event(
        self, session: aiohttp.ClientSession, event: FrigateEvent, snapshot: bytes
    ) -> Tuple[FrigateEvent, bool]:
        logger = self._logger.getChild(self.subscribe)
        inferences: List[CPAIInference] = []
        logger.info(self.pipelines)
        for pipeline in self.pipelines:
            try:
                inference, event = await pipeline.infer(session, event, snapshot)
                if not inference or len(inference.predictions) == 0:
                    return event, False
                inferences.append(inference)
            except Exception as exc:
                logger.error(
                    "Error running inference on event %s: %s" % (event.id, str(exc)),
                    exc_info=exc,
                )
                raise InferenceError(
                    "Error running inference on event %s: %s" % (event.id, str(exc)),
                    inferences=inferences,
                ) from exc

        return event, True
