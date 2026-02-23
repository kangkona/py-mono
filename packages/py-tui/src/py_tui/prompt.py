"""Interactive prompts."""

from typing import Optional
from rich.console import Console
from rich.prompt import Prompt as RichPrompt, Confirm


class Prompt:
    """Interactive prompt for user input."""

    def __init__(self):
        """Initialize prompt."""
        self.console = Console()

    def ask(
        self,
        question: str,
        default: Optional[str] = None,
        password: bool = False,
        choices: Optional[list[str]] = None,
    ) -> str:
        """Ask for user input.

        Args:
            question: Question to ask
            default: Default value
            password: Hide input (for passwords)
            choices: List of valid choices

        Returns:
            User input
        """
        return RichPrompt.ask(
            question,
            default=default,
            password=password,
            choices=choices,
            console=self.console,
        )

    def confirm(self, question: str, default: bool = False) -> bool:
        """Ask for yes/no confirmation.

        Args:
            question: Question to ask
            default: Default answer

        Returns:
            User confirmation
        """
        return Confirm.ask(question, default=default, console=self.console)

    def choice(self, question: str, choices: list[str]) -> str:
        """Ask user to choose from options.

        Args:
            question: Question to ask
            choices: List of choices

        Returns:
            Selected choice
        """
        return RichPrompt.ask(question, choices=choices, console=self.console)
