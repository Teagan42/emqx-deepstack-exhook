from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor


class ProviderLoadedRequest(_message.Message):
    __slots__ = ("broker", "meta")
    BROKER_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    broker: BrokerInfo
    meta: RequestMeta
    def __init__(self, broker: _Optional[_Union[BrokerInfo, _Mapping]] = ...,
                 meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ProviderUnloadedRequest(_message.Message):
    __slots__ = ("meta",)
    META_FIELD_NUMBER: _ClassVar[int]
    meta: RequestMeta
    def __init__(
        self, meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ClientConnectRequest(_message.Message):
    __slots__ = ("conninfo", "props", "meta")
    CONNINFO_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    conninfo: ConnInfo
    props: _containers.RepeatedCompositeFieldContainer[Property]
    meta: RequestMeta
    def __init__(self, conninfo: _Optional[_Union[ConnInfo, _Mapping]] = ..., props: _Optional[_Iterable[_Union[Property,
                 _Mapping]]] = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ClientConnackRequest(_message.Message):
    __slots__ = ("conninfo", "result_code", "props", "meta")
    CONNINFO_FIELD_NUMBER: _ClassVar[int]
    RESULT_CODE_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    conninfo: ConnInfo
    result_code: str
    props: _containers.RepeatedCompositeFieldContainer[Property]
    meta: RequestMeta
    def __init__(self, conninfo: _Optional[_Union[ConnInfo, _Mapping]] = ..., result_code: _Optional[str] = ...,
                 props: _Optional[_Iterable[_Union[Property, _Mapping]]] = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ClientConnectedRequest(_message.Message):
    __slots__ = ("clientinfo", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ClientDisconnectedRequest(_message.Message):
    __slots__ = ("clientinfo", "reason", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    reason: str
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., reason: _Optional[str]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ClientAuthenticateRequest(_message.Message):
    __slots__ = ("clientinfo", "result", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    result: bool
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ...,
                 result: bool = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ClientAuthorizeRequest(_message.Message):
    __slots__ = ("clientinfo", "type", "topic", "result", "meta")

    class AuthorizeReqType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PUBLISH: _ClassVar[ClientAuthorizeRequest.AuthorizeReqType]
        SUBSCRIBE: _ClassVar[ClientAuthorizeRequest.AuthorizeReqType]
    PUBLISH: ClientAuthorizeRequest.AuthorizeReqType
    SUBSCRIBE: ClientAuthorizeRequest.AuthorizeReqType
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    type: ClientAuthorizeRequest.AuthorizeReqType
    topic: str
    result: bool
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., type: _Optional[_Union[ClientAuthorizeRequest.AuthorizeReqType, str]]
                 = ..., topic: _Optional[str] = ..., result: bool = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ClientSubscribeRequest(_message.Message):
    __slots__ = ("clientinfo", "props", "topic_filters", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FILTERS_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    props: _containers.RepeatedCompositeFieldContainer[Property]
    topic_filters: _containers.RepeatedCompositeFieldContainer[TopicFilter]
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., props: _Optional[_Iterable[_Union[Property, _Mapping]]] = ...,
                 topic_filters: _Optional[_Iterable[_Union[TopicFilter, _Mapping]]] = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class ClientUnsubscribeRequest(_message.Message):
    __slots__ = ("clientinfo", "props", "topic_filters", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    PROPS_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FILTERS_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    props: _containers.RepeatedCompositeFieldContainer[Property]
    topic_filters: _containers.RepeatedCompositeFieldContainer[TopicFilter]
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., props: _Optional[_Iterable[_Union[Property, _Mapping]]] = ...,
                 topic_filters: _Optional[_Iterable[_Union[TopicFilter, _Mapping]]] = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class SessionCreatedRequest(_message.Message):
    __slots__ = ("clientinfo", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class SessionSubscribedRequest(_message.Message):
    __slots__ = ("clientinfo", "topic", "subopts", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    SUBOPTS_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    topic: str
    subopts: SubOpts
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., topic: _Optional[str] = ...,
                 subopts: _Optional[_Union[SubOpts, _Mapping]] = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class SessionUnsubscribedRequest(_message.Message):
    __slots__ = ("clientinfo", "topic", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    topic: str
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., topic: _Optional[str]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class SessionResumedRequest(_message.Message):
    __slots__ = ("clientinfo", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class SessionDiscardedRequest(_message.Message):
    __slots__ = ("clientinfo", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class SessionTakenoverRequest(_message.Message):
    __slots__ = ("clientinfo", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class SessionTerminatedRequest(_message.Message):
    __slots__ = ("clientinfo", "reason", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    reason: str
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., reason: _Optional[str]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class MessagePublishRequest(_message.Message):
    __slots__ = ("message", "meta")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    message: Message
    meta: RequestMeta
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ...,
                 meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class MessageDeliveredRequest(_message.Message):
    __slots__ = ("clientinfo", "message", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    message: Message
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., message: _Optional[_Union[Message,
                 _Mapping]] = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class MessageDroppedRequest(_message.Message):
    __slots__ = ("message", "reason", "meta")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    message: Message
    reason: str
    meta: RequestMeta
    def __init__(self, message: _Optional[_Union[Message, _Mapping]] = ..., reason: _Optional[str]
                 = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class MessageAckedRequest(_message.Message):
    __slots__ = ("clientinfo", "message", "meta")
    CLIENTINFO_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    clientinfo: ClientInfo
    message: Message
    meta: RequestMeta
    def __init__(self, clientinfo: _Optional[_Union[ClientInfo, _Mapping]] = ..., message: _Optional[_Union[Message,
                 _Mapping]] = ..., meta: _Optional[_Union[RequestMeta, _Mapping]] = ...) -> None: ...


class LoadedResponse(_message.Message):
    __slots__ = ("hooks",)
    HOOKS_FIELD_NUMBER: _ClassVar[int]
    hooks: _containers.RepeatedCompositeFieldContainer[HookSpec]
    def __init__(
        self, hooks: _Optional[_Iterable[_Union[HookSpec, _Mapping]]] = ...) -> None: ...


class ValuedResponse(_message.Message):
    __slots__ = ("type", "bool_result", "message")

    class ResponsedType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONTINUE: _ClassVar[ValuedResponse.ResponsedType]
        IGNORE: _ClassVar[ValuedResponse.ResponsedType]
        STOP_AND_RETURN: _ClassVar[ValuedResponse.ResponsedType]
    CONTINUE: ValuedResponse.ResponsedType
    IGNORE: ValuedResponse.ResponsedType
    STOP_AND_RETURN: ValuedResponse.ResponsedType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    BOOL_RESULT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: ValuedResponse.ResponsedType
    bool_result: bool
    message: Message
    def __init__(self, type: _Optional[_Union[ValuedResponse.ResponsedType, str]] = ...,
                 bool_result: bool = ..., message: _Optional[_Union[Message, _Mapping]] = ...) -> None: ...


class EmptySuccess(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...


class BrokerInfo(_message.Message):
    __slots__ = ("version", "sysdescr", "uptime", "datetime")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SYSDESCR_FIELD_NUMBER: _ClassVar[int]
    UPTIME_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FIELD_NUMBER: _ClassVar[int]
    version: str
    sysdescr: str
    uptime: int
    datetime: str
    def __init__(self, version: _Optional[str] = ..., sysdescr: _Optional[str] = ...,
                 uptime: _Optional[int] = ..., datetime: _Optional[str] = ...) -> None: ...


class HookSpec(_message.Message):
    __slots__ = ("name", "topics")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    name: str
    topics: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ...,
                 topics: _Optional[_Iterable[str]] = ...) -> None: ...


class ConnInfo(_message.Message):
    __slots__ = ("node", "clientid", "username", "peerhost",
                 "sockport", "proto_name", "proto_ver", "keepalive", "peerport")
    NODE_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PEERHOST_FIELD_NUMBER: _ClassVar[int]
    SOCKPORT_FIELD_NUMBER: _ClassVar[int]
    PROTO_NAME_FIELD_NUMBER: _ClassVar[int]
    PROTO_VER_FIELD_NUMBER: _ClassVar[int]
    KEEPALIVE_FIELD_NUMBER: _ClassVar[int]
    PEERPORT_FIELD_NUMBER: _ClassVar[int]
    node: str
    clientid: str
    username: str
    peerhost: str
    sockport: int
    proto_name: str
    proto_ver: str
    keepalive: int
    peerport: int
    def __init__(self, node: _Optional[str] = ..., clientid: _Optional[str] = ..., username: _Optional[str] = ..., peerhost: _Optional[str] = ..., sockport: _Optional[int]
                 = ..., proto_name: _Optional[str] = ..., proto_ver: _Optional[str] = ..., keepalive: _Optional[int] = ..., peerport: _Optional[int] = ...) -> None: ...


class ClientInfo(_message.Message):
    __slots__ = ("node", "clientid", "username", "password", "peerhost", "sockport",
                 "protocol", "mountpoint", "is_superuser", "anonymous", "cn", "dn", "peerport")
    NODE_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    PEERHOST_FIELD_NUMBER: _ClassVar[int]
    SOCKPORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    MOUNTPOINT_FIELD_NUMBER: _ClassVar[int]
    IS_SUPERUSER_FIELD_NUMBER: _ClassVar[int]
    ANONYMOUS_FIELD_NUMBER: _ClassVar[int]
    CN_FIELD_NUMBER: _ClassVar[int]
    DN_FIELD_NUMBER: _ClassVar[int]
    PEERPORT_FIELD_NUMBER: _ClassVar[int]
    node: str
    clientid: str
    username: str
    password: str
    peerhost: str
    sockport: int
    protocol: str
    mountpoint: str
    is_superuser: bool
    anonymous: bool
    cn: str
    dn: str
    peerport: int
    def __init__(self, node: _Optional[str] = ..., clientid: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., peerhost: _Optional[str] = ..., sockport: _Optional[int] = ...,
                 protocol: _Optional[str] = ..., mountpoint: _Optional[str] = ..., is_superuser: bool = ..., anonymous: bool = ..., cn: _Optional[str] = ..., dn: _Optional[str] = ..., peerport: _Optional[int] = ...) -> None: ...


class Message(_message.Message):
    __slots__ = ("node", "id", "qos", "topic",
                 "payload", "timestamp", "headers")

    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str

        def __init__(self, key: _Optional[str] = ...,
                     value: _Optional[str] = ...) -> None: ...
    NODE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    QOS_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    node: str
    id: str
    qos: int
    topic: str
    payload: bytes
    timestamp: int
    headers: _containers.ScalarMap[str, str]
    def __init__(self, node: _Optional[str] = ..., id: _Optional[str] = ..., qos: _Optional[int] = ..., topic: _Optional[str] = ...,
                 payload: _Optional[bytes] = ..., timestamp: _Optional[int] = ..., headers: _Optional[_Mapping[str, str]] = ..., **kwargs) -> None: ...


class Property(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ...,
                 value: _Optional[str] = ...) -> None: ...


class TopicFilter(_message.Message):
    __slots__ = ("name", "subopts")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SUBOPTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    subopts: SubOpts
    def __init__(self, name: _Optional[str] = ...,
                 subopts: _Optional[_Union[SubOpts, _Mapping]] = ...) -> None: ...


class SubOpts(_message.Message):
    __slots__ = ("qos", "rh", "rap", "nl")
    QOS_FIELD_NUMBER: _ClassVar[int]
    RH_FIELD_NUMBER: _ClassVar[int]
    RAP_FIELD_NUMBER: _ClassVar[int]
    NL_FIELD_NUMBER: _ClassVar[int]
    qos: int
    rh: int
    rap: int
    nl: int
    def __init__(self, qos: _Optional[int] = ..., rh: _Optional[int] = ...,
                 rap: _Optional[int] = ..., nl: _Optional[int] = ...) -> None: ...


class RequestMeta(_message.Message):
    __slots__ = ("node", "version", "sysdescr", "cluster_name")
    NODE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SYSDESCR_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    node: str
    version: str
    sysdescr: str
    cluster_name: str

    def __init__(self, node: _Optional[str] = ..., version: _Optional[str] = ...,
                 sysdescr: _Optional[str] = ..., cluster_name: _Optional[str] = ...) -> None: ...
