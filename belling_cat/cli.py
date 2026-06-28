"""CLI interface for Belling Cat."""

from collections.abc import Callable

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from yachalk import chalk


def display_banner(console: Console) -> None:
    """Display the Belling Cat ASCII art banner."""
    banner_text = Text("Belling Cat", style="bold cyan", justify="center")
    panel = Panel(banner_text, border_style="cyan")
    console.print(panel)


def parse_command(user_input: str) -> dict[str, str]:
    """Parse user command input and extract command and arguments.

    Args:
        user_input: Raw user input string

    Returns:
        Dictionary with 'command' and 'args' keys
    """
    user_input = user_input.strip()

    if user_input.startswith("/investigate "):
        return {"command": "investigate", "args": user_input[13:].strip()}

    if user_input.startswith("/save "):
        return {"command": "save", "args": user_input[6:].strip()}

    return {"command": "unknown", "args": ""}


def format_error_message(user_input: str) -> str:
    """Format a helpful error message for invalid commands.

    Args:
        user_input: The invalid user input

    Returns:
        Error message string with usage guidance
    """
    return (
        f"Unknown command: {user_input}\n\n"
        "Available commands:\n"
        "  /investigate <claim>  - Investigate a claim using OSINT techniques\n"
        "  /save <report-name>   - Save the current investigation report"
    )


def style_prompt(prompt_text: str) -> str:
    """Style a prompt string using Yachalk for terminal colors.

    Args:
        prompt_text: Plain prompt text

    Returns:
        Styled prompt string with Yachalk colors
    """
    return chalk.cyan(f"{prompt_text}: ")


class CommandRouter:
    """Routes parsed commands to registered handlers."""

    def __init__(self) -> None:
        """Initialize the command router."""
        self._handlers: dict[str, Callable[[str], str]] = {}

    def register(self, command: str, handler: Callable[[str], str]) -> None:
        """Register a handler for a command.

        Args:
            command: Command name (without leading slash)
            handler: Callable that takes args string and returns result
        """
        self._handlers[command] = handler

    def dispatch(self, user_input: str) -> str:
        """Parse and dispatch a command to its handler.

        Args:
            user_input: Raw user input string

        Returns:
            Handler result or error message
        """
        parsed = parse_command(user_input)
        command = parsed["command"]
        args = parsed["args"]

        if command == "unknown":
            return format_error_message(user_input)

        if command in self._handlers:
            return self._handlers[command](args)

        return format_error_message(user_input)
