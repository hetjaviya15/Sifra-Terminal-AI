"""
features/history.py - Chat history display for the /history command.

Fetches recent conversations from the database and renders them
in a clean, readable Rich layout.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from database.database import get_recent_conversations, get_messages_for_conversation
from ui.terminal_ui import print_divider, print_info

console = Console()


def show_history(limit: int = 8) -> None:
    """
    Display the most recent conversations with a summary list,
    then let the user pick one to expand.

    Args:
        limit: How many past conversations to show in the list.
    """
    print_divider("Chat History")

    conversations = get_recent_conversations(limit=limit)

    if not conversations:
        print_info("No previous conversations found. Start chatting!")
        console.print()
        return

    # ── Conversation summary table ───────────────────────────────────────────
    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="dim magenta",
        padding=(0, 1),
    )
    table.add_column("#",           style="dim",       width=4)
    table.add_column("Date / Time", style="cyan",      min_width=18)
    table.add_column("Messages",    style="white",     min_width=10, justify="right")
    table.add_column("ID",          style="dim",       min_width=6)

    for idx, conv in enumerate(conversations, start=1):
        table.add_row(
            str(idx),
            conv["created_at"][:16],
            str(conv["message_count"]),
            str(conv["id"]),
        )

    console.print(table)
    console.print()

    # ── Prompt user to expand a conversation ────────────────────────────────
    console.print(
        "  [dim]Enter a conversation [bold cyan]#[/bold cyan] to read it, "
        "or press [bold cyan]Enter[/bold cyan] to go back.[/dim]"
    )

    try:
        choice = console.input("  [bold cyan]▸[/bold cyan] ").strip()
    except (EOFError, KeyboardInterrupt):
        console.print()
        return

    if not choice:
        return

    try:
        idx = int(choice) - 1
        if not (0 <= idx < len(conversations)):
            raise ValueError
        conv_id = conversations[idx]["id"]
        _show_conversation_detail(conv_id)
    except ValueError:
        print_info("Invalid selection.")


def _show_conversation_detail(conversation_id: int) -> None:
    """
    Render all messages in a single conversation.

    Args:
        conversation_id: DB primary key of the conversation.
    """
    messages = get_messages_for_conversation(conversation_id)

    if not messages:
        print_info("This conversation has no messages.")
        return

    print_divider(f"Conversation #{conversation_id}")

    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        timestamp = msg["timestamp"][:16]

        if role == "user":
            label = Text(f"You  [{timestamp}]", style="bold cyan")
            console.print()
            console.print(f"  {label}")
            console.print(
                Panel(
                    Text(content, style="white"),
                    border_style="cyan",
                    padding=(0, 2),
                    expand=False,
                )
            )
        else:
            label = Text(f"SIFRA  [{timestamp}]", style="bold magenta")
            console.print()
            console.print(f"  {label}")
            console.print(
                Panel(
                    Markdown(content),
                    border_style="magenta",
                    padding=(0, 2),
                )
            )

    console.print()
    print_divider()
