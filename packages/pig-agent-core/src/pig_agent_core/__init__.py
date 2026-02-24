"""Agent runtime with tool calling and state management."""

from .agent import Agent
from .auth import AuthManager, OAuthFlow, OAuthProvider, TokenInfo
from .context import ContextManager
from .export import SessionExporter
from .extensions import ExtensionAPI, ExtensionManager
from .message_queue import MessageQueue, MessageType, QueuedMessage
from .models import AgentState, ToolCall, ToolResult
from .output_modes import JSONOutputMode, OutputModeManager, RPCMode
from .prompts import PromptManager, PromptTemplate
from .registry import ToolRegistry
from .session import Session, SessionEntry, SessionTree
from .session_manager import SessionInfo, SessionManager
from .share import GistSharer
from .skills import Skill, SkillManager
from .tools import Tool, tool

__version__ = "0.0.1"

__all__ = [
    "Agent",
    "Tool",
    "tool",
    "AgentState",
    "ToolCall",
    "ToolResult",
    "ToolRegistry",
    "Session",
    "SessionTree",
    "SessionEntry",
    "SessionManager",
    "SessionInfo",
    "ExtensionAPI",
    "ExtensionManager",
    "Skill",
    "SkillManager",
    "ContextManager",
    "PromptTemplate",
    "PromptManager",
    "MessageQueue",
    "MessageType",
    "QueuedMessage",
    "SessionExporter",
    "GistSharer",
    "JSONOutputMode",
    "RPCMode",
    "OutputModeManager",
    "AuthManager",
    "OAuthProvider",
    "OAuthFlow",
    "TokenInfo",
]
