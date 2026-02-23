"""Coding agent with file operations and code generation."""

from pathlib import Path
from typing import Optional

from py_ai import LLM
from py_agent_core import Agent
from py_tui import ChatUI

from .tools import FileTools, CodeTools, ShellTools


class CodingAgent:
    """Interactive coding agent with file and code tools."""

    def __init__(
        self,
        llm: Optional[LLM] = None,
        workspace: str = ".",
        verbose: bool = True,
    ):
        """Initialize coding agent.

        Args:
            llm: LLM client
            workspace: Working directory
            verbose: Enable verbose output
        """
        self.workspace = Path(workspace).resolve()
        self.llm = llm or LLM()
        self.verbose = verbose

        # Initialize tools
        file_tools = FileTools(str(self.workspace))
        code_tools = CodeTools()
        shell_tools = ShellTools()

        # Get all tool methods
        tools = []
        for tool_class in [file_tools, code_tools, shell_tools]:
            for attr_name in dir(tool_class):
                attr = getattr(tool_class, attr_name)
                if hasattr(attr, "execute"):  # Check if it's a Tool
                    tools.append(attr)

        # Create agent
        self.agent = Agent(
            name="CodingAgent",
            llm=self.llm,
            tools=tools,
            system_prompt=self._get_system_prompt(),
            verbose=verbose,
        )

        # Create UI
        self.ui = ChatUI(title="Coding Agent", show_timestamps=False)

    def _get_system_prompt(self) -> str:
        """Get system prompt for coding agent."""
        return f"""You are an expert coding assistant with access to file operations and code generation tools.

Workspace: {self.workspace}

You can:
- Read and write files
- Generate and modify code
- Execute shell commands
- Analyze and explain code

Be helpful, precise, and always confirm destructive operations.
When generating code, provide clean, well-documented, production-ready code.
"""

    def run_interactive(self) -> None:
        """Run interactive chat session."""
        self.ui.system(f"Workspace: {self.workspace}")
        self.ui.separator()

        try:
            while True:
                # Get user input
                from py_tui import Prompt
                prompt = Prompt()
                user_input = prompt.ask("\n[cyan]You[/]")

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    self._handle_command(user_input)
                    continue

                # Display user message
                self.ui.user(user_input)

                # Get agent response
                response = self.agent.run(user_input)

                # Display response
                self.ui.assistant(response.content)

        except KeyboardInterrupt:
            self.ui.system("\nGoodbye!")
        except EOFError:
            self.ui.system("\nGoodbye!")

    def _handle_command(self, command: str) -> None:
        """Handle slash commands.

        Args:
            command: Command string
        """
        cmd = command.lower().strip()

        if cmd == "/exit" or cmd == "/quit":
            raise KeyboardInterrupt()

        elif cmd == "/clear":
            self.agent.clear_history()
            self.ui.clear()
            self.ui.system("Conversation cleared")

        elif cmd == "/help":
            self.ui.panel("""
**Available Commands:**

/help       - Show this help
/exit       - Exit the agent
/clear      - Clear conversation
/files      - List files in workspace
/status     - Show agent status

**Tools Available:**
- read_file, write_file, list_files
- generate_code, explain_code
- run_command, git_status, git_diff
            """, title="Help")

        elif cmd == "/files":
            files = FileTools(str(self.workspace)).list_files()
            self.ui.panel(files, title="Files")

        elif cmd == "/status":
            self.ui.panel(f"""
**Agent Status**

Model: {self.agent.llm.config.model}
Workspace: {self.workspace}
Messages: {len(self.agent.history)}
Tools: {len(self.agent.registry)}
            """, title="Status")

        else:
            self.ui.error(f"Unknown command: {command}")

    def run_once(self, message: str) -> str:
        """Run agent with a single message.

        Args:
            message: User message

        Returns:
            Agent response
        """
        response = self.agent.run(message)
        return response.content
