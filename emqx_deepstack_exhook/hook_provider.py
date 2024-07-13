import asyncio
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
        self._logger = logging.getLogger(HookProvider.__name__)
        self._cpai: CPAIProcess = cpai
        self._lock: asyncio.Lock = asyncio.Lock()

    async def set_cpai(self, cpai: CPAIProcess):
        await self._lock.acquire()
        try:
            prev = self._cpai
            self._cpai = cpai

        except Exception as exc:
            self._logger.error(f"Error assigning CPAI: {str(exc)}", exc_info=exc)
        finally:
            self._lock.release()

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

    async def OnProviderUnloaded(self, request, context) -> EmptySuccess:
        print("OnProviderUnloaded:", request)
        return EmptySuccess()

    async def OnClientConnect(self, request, context) -> EmptySuccess:
        print("OnClientConnect:", request)
        return EmptySuccess()

    async def OnClientConnack(self, request, context) -> EmptySuccess:
        print("OnClientConnack:", request)
        return EmptySuccess()

    async def OnClientConnected(self, request, context) -> EmptySuccess:
        print("OnClientConnected:", request)
        return EmptySuccess()

    async def OnClientDisconnected(self, request, context) -> EmptySuccess:
        print("OnClientDisconnected:", request)
        return EmptySuccess()

    async def OnClientAuthenticate(self, request, context) -> ValuedResponse:
        print("OnClientAuthenticate:", request)
        return ValuedResponse(type=ValuedResponse.ResponsedType.IGNORE)

    async def OnClientAuthorize(self, request, context) -> ValuedResponse:
        print("OnClientAuthorize:", request)
        return ValuedResponse(type=ValuedResponse.ResponsedType.IGNORE)

    async def OnClientSubscribe(self, request, context):
        print("OnClientSubscribe:", request)
        return EmptySuccess()

    async def OnClientUnsubscribe(self, request, context) -> EmptySuccess:
        print("OnClientUnsubscribe:", request)
        return EmptySuccess()

    async def OnSessionCreated(self, request, context) -> EmptySuccess:
        print("OnSessionCreated:", request)
        return EmptySuccess()

    async def OnSessionSubscribed(self, request, context) -> EmptySuccess:
        print("OnSessionSubscribed:", request)
        return EmptySuccess()

    async def OnSessionUnsubscribed(self, request, context) -> EmptySuccess:
        print("OnSessionUnsubscribed:", request)
        return EmptySuccess()

    async def OnSessionResumed(self, request, context) -> EmptySuccess:
        print("OnSessionResumed:", request)
        return EmptySuccess()

    async def OnSessionDiscarded(self, request, context) -> EmptySuccess:
        print("OnSessionDiscarded:", request)
        return EmptySuccess()

    async def OnSessionTakenover(self, request, context) -> EmptySuccess:
        print("OnSessionTakenover:", request)
        return EmptySuccess()

    async def OnSessionTerminated(self, request, context) -> EmptySuccess:
        print("OnSessionTerminated:", request)
        return EmptySuccess()

    async def OnMessagePublish(self, request, context) -> ValuedResponse:
        print("OnMessagePublish:", request)
        await self._lock.acquire()
        try:
            event = await self._cpai.process_message(
                request.message.topic, request.message
            )
            if event is None:
                return ValuedResponse(type=ValuedResponse.IGNORE)
            nmsg = request.message
            nmsg.payload = json.dumps(event).encode("utf-8")

            return ValuedResponse(type=ValuedResponse.CONTINUE, message=nmsg)
        except Exception as exc:
            self._logger.error(f"Error processing message: {str(exc)}", exc_info=exc)
            return ValuedResponse(type=ValuedResponse.IGNORE, message=request.message)
        finally:
            self._lock.release()

    async def OnMessageDelivered(self, request, context) -> EmptySuccess:
        print("OnMessageDelivered:", request)
        return EmptySuccess()

    async def OnMessageDropped(self, request, context) -> EmptySuccess:
        print("OnMessageDropped:", request)
        return EmptySuccess()

    async def OnMessageAcked(self, request, context) -> EmptySuccess:
        print("OnMessageAcked:", request)
        return EmptySuccess()
