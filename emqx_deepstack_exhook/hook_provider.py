import logging
import json
from emqx_deepstack_exhook.cpai import CPAIProcess
from emqx_deepstack_exhook.pb2.exhook_pb2 import (
    EmptySuccess,
    HookSpec,
    LoadedResponse,
    ValuedResponse,
)
from emqx_deepstack_exhook.pb2.exhook_pb2_grpc import HookProviderServicer

_LOGGER = logging.getLogger(__name__)


class HookProvider(HookProviderServicer):
    _LOGGER = _LOGGER.getChild("HookProvider")

    def __init__(self, *args, cpai: CPAIProcess):
        super().__init__(*args)
        self._cpai = cpai

    async def OnProviderLoaded(self, request, context):
        _LOGGER.info("OnProviderLoaded:", request)
        specs = [
            # HookSpec(name="client.connect"),
            # HookSpec(name="client.connack"),
            # HookSpec(name="client.connected"),
            # HookSpec(name="client.disconnected"),
            # HookSpec(name="client.authenticate"),
            # HookSpec(name="client.authorize"),
            # HookSpec(name="client.subscribe"),
            # HookSpec(name="client.unsubscribe"),
            # HookSpec(name="session.created"),
            # HookSpec(name="session.subscribed"),
            # HookSpec(name="session.unsubscribed"),
            # HookSpec(name="session.resumed"),
            # HookSpec(name="session.discarded"),
            # HookSpec(name="session.takenover"),
            # HookSpec(name="session.terminated"),
            HookSpec(name="message.publish"),
            # HookSpec(name="message.delivered"),
            # HookSpec(name="message.acked"),
            # HookSpec(name="message.dropped")
        ]
        return LoadedResponse(hooks=specs)

    async def OnProviderUnloaded(self, request, context):
        print("OnProviderUnloaded:", request)
        return EmptySuccess()

    async def OnClientConnect(self, request, context):
        print("OnClientConnect:", request)
        return EmptySuccess()

    async def OnClientConnack(self, request, context):
        print("OnClientConnack:", request)
        return EmptySuccess()

    async def OnClientConnected(self, request, context):
        print("OnClientConnected:", request)
        return EmptySuccess()

    async def OnClientDisconnected(self, request, context):
        print("OnClientDisconnected:", request)
        return EmptySuccess()

    async def OnClientAuthenticate(self, request, context):
        print("OnClientAuthenticate:", request)
        return ValuedResponse(type=ValuedResponse.ResponsedType.IGNORE)

    async def OnClientAuthorize(self, request, context):
        print("OnClientAuthorize:", request)
        return ValuedResponse(type=ValuedResponse.ResponsedType.IGNORE)

    async def OnClientSubscribe(self, request, context):
        print("OnClientSubscribe:", request)
        return EmptySuccess()

    async def OnClientUnsubscribe(self, request, context):
        print("OnClientUnsubscribe:", request)
        return EmptySuccess()

    async def OnSessionCreated(self, request, context):
        print("OnSessionCreated:", request)
        return EmptySuccess()

    async def OnSessionSubscribed(self, request, context):
        print("OnSessionSubscribed:", request)
        return EmptySuccess()

    async def OnSessionUnsubscribed(self, request, context):
        print("OnSessionUnsubscribed:", request)
        return EmptySuccess()

    async def OnSessionResumed(self, request, context):
        print("OnSessionResumed:", request)
        return EmptySuccess()

    async def OnSessionDiscarded(self, request, context):
        print("OnSessionDiscarded:", request)
        return EmptySuccess()

    async def OnSessionTakenover(self, request, context):
        print("OnSessionTakenover:", request)
        return EmptySuccess()

    async def OnSessionTerminated(self, request, context):
        print("OnSessionTerminated:", request)
        return EmptySuccess()

    async def OnMessagePublish(self, request, context) -> ValuedResponse:
        print("OnMessagePublish:", request)
        event = await self._cpai.process_message(request.message.topic, request.message)
        nmsg = request.message
        nmsg.payload = json.dumps(event.__dict__).encode("utf-8")

        reply = ValuedResponse(type="CONTINUE", message=nmsg)
        return reply

    async def OnMessageDelivered(self, request, context):
        print("OnMessageDelivered:", request)
        return EmptySuccess()

    async def OnMessageDropped(self, request, context):
        print("OnMessageDropped:", request)
        return EmptySuccess()

    async def OnMessageAcked(self, request, context):
        print("OnMessageAcked:", request)
        return EmptySuccess()
