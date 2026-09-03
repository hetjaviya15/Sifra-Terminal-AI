"""
main.py - Entry point for SIFRA AI Terminal Assistant.

Run with:
    python main.py

This file wires together all modules:
  - Startup sequence (banner, DB init, AI engine)
  - The main input loop (prompt_toolkit)
  - Command dispatch and AI chat
  - Graceful shutdown
"""

import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console

# ── SIFRA modules ───────────────────────────────────────────────────────────
# from config import AI_API_KEY
from database.database import init_db
from core.ai_engine import AIEngine
from core.conversation import Conversation
from features.commands import dispatch, cmd_exit
from features.memory import parse_and_store_memories
from ui.banner import print_banner, print_startup_status, print_online_message
from ui.terminal_ui import (
    print_user_message,
    print_sifra_message,
    print_error,
    print_info,
    ThinkingSpinner,
)

console = Console()


# ════════════════════════════════════════════════════════════════════════════
# prompt_toolkit styling  —  makes the "You ▸" prompt look sharp
# ════════════════════════════════════════════════════════════════════════════

PROMPT_STYLE = Style.from_dict({
    "prompt":       "bold ansicyan",
    "prompt.arrow": "bold ansimagenta",
})


def build_prompt_session() -> PromptSession:
    """Create a prompt_toolkit session with history and custom style."""
    return PromptSession(
        history=InMemoryHistory(),
        style=PROMPT_STYLE,
        mouse_support=False,
        wrap_lines=True,
    )


# ════════════════════════════════════════════════════════════════════════════
# Startup sequence
# ════════════════════════════════════════════════════════════════════════════

def startup() -> tuple[AIEngine, Conversation]:
    """
    Run the startup sequence and return a ready AIEngine + Conversation.

    Steps:
      1. Print banner
      2. Initialise database
      3. Load AI engine
      4. Print online status

    Returns:
        (engine, conversation) tuple ready for the main loop.

    Raises:
        SystemExit on unrecoverable startup errors.
    """
    print_banner()

    # ── Database ──────────────────────────────────────────────────────────
    print_startup_status("Connecting to database…")
    try:
        init_db()
    except Exception as exc:
        console.print(f"\n[bold red]Database error:[/bold red] {exc}")
        sys.exit(1)

    # ── Memory ────────────────────────────────────────────────────────────
    print_startup_status("Loading memory…")

    # ── AI Engine ─────────────────────────────────────────────────────────
    print_startup_status("Initialising AI engine…")

    # if not AI_API_KEY:
    #     console.print(
    #         "\n[bold red]✘  AI_API_KEY is not set.[/bold red]\n"
    #         "  Create a [bold cyan].env[/bold cyan] file in the project root "
    #         "and add your key:\n\n"
    #         "    [dim]AI_API_KEY=your_api_key_here[/dim]\n\n"
    #         "  See [bold cyan].env.example[/bold cyan] for a template.\n"
    #     )
    #     sys.exit(1)

    try:
        engine = AIEngine()
    except ValueError as exc:
        console.print(f"\n[bold red]✘  {exc}[/bold red]\n")
        sys.exit(1)

    conversation = Conversation(engine)

    print_online_message()

    # SIFRA's opening greeting via AI
    print_startup_status("Preparing SIFRA…", style="dim magenta")
    try:
        with ThinkingSpinner():
            greeting = engine.chat([
                {
                    "role": "user",
                    "content": (
                        "Greet the user. You are just coming online. "
                        "Keep it short, warm and natural — one or two sentences max."
                    ),
                }
            ])
        print_sifra_message(greeting)
    except Exception:
        # Non-fatal — just skip the greeting
        print_sifra_message("Hello! I'm SIFRA. I'm online and ready to help. 👋")

    return engine, conversation


# ════════════════════════════════════════════════════════════════════════════
# Main chat loop
# ════════════════════════════════════════════════════════════════════════════

def run_chat_loop(conversation: Conversation) -> None:
    """
    The main REPL loop.

    Reads user input via prompt_toolkit, dispatches /commands,
    and sends chat messages to the AI engine.
    """
    session = build_prompt_session()

    while True:
        # ── Get user input ────────────────────────────────────────────────
        try:
            user_input = session.prompt(
                [
                    ("class:prompt",       "  You "),
                    ("class:prompt.arrow", "▸ "),
                ],
                style=PROMPT_STYLE,
            ).strip()
        except KeyboardInterrupt:
            # Ctrl+C — show a hint instead of crashing
            print_info("\n  [dim]Tip: type [bold cyan]/exit[/bold cyan] to quit SIFRA gracefully.[/dim]")
            continue
        except EOFError:
            # Ctrl+D — treat as /exit
            break

        if not user_input:
            continue

        # ── /command dispatch ─────────────────────────────────────────────
        if user_input.startswith("/"):
            # Check for exit before dispatching
            if user_input.lower() in ("/exit", "/quit", "/q"):
                cmd_exit()
                break

            dispatch(user_input, conversation=conversation)
            continue

        # ── Chat message → AI ─────────────────────────────────────────────
        print_user_message(user_input)

        try:
            with ThinkingSpinner():
                raw_reply = conversation.send(user_input)

            # Strip any [REMEMBER ...] memory tags from the visible reply
            visible_reply = parse_and_store_memories(raw_reply)

            print_sifra_message(visible_reply)

        except PermissionError as exc:
            print_error(str(exc))
        except ConnectionError as exc:
            print_error(
                f"I'm having trouble reaching my AI service right now.\n"
                f"Please check your connection and try again.\n\n[dim]{exc}[/dim]"
            )
        except RuntimeError as exc:
            print_error(str(exc))
        except Exception as exc:
            print_error(f"Something unexpected went wrong: {exc}")


# ════════════════════════════════════════════════════════════════════════════
# Entry point
# ════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Bootstrap and run SIFRA."""
    try:
        _engine, conversation = startup()
        run_chat_loop(conversation)
    except KeyboardInterrupt:
        # Top-level Ctrl+C during startup
        cmd_exit()
    finally:
        console.print()


if __name__ == "__main__":
    main()
