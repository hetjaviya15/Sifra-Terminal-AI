"""
features/memory.py - Long-term memory feature for SIFRA.

Provides helpers to extract memorable facts from AI replies,
and functions that back the /memory and /forget commands.

Design philosophy
─────────────────
We do NOT auto-save every message.  Instead, SIFRA's reply may
contain a special tag block like:

  [REMEMBER key: value]

The AI engine is instructed (via a memory-extraction prompt) to emit
these tags only when the user explicitly shares a piece of info worth
remembering (name, location, project, preference, etc.).

The parse_and_store_memories() function scans each reply for those
tags and writes them to the DB automatically.
"""

import re
from rich.table import Table
from rich.console import Console

from database.database import (
    save_memory,
    get_all_memories,
    delete_memory,
    clear_all_memories,
)
from ui.terminal_ui import print_success, print_error, print_info, print_divider

console = Console()

# ── Regex to match [REMEMBER key: value] tags in AI output ──────────────────
_REMEMBER_PATTERN = re.compile(
    r"\[REMEMBER\s+([^:\]]+?)\s*:\s*([^\]]+?)\]",
    re.IGNORECASE,
)


def parse_and_store_memories(text: str) -> str:
    """
    Scan `text` for [REMEMBER key: value] tags.
    Save each found memory to the DB and return the text
    with all such tags stripped out (so they don't appear in the UI).

    Args:
        text: Raw assistant reply string.

    Returns:
        Cleaned reply without the memory tags.
    """
    matches = _REMEMBER_PATTERN.findall(text)
    for key, value in matches:
        save_memory(key.strip(), value.strip())

    # Remove the tags from the visible reply
    cleaned = _REMEMBER_PATTERN.sub("", text).strip()
    return cleaned


def get_memory_injection_note() -> str:
    """
    Return a short instruction snippet to append to the system prompt
    so the AI knows how to emit memory tags.
    """
    return (
        "\n\n[Memory instruction]\n"
        "If the user shares a personal fact worth remembering "
        "(like their name, location, project name, programming language, "
        "or preference), embed a tag like:\n"
        "[REMEMBER key: value]\n"
        "Only do this for genuinely useful facts, not for every message.\n"
        "The tag will be stripped from your visible reply automatically.\n"
    )


# ════════════════════════════════════════════════════════════════════════════
# /memory command handler
# ════════════════════════════════════════════════════════════════════════════

def show_memories() -> None:
    """Display all saved memories in a Rich table."""
    memories = get_all_memories()

    print_divider("Memory")

    if not memories:
        print_info("No memories saved yet. Chat with SIFRA and she'll remember important things.")
        return

    table = Table(
        show_header=True,
        header_style="bold magenta",
        border_style="dim magenta",
        padding=(0, 1),
    )
    table.add_column("#",        style="dim",          width=4)
    table.add_column("Key",      style="bold cyan",    min_width=16)
    table.add_column("Value",    style="white",        min_width=24)
    table.add_column("Saved At", style="dim",          min_width=20)

    for idx, mem in enumerate(memories, start=1):
        table.add_row(
            str(idx),
            mem["memory_key"],
            mem["memory_value"],
            mem["created_at"][:16],   # Trim to YYYY-MM-DD HH:MM
        )

    console.print(table)
    console.print()


# ════════════════════════════════════════════════════════════════════════════
# /forget command handler
# ════════════════════════════════════════════════════════════════════════════

def forget_memory(key: str) -> None:
    """
    Delete a memory by its key, or all memories if 'all' is passed.

    Args:
        key: The memory key to delete, or 'all' to delete everything.
    """
    cleaned_key = key.strip().lower()
    if not cleaned_key:
        print_error("Please provide a memory key to forget. Example: /forget name (or /forget all)")
        return

    if cleaned_key in ("all", "*"):
        count = clear_all_memories()
        print_success(f"All {count} memories have been cleared.")
        return

    if delete_memory(cleaned_key):
        print_success(f'Memory "{key}" has been forgotten.')
    else:
        print_error(f'No memory found with key "{key}".')
