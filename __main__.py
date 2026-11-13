"""EivaBot package.

The upstream plugin suite is fetched at runtime by the `Eivabot` launcher
(see Procfile) into the working directory, where the `Eivabot` module tree
shadows this lightweight shim when run via `bash Eivabot`. Locally, running
`python -m Eivabot` from a checkout without the plugin tree will use this
package, which validates configuration and connects a Telethon client.
"""
from __future__ import annotations

import asyncio
import logging
import os
import sys

logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("Eivabot")


def _build_client():
    from .config import Config
    from telethon import TelegramClient
    from telethon.sessions import StringSession

    cfg = Config.from_env()
    session = StringSession(cfg.session)
    return TelegramClient(
        session,
        cfg.api_id,
        cfg.api_hash,
        connection_retries=None,  # retry indefinitely, Telethon backs off
    ), cfg


def main() -> int:
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        client, cfg = _build_client()
    except Exception as exc:
        log.error("Configuration error: %s", exc)
        return 1

    log.info("Starting EivaBot (handler=%r)...", cfg.handler)
    try:
        with client:
            client.loop.run_until_complete(client.start())
            me = client.loop.run_until_complete(client.get_me())
            log.info("EivaBot started as %s", getattr(me, "first_name", me))
            client.run_until_disconnected()
    except KeyboardInterrupt:
        log.info("Shutdown requested — exiting gracefully.")
    except Exception:
        log.exception("EivaBot crashed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
