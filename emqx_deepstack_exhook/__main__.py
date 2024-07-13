# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC exhook server."""

from concurrent import futures
import logging
from multiprocessing.sharedctypes import Value

import grpc

from emqx_deepstack_exhook.hook_provider import HookProvider

from emqx_deepstack_exhook.pb2.exhook_pb2_grpc import add_HookProviderServicer_to_server


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HookProviderServicer_to_server(HookProvider(), server)
    server.add_insecure_port('[::]:9000')
    server.start()

    print("Started gRPC server on [::]:9000")

    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
