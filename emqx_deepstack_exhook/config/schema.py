from typing import Any, Dict
import voluptuous as vol

from emqx_deepstack_exhook.config.const import (
    ATTR_BIND,
    ATTR_BIND_IP,
    ATTR_BIND_PORT,
    ATTR_PIPELINE_FILTER,
    ATTR_PIPELINE_SERVER,
    ATTR_PIPELINE_MODEL,
    ATTR_PIPELINE_THRESHOLD,
    ATTR_PIPELINE_RESULT_TOPIC,
    ATTR_PIPELINES,
    ATTR_SERVER_HOST,
    ATTR_SERVER_PORT,
    ATTR_SERVERS,
    ATTR_THREADS,
    ATTR_TOPIC_PIPELINE,
    ATTR_TOPIC_TOPIC,
    ATTR_TOPICS,
    ATTR_FRIGATE_HOST,
    ATTR_FRIGATE_PORT,
    ATTR_FRIGATE,
)
from emqx_deepstack_exhook.config.validation import (
    ensure_list,
    schema_with_slug_keys,
    slugify,
    string,
    ip_address,
    url_no_path,
    valid_subscribe_topic,
    small_float,
    fqdn,
    port,
    bind_address,
    threads,
    valid_topic,
)

SCHEMA_FRIGATE_DICT = vol.Schema(
    {
        vol.Required(ATTR_FRIGATE_HOST): vol.Or(ip_address, fqdn),
        vol.Required(ATTR_FRIGATE_PORT): port,
    }
)


def ensure_frigate(value: Any | None) -> str:
    if value is None:
        raise vol.Invalid("frigate can not be None")
    if isinstance(value, dict):
        frigate_dict = SCHEMA_FRIGATE_DICT(value)
        value = f"{frigate_dict[ATTR_FRIGATE_HOST]}:{frigate_dict[ATTR_FRIGATE_PORT]}"
    if isinstance(value, str):
        return url_no_path(value)
    raise vol.Invalid("Invalid frigate configuration")


SCHEMA_FRIGATE = ensure_frigate


SCHEMA_TOPIC = vol.Schema(
    {
        vol.Required(ATTR_TOPIC_TOPIC): valid_subscribe_topic,
        vol.Required(ATTR_TOPIC_PIPELINE): vol.All(ensure_list, [slugify]),
    }
)

SCHEMA_PIPELINE = vol.Schema(
    {
        vol.Required(ATTR_PIPELINE_SERVER): slugify,
        vol.Optional(ATTR_PIPELINE_MODEL): string,
        vol.Optional(ATTR_PIPELINE_THRESHOLD, default=0.7): small_float,
        vol.Optional(ATTR_PIPELINE_RESULT_TOPIC): valid_topic,
        vol.Optional(ATTR_PIPELINE_FILTER): string,
    }
)

SCHEMA_SERVER = vol.Schema(
    {
        vol.Required(ATTR_SERVER_HOST): vol.Or(ip_address, fqdn),
        vol.Required(ATTR_SERVER_PORT): port,
    }
)

SCHEMA_BIND_DICT = vol.Schema(
    {vol.Required(ATTR_BIND_IP): ip_address, vol.Required(ATTR_BIND_PORT): port}
)


def ensure_bind(value: Any | None) -> str:
    if value is None:
        raise vol.Invalid("bind cannot be None")
    if isinstance(value, dict):
        bind_dict = SCHEMA_BIND_DICT(value)
        value = f"{bind_dict[ATTR_BIND_IP]}:{bind_dict[ATTR_BIND_PORT]}"
    if isinstance(value, str):
        return bind_address(value)
    raise vol.Invalid("invalid bind configuration")


SCHEMA_BIND = ensure_bind

SCHEMA_CONFIG = vol.Schema(
    {
        vol.Optional(
            ATTR_BIND, default={ATTR_BIND_IP: "0.0.0.0", ATTR_BIND_PORT: 9000}
        ): SCHEMA_BIND,
        vol.Optional(ATTR_THREADS, default=10): threads,
        vol.Required(ATTR_FRIGATE): SCHEMA_FRIGATE,
        vol.Required(ATTR_SERVERS): schema_with_slug_keys(SCHEMA_SERVER),
        vol.Required(ATTR_PIPELINES): schema_with_slug_keys(SCHEMA_PIPELINE),
        vol.Required(ATTR_TOPICS): vol.All(ensure_list, [SCHEMA_TOPIC]),
    }
)
