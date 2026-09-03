"""
config.py - Central configuration for SIFRA
All environment variables and app settings are loaded here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─────────────────────────────────────────────
# AI Engine Configuration
# ─────────────────────────────────────────────

AI_API_KEY: str = os.getenv("AI_API_KEY", "")
AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4o-mini")
AI_BASE_URL: str = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")

# Maximum number of messages to keep in context window per session
MAX_CONTEXT_MESSAGES: int = int(os.getenv("MAX_CONTEXT_MESSAGES", "30"))

# ─────────────────────────────────────────────
# App Info
# ─────────────────────────────────────────────

APP_NAME: str = "SIFRA"
APP_VERSION: str = "1.0.0"
APP_DESCRIPTION: str = "Your Intelligent Terminal Companion"

# ─────────────────────────────────────────────
# Database Configuration
# ─────────────────────────────────────────────

import pathlib

# Database lives inside the sifra/database/ folder
BASE_DIR = pathlib.Path(__file__).parent
DB_PATH: str = str(BASE_DIR / "database" / "sifra.db")

# ─────────────────────────────────────────────
# UI Settings
# ─────────────────────────────────────────────

# Rich theme colours
COLOR_USER: str = "bold cyan"
COLOR_SIFRA: str = "bold magenta"
COLOR_SYSTEM: str = "bold yellow"
COLOR_ERROR: str = "bold red"
COLOR_SUCCESS: str = "bold green"
COLOR_DIM: str = "dim white"
