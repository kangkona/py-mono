"""Terminal UI library with rich formatting."""

from .chat import ChatUI
from .console import Console
from .prompt import Prompt
from .progress import Progress, Spinner
from .theme import Theme

__version__ = "0.0.1"

__all__ = [
    "ChatUI",
    "Console",
    "Prompt",
    "Progress",
    "Spinner",
    "Theme",
]
