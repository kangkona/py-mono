"""Built-in tools for coding agent."""

import os
import subprocess
from pathlib import Path
from typing import Optional

from py_agent_core import tool


class FileTools:
    """File operation tools."""

    def __init__(self, workspace: str = "."):
        """Initialize file tools.

        Args:
            workspace: Workspace directory
        """
        self.workspace = Path(workspace).resolve()

    def _resolve_path(self, path: str) -> Path:
        """Resolve path within workspace."""
        full_path = (self.workspace / path).resolve()
        if not str(full_path).startswith(str(self.workspace)):
            raise ValueError(f"Path {path} is outside workspace")
        return full_path

    @tool(description="Read contents of a file")
    def read_file(self, path: str) -> str:
        """Read file contents.

        Args:
            path: File path relative to workspace

        Returns:
            File contents
        """
        file_path = self._resolve_path(path)
        if not file_path.exists():
            return f"Error: File {path} does not exist"
        return file_path.read_text()

    @tool(description="Write content to a file")
    def write_file(self, path: str, content: str) -> str:
        """Write content to file.

        Args:
            path: File path relative to workspace
            content: Content to write

        Returns:
            Success message
        """
        file_path = self._resolve_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return f"Successfully wrote to {path}"

    @tool(description="List files in a directory")
    def list_files(self, directory: str = ".") -> str:
        """List files in directory.

        Args:
            directory: Directory path

        Returns:
            List of files
        """
        dir_path = self._resolve_path(directory)
        if not dir_path.exists():
            return f"Error: Directory {directory} does not exist"
        
        files = []
        for item in sorted(dir_path.iterdir()):
            if item.is_file():
                files.append(f"  📄 {item.name}")
            elif item.is_dir():
                files.append(f"  📁 {item.name}/")
        
        return "\n".join(files) if files else "Empty directory"

    @tool(description="Check if file exists")
    def file_exists(self, path: str) -> bool:
        """Check if file exists.

        Args:
            path: File path

        Returns:
            True if exists
        """
        return self._resolve_path(path).exists()


class CodeTools:
    """Code generation and analysis tools."""

    @tool(description="Generate code from description")
    def generate_code(self, description: str, language: str = "python") -> str:
        """Generate code from natural language description.

        Args:
            description: What the code should do
            language: Programming language

        Returns:
            Generated code
        """
        # This is a placeholder - actual implementation would use LLM
        return f"# Generated {language} code for: {description}\n# TODO: Implement"

    @tool(description="Explain what code does")
    def explain_code(self, code: str) -> str:
        """Explain what code does.

        Args:
            code: Code to explain

        Returns:
            Explanation
        """
        # Placeholder
        return f"This code appears to be {len(code.split())} lines long."

    @tool(description="Add type hints to Python code")
    def add_type_hints(self, code: str) -> str:
        """Add type hints to Python code.

        Args:
            code: Python code

        Returns:
            Code with type hints
        """
        # Placeholder
        return f"# Type hints added:\n{code}"


class ShellTools:
    """Shell command execution tools."""

    @tool(description="Execute a shell command")
    def run_command(self, command: str, cwd: Optional[str] = None) -> str:
        """Execute shell command safely.

        Args:
            command: Command to execute
            cwd: Working directory

        Returns:
            Command output
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"
            return output
        except subprocess.TimeoutExpired:
            return "Error: Command timed out"
        except Exception as e:
            return f"Error: {e}"

    @tool(description="Get git status")
    def git_status(self) -> str:
        """Get git repository status.

        Returns:
            Git status output
        """
        return self.run_command("git status --short")

    @tool(description="Get git diff")
    def git_diff(self, path: Optional[str] = None) -> str:
        """Get git diff.

        Args:
            path: Optional path to diff

        Returns:
            Git diff output
        """
        cmd = f"git diff {path}" if path else "git diff"
        return self.run_command(cmd)
