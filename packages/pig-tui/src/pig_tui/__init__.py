"""Terminal UI library with rich formatting."""

from .chat import ChatUI
from .console import Console
from .layout import LayoutManager, Overlay, StatusLine
from .progress import Progress, Spinner
from .prompt import InteractivePrompt, Prompt
from .theme import Theme

try:
    from .advanced import (
        AutoCompleter,
        FileCompleter,
        InteractiveTable,
        MultiSelect,
        PyCodeCompleter,
        prompt_with_autocomplete,
    )
except ModuleNotFoundError:
    # Optional dependency (prompt_toolkit) may be absent in minimal environments.
    # Keep base UI imports working; raise a helpful error only when advanced APIs are used.
    def _missing_advanced(*args, **kwargs):
        raise ModuleNotFoundError(
            "Advanced TUI features require prompt_toolkit. Install with: pip install prompt-toolkit"
        )

    AutoCompleter = _missing_advanced
    FileCompleter = _missing_advanced
    InteractiveTable = _missing_advanced
    MultiSelect = _missing_advanced
    PyCodeCompleter = _missing_advanced
    prompt_with_autocomplete = _missing_advanced

__version__ = "0.0.1"

__all__ = [
    "ChatUI",
    "Console",
    "Prompt",
    "InteractivePrompt",
    "Progress",
    "Spinner",
    "Theme",
    "AutoCompleter",
    "FileCompleter",
    "PyCodeCompleter",
    "MultiSelect",
    "InteractiveTable",
    "prompt_with_autocomplete",
    "LayoutManager",
    "StatusLine",
    "Overlay",
]
