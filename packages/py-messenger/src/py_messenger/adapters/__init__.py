"""Platform adapters."""

from .slack import SlackAdapter
from .discord import DiscordAdapter
from .telegram import TelegramAdapter

__all__ = [
    "SlackAdapter",
    "DiscordAdapter",
    "TelegramAdapter",
]
