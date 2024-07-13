from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from emqx_deepstack_exhook.config.const import (
    ATTR_FRIGATE,
    ATTR_PIPELINE_MODEL,
    ATTR_PIPELINE_RESULT_TOPIC,
    ATTR_PIPELINE_SERVER,
    ATTR_PIPELINE_THRESHOLD,
    ATTR_PIPELINES,
    ATTR_SERVER_HOST,
    ATTR_SERVER_PORT,
    ATTR_SERVERS,
    ATTR_TOPIC_PIPELINE,
    ATTR_TOPIC_TOPIC,
    ATTR_TOPICS,
)


@dataclass
class ServerConfig:
    host: str
    port: int


@dataclass
class TopicConfig:
    subscribe: str
    pipelines: List[str]


@dataclass
class PipelineConfig:
    server: str
    model: Optional[str]
    threshold: float
    result_topic: Optional[str]


@dataclass
class Config:
    @classmethod
    def load(cls, config: Dict[str, Any]) -> "Config":
        return Config(
            servers={
                key: ServerConfig(
                    host=value[ATTR_SERVER_HOST], port=value[ATTR_SERVER_PORT]
                )
                for key, value in config[ATTR_SERVERS].items()
            },
            pipelines={
                key: PipelineConfig(
                    server=value[ATTR_PIPELINE_SERVER],
                    model=value.get(ATTR_PIPELINE_MODEL, None),
                    threshold=value[ATTR_PIPELINE_THRESHOLD],
                    result_topic=value.get(ATTR_PIPELINE_RESULT_TOPIC, None),
                )
                for key, value in config[ATTR_PIPELINES].items()
            },
            topics=[
                TopicConfig(
                    subscribe=topic[ATTR_TOPIC_TOPIC],
                    pipelines=topic[ATTR_TOPIC_PIPELINE],
                )
                for topic in config[ATTR_TOPICS]
            ],
            frigate=config[ATTR_FRIGATE],
        )

    servers: Dict[str, ServerConfig]
    pipelines: Dict[str, PipelineConfig]
    topics: List[TopicConfig]
    frigate: str
