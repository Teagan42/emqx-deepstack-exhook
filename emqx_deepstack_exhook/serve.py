import asyncio
from typing import Optional
import aiohttp
import click
from concurrent import futures
import logging
import voluptuous as vol
import grpc.aio as g_aio
import aiofiles
from yaml import load
import os
from emqx_deepstack_exhook.config import Config
from emqx_deepstack_exhook.cpai import CPAIProcess

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from emqx_deepstack_exhook.config.schema import SCHEMA_CONFIG
from emqx_deepstack_exhook.hook_provider import HookProvider

from emqx_deepstack_exhook.pb2.exhook_pb2_grpc import (
    add_HookProviderServicer_to_server,
)

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger(__name__)

_session: aiohttp.ClientSession = aiohttp.ClientSession()
_task: asyncio.Task
_last_modified = 0.0
_cleanup_coroutines = []


async def reload_config(config_file: str, servicer: HookProvider) -> None:
    try:
        config = await load_config(config_file)
    except Exception as exc:
        logging.getLogger("reload_config").error(
            f"Error reloading config: {str(exc)}", exc_info=exc
        )
        return

    try:
        await servicer.set_cpai(CPAIProcess(config, _session))
        logging.getLogger("reload_conif").info("Config reloaded!")
    except Exception as exc:
        logging.getLogger("reload_config").error(
            f"Error assigning new config: {str(exc)}", exc_info=exc
        )
        return


async def check_for_changes(config_file: str, servicer: HookProvider):
    global _last_modified
    while True:
        await asyncio.sleep(10)
        logging.getLogger("check_for_changes").info("Checking for changes...")
        mtime = os.stat(config_file).st_mtime
        if mtime != _last_modified:
            logging.getLogger("check_for_changes").info("Loading changes...")
            await reload_config(config_file, servicer)


def stop_config_watch():
    global _task
    _task.cancel()


async def load_config(config_file: str) -> Config:
    async with aiofiles.open(config_file, mode="r") as f:
        config = load(await f.read(), Loader=Loader)
    global _last_modified
    _last_modified = os.stat(config_file).st_mtime
    try:
        config = SCHEMA_CONFIG(config)
    except vol.Invalid as exc:
        _LOGGER.error("Invalid config", exc_info=exc)
        raise exc
    return Config.load(config)


async def serve(config_file):
    """Start up the EMQX ExHook gRPC server.

    CONFIG_FILE is the path to the file specifying the configuration for this server."""
    try:
        config = await load_config(config_file)
    except:
        exit(1)

    server = g_aio.server(futures.ThreadPoolExecutor(max_workers=config.threads))
    cpai = CPAIProcess(config)
    hook_provider = HookProvider(cpai=cpai)

    add_HookProviderServicer_to_server(hook_provider, server)
    server.add_insecure_port(config.bind_address)
    await server.start()
    loop = asyncio.get_event_loop()
    global _task
    _task = loop.create_task(check_for_changes(config_file, hook_provider))
    asyncio.ensure_future(_task)
    _LOGGER.info("Started gRPC server on %s", config.bind_address)

    async def graceful_shutdown():
        stop_config_watch()
        await server.stop(1)

    _cleanup_coroutines.append(graceful_shutdown())
    _cleanup_coroutines.append(_session.close())
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
    try:
        loop.run_until_complete(serve(config_file=config_file))
    finally:
        asyncio.gather(*_cleanup_coroutines)
        loop.close()
