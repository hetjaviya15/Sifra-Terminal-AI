"""
ui/terminal_ui.py - All Rich-based rendering helpers for SIFRA.

This module owns:
  - Printing user / assistant message bubbles
  - The "SIFRA is thinking…" spinner
  - System / error / success messages
  - Dividers and spacing utilities
"""


from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from rich.live import Live
from rich.rule import Rule
from config import (
    COLOR_USER, COLOR_SIFRA, COLOR_SYSTEM,
    COLOR_ERROR, COLOR_SUCCESS, COLOR_DIM,
)

console = Console()


# ════════════════════════════════════════════════════════════════════════════
# Message Bubbles
# ════════════════════════════════════════════════════════════════════════════

def print_user_message(message: str) -> None:
    """
    Render the user's message in a clean, right-leaning style.
    We keep it minimal — just a labelled block.
    """
    console.print()
    console.print(f"  [{COLOR_USER}]You[/{COLOR_USER}]")
    console.print(
        Panel(
            Text(message, style="white"),
            border_style="cyan",
            padding=(0, 2),
            expand=False,
        )
    )


def print_sifra_message(message: str) -> None:
    """
    Render SIFRA's reply with Markdown support inside a panel.
    Rich's Markdown renderer handles code blocks, bold, lists, etc.
    """
    console.print()
    console.print(f"  [{COLOR_SIFRA}]SIFRA[/{COLOR_SIFRA}]")
    console.print(
        Panel(
            Markdown(message),
            border_style="magenta",
            padding=(0, 2),
        )
    )
    console.print()


# ════════════════════════════════════════════════════════════════════════════
# Thinking Spinner
# ════════════════════════════════════════════════════════════════════════════

class ThinkingSpinner:
    """
    Context manager that shows a "SIFRA is thinking…" spinner.

    Usage:
        with ThinkingSpinner():
            reply = conversation.send(user_input)
    """

    def __enter__(self):
        self._live = Live(
            Spinner("dots", text="[bold magenta]SIFRA is thinking…[/bold magenta]"),
            console=console,
            refresh_per_second=12,
            transient=True,   # Clears itself when done
        )
        self._live.__enter__()
        return self

    def __exit__(self, *args):
        self._live.__exit__(*args)


# ════════════════════════════════════════════════════════════════════════════
# System / Status Messages
# ════════════════════════════════════════════════════════════════════════════

def print_system(message: str) -> None:
    """Display a neutral system info line."""
    console.print(f"\n  [{COLOR_SYSTEM}]⚙  {message}[/{COLOR_SYSTEM}]\n")


def print_error(message: str) -> None:
    """Display a formatted error panel."""
    console.print()
    console.print(
        Panel(
            f"[{COLOR_ERROR}]{message}[/{COLOR_ERROR}]",
            title="[bold red]Error[/bold red]",
            border_style="red",
            padding=(0, 2),
        )
    )
    console.print()


def print_success(message: str) -> None:
    """Display a short success message."""
    console.print(f"\n  [{COLOR_SUCCESS}]✔  {message}[/{COLOR_SUCCESS}]\n")


def print_info(message: str) -> None:
    """Display a dim informational note."""
    console.print(f"  [{COLOR_DIM}]{message}[/{COLOR_DIM}]")


# ════════════════════════════════════════════════════════════════════════════
# Dividers / Spacing
# ════════════════════════════════════════════════════════════════════════════

def print_divider(label: str = "") -> None:
    """Print a horizontal rule, optionally with a centred label."""
    console.print(Rule(label, style="dim magenta"))


def clear_screen() -> None:
    """Clear the terminal using Rich (cross-platform)."""
    console.clear()
