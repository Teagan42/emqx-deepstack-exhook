import asyncio
import click
from concurrent import futures
import logging
import voluptuous as vol
import grpc.aio as g_aio
from yaml import load

from emqx_deepstack_exhook.config import Config
from emqx_deepstack_exhook.cpai import CPAIProcess

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from emqx_deepstack_exhook.config.const import ATTR_BIND, ATTR_THREADS
from emqx_deepstack_exhook.config.schema import SCHEMA_CONFIG
from emqx_deepstack_exhook.hook_provider import HookProvider

from emqx_deepstack_exhook.pb2.exhook_pb2_grpc import add_HookProviderServicer_to_server

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)


async def serve(config_file):
    """Start up the EMQX ExHook gRPC server.

    CONFIG_FILE is the path to the file specifying the configuration for this server."""
    with open(config_file, "r") as f:
        config = load(f, Loader=Loader)
    try:
        config = SCHEMA_CONFIG(config)
    except vol.Invalid as exc:
        _LOGGER.error("Invalid config", exc_info=exc)
        exit(1)

    server = g_aio.server(futures.ThreadPoolExecutor(max_workers=config[ATTR_THREADS]))
    cpai = CPAIProcess(Config.load(config))
    add_HookProviderServicer_to_server(HookProvider(cpai=cpai), server)
    server.add_insecure_port(config[ATTR_BIND])
    await server.start()

    _LOGGER.info("Started gRPC server on %s", config[ATTR_BIND])

    await server.wait_for_termination()


@click.command()
@click.argument(
    "config_file",
    type=click.Path(
        exists=True, dir_okay=False, readable=True, resolve_path=True, allow_dash=False
    ),
    required=True,
)
def cli(config_file):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve(config_file=config_file))
