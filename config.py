"""Centralized, validated configuration for EivaBot."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - python-dotenv is in requirements
    pass


class ConfigError(RuntimeError):
    """Raised when mandatory configuration is missing or invalid."""


@dataclass
class Config:
    """Validated runtime configuration loaded from environment variables."""

    api_id: int
    api_hash: str
    session: str
    handler: str = "."
    logger_id: Optional[int] = None
    bot_token: Optional[str] = None
    bot_username: Optional[str] = None
    pm_permit: bool = True
    sudo_users: List[int] = field(default_factory=list)
    mongo_db_url: Optional[str] = None
    database_url: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Config":
        api_id_raw = os.getenv("APP_ID", "").strip()
        api_hash = os.getenv("API_HASH", "").strip()
        session = os.getenv("EivaBOT_SESSION", os.getenv("SESSION", "")).strip()

        missing = [
            name
            for name, value in (
                ("APP_ID", api_id_raw),
                ("API_HASH", api_hash),
                ("EivaBOT_SESSION", session),
            )
            if not value
        ]
        if missing:
            raise ConfigError(
                "Missing required environment variables: "
                + ", ".join(missing)
                + ". See .env.example and the README for setup instructions."
            )

        try:
            api_id = int(api_id_raw)
        except ValueError as exc:
            raise ConfigError("APP_ID must be an integer from my.telegram.org") from exc

        logger_id: Optional[int] = None
        logger_raw = os.getenv("LOGGER_ID", "").strip()
        if logger_raw:
            try:
                logger_id = int(logger_raw)
            except ValueError as exc:
                raise ConfigError("LOGGER_ID must be an integer chat id") from exc

        sudo_users: List[int] = []
        for token in os.getenv("SUDO_USERS", "").replace(",", " ").split():
            try:
                sudo_users.append(int(token))
            except ValueError:
                print(f"[config] Ignoring non-numeric SUDO_USERS entry: {token!r}")

        return cls(
            api_id=api_id,
            api_hash=api_hash,
            session=session,
            handler=os.getenv("HANDLER", ".").strip() or ".",
            logger_id=logger_id,
            bot_token=os.getenv("BOT_TOKEN", "").strip() or None,
            bot_username=os.getenv("BOT_USERNAME", "").strip() or None,
            pm_permit=os.getenv("PM_PERMIT", "ENABLE").strip().upper() != "DISABLE",
            sudo_users=sudo_users,
            mongo_db_url=os.getenv("MONGO_DB_URL", "").strip() or None,
            database_url=os.getenv("DATABASE_URL", "").strip() or None,
        )
