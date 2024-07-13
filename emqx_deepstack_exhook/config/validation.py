from enum import StrEnum
import re

from typing import Any, Callable, TypeVar, cast, overload
from urllib.parse import urlparse
import slugify as unicode_slug
import voluptuous as vol

_T = TypeVar("_T")


class UrlProtocolSchema(StrEnum):
    """Valid URL protocol schema values."""

    HTTP = "http"
    HTTPS = "https"


EXTERNAL_URL_PROTOCOL_SCHEMA_LIST = frozenset(
    {UrlProtocolSchema.HTTP, UrlProtocolSchema.HTTPS}
)


def util_slugify(text: str | None, *, separator: str = "_") -> str:
    """Slugify a given text."""
    if text == "" or text is None:
        return ""
    slug = unicode_slug.slugify(text, separator=separator)
    return "unknown" if slug == "" else slug


def slug(value: Any) -> str:
    """Validate value is a valid slug."""
    if value is None:
        raise vol.Invalid("Slug should not be None")
    str_value = str(value)
    slg = util_slugify(str_value)
    if str_value == slg:
        return str_value
    raise vol.Invalid(f"invalid slug {value} (try {slg})")


def schema_with_slug_keys(
    value_schema: dict | Callable, *, slug_validator: Callable[[Any], str] = slug
) -> Callable:
    """Ensure dicts have slugs as keys.

    Replacement of vol.Schema({cv.slug: value_schema}) to prevent misleading
    "Extra keys" errors from voluptuous.
    """
    schema = vol.Schema({str: value_schema})

    def verify(value: dict) -> dict:
        """Validate all keys are slugs and then the value_schema."""
        if not isinstance(value, dict):
            raise vol.Invalid("expected dictionary")

        for key in value:
            slug_validator(key)

        return cast(dict, schema(value))

    return verify


def slugify(value: Any) -> str:
    """Coerce a value to a slug."""
    if value is None:
        raise vol.Invalid("Slug should not be None")
    slg = util_slugify(str(value))
    if slg:
        return slg
    raise vol.Invalid(f"Unable to slugify {value}")


def string(value: Any) -> str:
    """Coerce value to string, except for None."""
    if value is None:
        raise vol.Invalid("string value is None")

    # This is expected to be the most common case, so check it first.
    if type(value) is str or isinstance(value, str):  # noqa: E721
        return value

    elif isinstance(value, (list, dict)):
        raise vol.Invalid("value should be a string")
    return str(value)


def matches_regex(regex: str) -> Callable[[Any], str]:
    """Validate that the value is a string that matches a regex."""
    compiled = re.compile(regex)

    def validator(value: Any) -> str:
        """Validate that value matches the given regex."""
        if not isinstance(value, str):
            raise vol.Invalid(f"not a string value: {value}")

        if not compiled.match(value):
            raise vol.Invalid(
                f"value {value} does not match regular expression {compiled.pattern}"
            )

        return value

    return validator


def valid_topic(topic: Any) -> str:
    """Validate that this is a valid topic name/filter.

    This function is not cached and is not expected to be called
    directly outside of this module. It is not marked as protected
    only because its tested directly in test_util.py.

    If it gets used outside of valid_subscribe_topic and
    valid_publish_topic, it may need an lru_cache decorator or
    an lru_cache decorator on the function where its used.
    """
    validated_topic = string(topic)
    try:
        raw_validated_topic = validated_topic.encode("utf-8")
    except UnicodeError as err:
        raise vol.Invalid("MQTT topic name/filter must be valid UTF-8 string.") from err

    if not raw_validated_topic:
        raise vol.Invalid("MQTT topic name/filter must not be empty.")
    if len(raw_validated_topic) > 65535:
        raise vol.Invalid(
            "MQTT topic name/filter must not be longer than 65535 encoded bytes."
        )

    for char in validated_topic:
        if char == "\0":
            raise vol.Invalid("MQTT topic name/filter must not contain null character.")
        if char <= "\u001f" or "\u007f" <= char <= "\u009f":
            raise vol.Invalid(
                "MQTT topic name/filter must not contain control characters."
            )
        if "\ufdd0" <= char <= "\ufdef" or (ord(char) & 0xFFFF) in (0xFFFE, 0xFFFF):
            raise vol.Invalid("MQTT topic name/filter must not contain non-characters.")
    return validated_topic


def valid_subscribe_topic(topic: Any) -> str:
    """Validate that we can subscribe using this MQTT topic."""
    validated_topic = valid_topic(topic)
    if "+" in validated_topic:
        for i in (i for i, c in enumerate(validated_topic) if c == "+"):
            if (i > 0 and validated_topic[i - 1] != "/") or (
                i < len(validated_topic) - 1 and validated_topic[i + 1] != "/"
            ):
                raise vol.Invalid(
                    "Single-level wildcard must occupy an entire level of the filter"
                )

    index = validated_topic.find("#")
    if index != -1:
        if index != len(validated_topic) - 1:
            # If there are multiple wildcards, this will also trigger
            raise vol.Invalid(
                "Multi-level wildcard must be the last character in the topic filter."
            )
        if len(validated_topic) > 1 and validated_topic[index - 1] != "/":
            raise vol.Invalid(
                "Multi-level wildcard must be after a topic level separator."
            )

    return validated_topic


def ensure_list(value: _T | None) -> list[_T] | list[Any]:
    """Wrap value in list if it is not one."""
    if value is None:
        return []
    return cast("list[_T]", value) if isinstance(value, list) else [value]


port = vol.All(vol.Coerce(int), vol.Range(min=1, max=65535))
threads = vol.All(vol.Coerce(int), vol.Range(min=1, max=15))
small_float = vol.All(vol.Coerce(float), vol.Range(min=0, max=1))
ip_address = vol.All(vol.Coerce(str), matches_regex(r"^(?:\d{1,3}\.){3}\d{1,3}$"))
bind_address = vol.All(
    vol.Coerce(str), matches_regex(r"^(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}$")
)
fqdn = vol.All(
    vol.Coerce(str),
    matches_regex(
        r"(?=^.{1,253}$)(^(((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9])|((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63})$)"
    ),
)


def url(value: Any) -> str:
    if value is None:
        raise vol.Invalid("url cannot be None")

    url_in = str(value)

    return cast(str, vol.Schema(vol.Url())(url_in))  # type: ignore


def url_no_path(value: Any) -> str:
    """Validate a url without a path."""
    if value is None:
        raise vol.Invalid("url cannot be None")

    url_in = url(value)

    if urlparse(url_in).path not in ("", "/"):
        raise vol.Invalid("url it not allowed to have a path component")

    return url_in
