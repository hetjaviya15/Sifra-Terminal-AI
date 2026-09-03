"""
ui/banner.py - SIFRA startup banner and branding elements.

All visual branding (ASCII art, version string, taglines) lives here
so it's easy to customise without touching business logic.
"""

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from config import APP_VERSION, APP_DESCRIPTION

console = Console()


def print_banner() -> None:
    """Print the main SIFRA startup banner."""

    # Futuristic ASCII art logo
    art = r"""
 ______     __     ______   ______     ______    
/\  ___\   /\ \   /\  ___\ /\  == \   /\  __ \   
\ \___  \  \ \ \  \ \  __\ \ \  __<   \ \  __ \  
 \/\_____\  \ \_\  \ \_\    \ \_\ \_\  \ \_\ \_\ 
  \/_____/   \/_/   \/_/     \/_/ /_/   \/_/\/_/ 
"""

    tagline = f"✦  {APP_DESCRIPTION}  ✦"
    version_str = f"v{APP_VERSION}"

    content = Text(justify="center")
    content.append(art, style="bold magenta")
    content.append("\n")
    content.append(tagline, style="bold cyan")
    content.append("\n")
    content.append(version_str, style="dim cyan")
    content.append("\n")

    panel = Panel(
        Align.center(content),
        border_style="bright_magenta",
        padding=(0, 4),
        expand=False,
    )

    console.print()
    console.print(Align.center(panel))
    console.print()


def print_startup_status(message: str, style: str = "dim cyan") -> None:
    """Print a single-line startup status message."""
    console.print(f"  [dim]▸[/dim] [{style}]{message}[/{style}]")


def print_online_message() -> None:
    """Display SIFRA's greeting after startup completes."""
    console.print()
    console.print(
        Panel(
            "[bold magenta]SIFRA[/bold magenta] [white]is online.[/white]  "
            "[dim]Type your message or [bold cyan]/help[/bold cyan] to see commands.[/dim]",
            border_style="magenta",
            padding=(0, 2),
        )
    )
    console.print()
