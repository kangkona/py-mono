"""Coding agent with file operations and code generation."""

from pathlib import Path
from typing import Optional

from py_ai import LLM
from py_agent_core import Agent, Session, ExtensionManager, SkillManager, ContextManager, PromptManager
from py_tui import ChatUI

from .tools import FileTools, CodeTools, ShellTools


class CodingAgent:
    """Interactive coding agent with file and code tools."""

    def __init__(
        self,
        llm: Optional[LLM] = None,
        workspace: str = ".",
        verbose: bool = True,
        session_name: Optional[str] = None,
        session_path: Optional[Path] = None,
        enable_extensions: bool = True,
        enable_skills: bool = True,
    ):
        """Initialize coding agent.

        Args:
            llm: LLM client
            workspace: Working directory
            verbose: Enable verbose output
            session_name: Session name for auto-save
            session_path: Path to load existing session
            enable_extensions: Enable extension system
            enable_skills: Enable skills system
        """
        self.workspace = Path(workspace).resolve()
        self.llm = llm or LLM()
        self.verbose = verbose

        # Initialize session
        if session_path and session_path.exists():
            self.session = Session.load(session_path)
            print(f"✓ Loaded session: {self.session.name}")
        else:
            self.session = Session(
                name=session_name or "coding-session",
                workspace=str(self.workspace),
                auto_save=True,
            )

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

        # Initialize extension manager
        self.extension_manager = None
        if enable_extensions:
            self.extension_manager = ExtensionManager(self.agent)
            self._load_extensions()

        # Initialize skill manager
        self.skill_manager = None
        if enable_skills:
            self.skill_manager = SkillManager()
            self.skill_manager.discover_skills([])
            if len(self.skill_manager) > 0:
                print(f"✓ Loaded {len(self.skill_manager)} skills")

        # Initialize context manager
        self.context_manager = ContextManager(self.workspace)

        # Initialize prompt manager
        self.prompt_manager = PromptManager()
        self.prompt_manager.discover_prompts([])
        if len(self.prompt_manager) > 0:
            print(f"✓ Loaded {len(self.prompt_manager)} prompt templates")

        # Create UI
        self.ui = ChatUI(title="Coding Agent", show_timestamps=False)

    def _load_extensions(self):
        """Load extensions from standard directories."""
        if not self.extension_manager:
            return

        # Standard extension paths
        ext_paths = [
            self.workspace / ".agents" / "extensions",
            self.workspace / ".pi" / "extensions",
            Path.home() / ".agents" / "extensions",
        ]

        for path in ext_paths:
            if path.exists():
                self.extension_manager.load_from_directory(path)

    def _get_system_prompt(self) -> str:
        """Get system prompt for coding agent."""
        # Default prompt
        default_prompt = f"""You are an expert coding assistant with access to file operations and code generation tools.

Workspace: {self.workspace}

You can:
- Read and write files
- Generate and modify code
- Execute shell commands
- Analyze and explain code

Be helpful, precise, and always confirm destructive operations.
When generating code, provide clean, well-documented, production-ready code.
"""

        # Build with context files
        prompt = self.context_manager.build_system_prompt(default_prompt)

        # Add skills information if available
        if self.skill_manager and len(self.skill_manager) > 0:
            skills_prompt = self.skill_manager.get_all_skills_prompt()
            prompt += f"\n\n{skills_prompt}"

        return prompt

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

        elif cmd.startswith("/tree"):
            self._show_tree()

        elif cmd.startswith("/fork"):
            parts = cmd.split(maxsplit=1)
            fork_name = parts[1] if len(parts) > 1 else None
            self._fork_session(fork_name)

        elif cmd.startswith("/compact"):
            parts = cmd.split(maxsplit=1)
            instructions = parts[1] if len(parts) > 1 else None
            self._compact_session(instructions)

        elif cmd.startswith("/session"):
            self._show_session_info()

        elif cmd.startswith("/skill:"):
            skill_name = cmd.split(":", 1)[1]
            self._invoke_skill(skill_name)

        elif cmd.startswith("/skills"):
            self._list_skills()

        elif cmd.startswith("/extensions"):
            self._list_extensions()

        elif cmd.startswith("/prompts"):
            self._list_prompts()

        elif cmd.startswith("/"):
            # Check if it's a prompt template
            template_name = cmd.lstrip("/").split()[0]
            if self.prompt_manager and template_name in self.prompt_manager:
                # Extract variables from rest of command
                args_str = cmd.split(maxsplit=1)[1] if " " in cmd else ""
                self._expand_prompt(template_name, args_str)
                return

        else:
            # Try extension commands
            if self.extension_manager:
                ext_cmd = cmd.lstrip("/").split()[0]
                cmd_args = cmd.split(maxsplit=1)[1] if " " in cmd else None
                try:
                    result = self.extension_manager.handle_command(ext_cmd, cmd_args)
                    self.ui.panel(str(result), title=f"/{ext_cmd}")
                    return
                except (ValueError, KeyError):
                    pass

            self.ui.error(f"Unknown command: {command}")

    def _show_tree(self):
        """Show session tree."""
        if not self.session:
            self.ui.error("No session loaded")
            return

        tree_text = "**Session Tree**\n\n"
        path = self.session.get_current_conversation()

        for i, entry in enumerate(path):
            indent = "  " * min(i, 5)
            preview = entry.content[:60].replace("\n", " ")
            tree_text += f"{indent}• [{entry.role}] {preview}...\n"

        tree_text += f"\nTotal entries: {len(self.session.tree.entries)}"
        tree_text += f"\nCurrent path: {len(path)}"
        self.ui.panel(tree_text, title="Session Tree")

    def _fork_session(self, fork_name: Optional[str]):
        """Fork current session."""
        if not self.session:
            self.ui.error("No session loaded")
            return

        conversation = self.session.get_current_conversation()
        if not conversation:
            self.ui.error("No messages to fork")
            return

        # Fork from last message
        name = fork_name or f"{self.session.name}-fork"
        fork = self.session.fork(conversation[-1].id, name)

        save_path = fork.save()
        self.ui.system(f"✓ Forked session: {name}")
        self.ui.system(f"  Copied {len(fork.tree.entries)} entries")
        self.ui.system(f"  Saved to: {save_path}")

    def _compact_session(self, instructions: Optional[str]):
        """Compact session messages."""
        if not self.session:
            self.ui.error("No session loaded")
            return

        before = len(self.session.tree.entries)
        compacted = self.session.compact(instructions)

        self.ui.system(f"✓ Compacted: {before} entries → {len(compacted)} entries")
        if instructions:
            self.ui.system(f"  Instructions: {instructions}")

    def _show_session_info(self):
        """Show session information."""
        if not self.session:
            self.ui.error("No session loaded")
            return

        info = self.session.get_info()
        info_text = f"""
**Session Information**

ID: {info['id'][:8]}...
Name: {info['name']}
Created: {info['created_at'][:19]}
Updated: {info['updated_at'][:19]}

Entries: {info['entries']}
Current path: {info['current_path_length']}
Branches: {info['branches']}

Tokens: {info['metadata'].get('tokens_used', 0)}
Cost: ${info['metadata'].get('cost', 0.0):.4f}
        """
        self.ui.panel(info_text, title="Session")

    def _invoke_skill(self, skill_name: str):
        """Invoke a skill."""
        if not self.skill_manager:
            self.ui.error("Skills not enabled")
            return

        skill = self.skill_manager.get_skill(skill_name)
        if not skill:
            self.ui.error(f"Skill '{skill_name}' not found")
            self.ui.system("Use /skills to see available skills")
            return

        # Show skill
        skill_prompt = skill.to_prompt()
        self.ui.panel(skill_prompt, title=f"Skill: {skill_name}")
        self.ui.system("Skill context loaded. Ask your question now.")

    def _list_skills(self):
        """List available skills."""
        if not self.skill_manager:
            self.ui.error("Skills not enabled")
            return

        if len(self.skill_manager) == 0:
            self.ui.system("No skills found")
            self.ui.system("Create skills in .agents/skills/skill-name/SKILL.md")
            return

        skills_text = "**Available Skills**\n\n"
        for skill in self.skill_manager.list_skills():
            skills_text += f"• **{skill.name}**\n"
            skills_text += f"  {skill.description}\n\n"

        skills_text += "Use `/skill:name` to invoke a skill."
        self.ui.panel(skills_text, title=f"Skills ({len(self.skill_manager)})")

    def _list_extensions(self):
        """List loaded extensions."""
        if not self.extension_manager:
            self.ui.error("Extensions not enabled")
            return

        if len(self.extension_manager.extensions) == 0:
            self.ui.system("No extensions loaded")
            self.ui.system("Place extensions in .agents/extensions/")
            return

        ext_text = "**Loaded Extensions**\n\n"
        for name in self.extension_manager.extensions.keys():
            ext_text += f"• {name}\n"

        # List custom commands
        commands = self.extension_manager.api.get_commands()
        if commands:
            ext_text += "\n**Custom Commands**:\n"
            for cmd in commands.keys():
                ext_text += f"• /{cmd}\n"

        # List registered tools count
        ext_text += f"\n**Tools**: {len(self.agent.registry)} total"

        self.ui.panel(ext_text, title=f"Extensions ({len(self.extension_manager.extensions)})")

    def _show_help(self):
        """Show comprehensive help."""
        help_text = """
**Built-in Commands:**

/help       - Show this help
/exit       - Exit agent
/clear      - Clear conversation
/status     - Agent status
/files      - List workspace files

**Session Management:**

/session    - Show session info
/tree       - Show conversation tree
/fork [name] - Fork session from current point
/compact [instructions] - Compact old messages

**Skills & Extensions:**

/skills     - List available skills
/skill:name - Invoke a skill
/extensions - List loaded extensions
/prompts    - List prompt templates
/template   - Expand a template

**Context Files:**

• AGENTS.md - Project instructions (auto-loaded)
• SYSTEM.md - Override system prompt
• APPEND_SYSTEM.md - Append to system prompt

**Features:**

• Sessions auto-save to .sessions/
• Extensions auto-load from .agents/extensions/
• Skills auto-discover from .agents/skills/
• Prompts auto-load from .agents/prompts/
• Use /tree to navigate conversation history
• Use /fork to create alternate branches
        """
        self.ui.panel(help_text, title="Help")

    def _list_prompts(self):
        """List available prompt templates."""
        if not self.prompt_manager or len(self.prompt_manager) == 0:
            self.ui.system("No prompts found")
            self.ui.system("Create prompts in .agents/prompts/*.md")
            return

        prompts_text = "**Available Prompt Templates**\n\n"
        for template in self.prompt_manager.list_templates():
            prompts_text += f"• **/{template.name}**\n"
            if template.variables:
                prompts_text += f"  Variables: {', '.join(template.variables)}\n"
            # Show first line as description
            first_line = template.content.split("\n")[0].strip("# ").strip()
            prompts_text += f"  {first_line}\n\n"

        prompts_text += "Use `/template_name` to expand a template."
        self.ui.panel(prompts_text, title=f"Prompts ({len(self.prompt_manager)})")

    def _expand_prompt(self, template_name: str, args: str):
        """Expand a prompt template.

        Args:
            template_name: Template name
            args: Arguments string (key=value format)
        """
        template = self.prompt_manager.get_template(template_name)
        if not template:
            self.ui.error(f"Template '{template_name}' not found")
            return

        # Parse arguments (simple key=value parsing)
        kwargs = {}
        if args:
            parts = args.split()
            for part in parts:
                if "=" in part:
                    key, value = part.split("=", 1)
                    kwargs[key] = value

        # Show template info
        if template.variables and not kwargs:
            vars_text = "**Template Variables**:\n\n"
            for var in template.variables:
                vars_text += f"• {var}\n"
            vars_text += f"\nUsage: /{template_name} {' '.join(f'{v}=value' for v in template.variables)}"
            self.ui.panel(vars_text, title=f"Template: {template_name}")
            return

        # Render template
        rendered = template.render(**kwargs)
        
        # Show rendered prompt
        self.ui.panel(rendered, title=f"Prompt: {template_name}")
        self.ui.system("Prompt loaded. Press Enter to send it, or modify it.")
        
        # In a real implementation, this would put the rendered text in the input buffer
        # For now, we just display it

    def _show_status(self):
        """Show comprehensive status."""
        status_text = f"""
**Agent Configuration**

Model: {self.agent.llm.config.model}
Provider: {self.agent.llm.config.provider}
Workspace: {self.workspace}

**Current State**

Messages in history: {len(self.agent.history)}
Tools available: {len(self.agent.registry)}
"""

        if self.session:
            info = self.session.get_info()
            status_text += f"""
**Session**

Name: {self.session.name}
Entries: {info['entries']}
Current path: {info['current_path_length']}
Branches: {info['branches']}
"""

        if self.skill_manager:
            status_text += f"\n**Skills**: {len(self.skill_manager)} loaded"

        if self.extension_manager:
            ext_count = len(self.extension_manager.extensions)
            cmd_count = len(self.extension_manager.api.get_commands())
            status_text += f"\n**Extensions**: {ext_count} loaded, {cmd_count} commands"

        if self.prompt_manager:
            status_text += f"\n**Prompts**: {len(self.prompt_manager)} loaded"

        # Show context files
        agents_md = self.context_manager.find_context_files("AGENTS.md")
        if agents_md:
            status_text += f"\n**Context**: {len(agents_md)} AGENTS.md files"

        self.ui.panel(status_text, title="Status")

    def run_once(self, message: str) -> str:
        """Run agent with a single message.

        Args:
            message: User message

        Returns:
            Agent response
        """
        response = self.agent.run(message)
        return response.content
