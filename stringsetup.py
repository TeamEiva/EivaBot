#!/usr/bin/env python3
"""Generate a Telethon StringSession for EivaBot.

Run:  python stringsetup.py
Requires: pip install telethon
"""
import asyncio
import os

from telethon import TelegramClient
from telethon.sessions import StringSession

print(
    """Please go-to my.telegram.org
Login using your Telegram account
Click on API Development Tools
Create a new application, by entering the required details"""
)

APP_ID = int(input("Enter APP ID here: ").strip())
API_HASH = input("Enter API HASH here: ").strip()


async def main() -> None:
    async with TelegramClient(StringSession(), APP_ID, API_HASH) as client:
        session = client.session.save()
        print("\nEivaBOT_SESSION value (store it in your environment, never commit it):\n")
        print(session)
        # Also send to Saved Messages for convenience.
        await client.send_message("me", session)


if __name__ == "__main__":
    if os.name == "nt":
        # Windows: ensure the default event-loop policy works with Telethon.
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
