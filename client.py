from __future__ import print_function

import logging

import grpc
import emqx_deepstack_exhook.hook_provider
import emqx_deepstack_exhook.pb2.exhook_pb2
import emqx_deepstack_exhook.pb2.exhook_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:9000") as channel:
        stub = emqx_deepstack_exhook.pb2.exhook_pb2_grpc.HookProviderStub(channel)
        response = stub.OnMessagePublish(
            emqx_deepstack_exhook.pb2.exhook_pb2.MessagePublishRequest(
                message={
                    "topic": "frigate/driveway/event/car",
                    "payload": b'{"id": "1720860695.72587-ja8pzq", "camera": "driveway", "label": "car"}',
                }
            )
        )
    print(response.message)
