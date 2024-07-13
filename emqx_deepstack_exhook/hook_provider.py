from emqx_deepstack_exhook.pb2.exhook_pb2 import EmptySuccess, HookSpec, LoadedResponse, ValuedResponse
from emqx_deepstack_exhook.pb2.exhook_pb2_grpc import HookProviderServicer


class HookProvider(HookProviderServicer):

    def OnProviderLoaded(self, request, context):
        print("OnProviderLoaded:", request)
        specs = [HookSpec(name="client.connect"),
                 HookSpec(name="client.connack"),
                 HookSpec(name="client.connected"),
                 HookSpec(name="client.disconnected"),
                 HookSpec(name="client.authenticate"),
                 HookSpec(name="client.authorize"),
                 HookSpec(name="client.subscribe"),
                 HookSpec(name="client.unsubscribe"),

                 HookSpec(name="session.created"),
                 HookSpec(name="session.subscribed"),
                 HookSpec(name="session.unsubscribed"),
                 HookSpec(name="session.resumed"),
                 HookSpec(name="session.discarded"),
                 HookSpec(name="session.takenover"),
                 HookSpec(name="session.terminated"),

                 HookSpec(name="message.publish"),
                 HookSpec(name="message.delivered"),
                 HookSpec(name="message.acked"),
                 HookSpec(name="message.dropped")
                 ]
        return LoadedResponse(hooks=specs)

    def OnProviderUnloaded(self, request, context):
        print("OnProviderUnloaded:", request)
        return EmptySuccess()

    def OnClientConnect(self, request, context):
        print("OnClientConnect:", request)
        return EmptySuccess()

    def OnClientConnack(self, request, context):
        print("OnClientConnack:", request)
        return EmptySuccess()

    def OnClientConnected(self, request, context):
        print("OnClientConnected:", request)
        return EmptySuccess()

    def OnClientDisconnected(self, request, context):
        print("OnClientDisconnected:", request)
        return EmptySuccess()

    def OnClientAuthenticate(self, request, context):
        print("OnClientAuthenticate:", request)
        reply = ValuedResponse(type="STOP_AND_RETURN", bool_result=True)
        return reply

    def OnClientAuthorize(self, request, context):
        print("OnClientAuthorize:", request)
        reply = ValuedResponse(type="STOP_AND_RETURN", bool_result=True)
        return reply

    def OnClientSubscribe(self, request, context):
        print("OnClientSubscribe:", request)
        return EmptySuccess()

    def OnClientUnsubscribe(self, request, context):
        print("OnClientUnsubscribe:", request)
        return EmptySuccess()

    def OnSessionCreated(self, request, context):
        print("OnSessionCreated:", request)
        return EmptySuccess()

    def OnSessionSubscribed(self, request, context):
        print("OnSessionSubscribed:", request)
        return EmptySuccess()

    def OnSessionUnsubscribed(self, request, context):
        print("OnSessionUnsubscribed:", request)
        return EmptySuccess()

    def OnSessionResumed(self, request, context):
        print("OnSessionResumed:", request)
        return EmptySuccess()

    def OnSessionDiscarded(self, request, context):
        print("OnSessionDiscarded:", request)
        return EmptySuccess()

    def OnSessionTakenover(self, request, context):
        print("OnSessionTakenover:", request)
        return EmptySuccess()

    def OnSessionTerminated(self, request, context):
        print("OnSessionTerminated:", request)
        return EmptySuccess()

    def OnMessagePublish(self, request, context):
        print("OnMessagePublish:", request)
        nmsg = request.message
        nmsg.payload = b"hardcode payload by exhook-svr-python :)"

        reply = ValuedResponse(type="STOP_AND_RETURN", message=nmsg)
        return reply

    # case2: stop publish the 't/d' messages
    # def OnMessagePublish(self, request, context):
    #    nmsg = request.message
    #    if nmsg.topic == 't/d':
    #        nmsg.payload = b""
    #        nmsg.headers['allow_publish'] = b"false"
    #
    #    reply = ValuedResponse(type="STOP_AND_RETURN", message=nmsg)
    #    return reply

    def OnMessageDelivered(self, request, context):
        print("OnMessageDelivered:", request)
        return EmptySuccess()

    def OnMessageDropped(self, request, context):
        print("OnMessageDropped:", request)
        return EmptySuccess()

    def OnMessageAcked(self, request, context):
        print("OnMessageAcked:", request)
        return EmptySuccess()
