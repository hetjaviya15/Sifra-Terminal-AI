"""
features/commands.py - Slash-command dispatcher for SIFRA.

All /commands are registered here in the COMMAND_REGISTRY dict.
To add a new command, just add an entry — no changes needed elsewhere.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from config import APP_NAME, APP_VERSION, APP_DESCRIPTION
from ui.terminal_ui import (
    print_divider, print_info, print_system, clear_screen
)
from features.memory import show_memories, forget_memory
from features.history import show_history

console = Console()


# ════════════════════════════════════════════════════════════════════════════
# Individual command handlers
# ════════════════════════════════════════════════════════════════════════════

def cmd_help(_args: str = "") -> None:
    """Display all available slash commands."""
    print_divider("Available Commands")

    table = Table(
        show_header=False,
        border_style="dim magenta",
        padding=(0, 2),
        expand=False,
    )
    table.add_column("Command",     style="bold cyan",  min_width=14)
    table.add_column("Description", style="white")

    commands_info = [
        ("/help",       "Show this command list"),
        ("/new",        "Start a fresh conversation (clears context)"),
        ("/history",    "Browse previous conversations"),
        ("/memory",     "View all saved long-term memories"),
        ("/forget",     "Delete a memory  —  usage: /forget <key>"),
        ("/clear",      "Clear the terminal screen"),
        ("/about",      "About SIFRA"),
        ("/exit",       "Exit SIFRA gracefully"),
    ]

    for cmd, desc in commands_info:
        table.add_row(cmd, desc)

    console.print(table)
    console.print()


def cmd_about(_args: str = "") -> None:
    """Display information about the SIFRA application."""
    content = Text(justify="center")
    content.append(f"{APP_NAME}\n", style="bold magenta")
    content.append(f"{APP_DESCRIPTION}\n", style="cyan")
    content.append(f"Version {APP_VERSION}\n\n", style="dim cyan")
    content.append(
        "SIFRA is an AI terminal assistant built with Python, Rich,\n"
        "prompt_toolkit, SQLite, and an OpenAI-compatible AI backend.\n\n",
        style="white",
    )
    content.append(
        "Created as a university Application Development project.\n",
        style="dim",
    )

    console.print()
    console.print(
        Panel(
            content,
            border_style="magenta",
            padding=(1, 4),
            expand=False,
        )
    )
    console.print()


def cmd_clear(_args: str = "") -> None:
    """Clear the terminal screen."""
    clear_screen()
    print_system("Screen cleared.")


def cmd_history(_args: str = "") -> None:
    """Show recent chat history."""
    show_history()


def cmd_memory(_args: str = "") -> None:
    """Show saved long-term memories."""
    show_memories()


def cmd_forget(args: str = "") -> None:
    """Delete a saved memory by key.  Usage: /forget <key>"""
    forget_memory(args.strip())


def cmd_new(_args: str = "", conversation=None) -> None:
    """Start a new conversation session."""
    if conversation:
        conversation.reset()
    print_system("New conversation started. Context cleared.")


def cmd_exit(_args: str = "") -> None:
    """Exit the SIFRA application."""
    console.print()
    console.print(
        Panel(
            "[bold magenta]SIFRA[/bold magenta] [white]signing off.[/white]  "
            "[dim]See you next time! 👋[/dim]",
            border_style="magenta",
            padding=(0, 2),
        )
    )
    console.print()


# ════════════════════════════════════════════════════════════════════════════
from typing import Any, Callable

COMMAND_REGISTRY: dict[str, Callable[..., Any]] = {
    "/help":    cmd_help,
    "/about":   cmd_about,
    "/clear":   cmd_clear,
    "/history": cmd_history,
    "/memory":  cmd_memory,
    "/forget":  cmd_forget,
    "/new":     cmd_new,
    "/exit":    cmd_exit,
}


def dispatch(raw_input: str, conversation=None) -> bool:
    """
    Parse and dispatch a slash command.

    Args:
        raw_input:    The full string the user typed (e.g. "/forget name").
        conversation: The active Conversation instance (passed to /new).

    Returns:
        True  → command was handled (stop processing the input as a chat msg).
        False → not a known command (treat as normal chat message).
    """
    stripped = raw_input.strip()
    if not stripped.startswith("/"):
        return False

    # Split into command and optional arguments
    parts = stripped.split(maxsplit=1)
    cmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if cmd not in COMMAND_REGISTRY:
        print_info(f'Unknown command "{cmd}". Type /help to see available commands.')
        return True   # It was a command attempt; don't pass to AI

    handler = COMMAND_REGISTRY[cmd]

    # /new and /forget need extra args
    if cmd == "/new":
        handler(args, conversation=conversation)
    elif cmd == "/forget":
        handler(args)
    else:
        handler(args)

    return True
