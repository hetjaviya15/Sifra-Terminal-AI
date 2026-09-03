# SIFRA – AI Terminal Assistant

> *Your Intelligent Terminal Companion*

SIFRA is a futuristic, conversational AI assistant that runs entirely inside
your terminal. Built with Python, Rich, and an OpenAI-compatible API backend,
SIFRA offers a polished command-line chat experience with persistent memory,
conversation history, and a strong personality.

---

## ✨ Features

| Feature | Details |
|---|---|
| **AI Chat** | Natural conversations powered by any OpenAI-compatible model |
| **SIFRA Personality** | Friendly, intelligent, slightly playful female AI |
| **Session Memory** | Full context maintained within a session |
| **Long-term Memory** | Saves facts (name, preferences, projects) across sessions |
| **Chat History** | Browse and re-read past conversations (SQLite) |
| **Slash Commands** | `/help`, `/history`, `/memory`, `/forget`, `/new`, `/clear`, `/about`, `/exit` |
| **Beautiful UI** | Rich panels, Markdown rendering, spinners, colour themes |
| **Modular Design** | Swap AI providers by changing two lines in `.env` |

---

## 🗂 Project Structure

```
sifra/
│
├── main.py                  ← Entry point
│
├── config.py                ← All settings & env vars
│
├── core/
│   ├── ai_engine.py         ← OpenAI-compatible AI client (swap-friendly)
│   ├── personality.py       ← SIFRA's system prompt / character definition
│   └── conversation.py      ← Session-level message history manager
│
├── database/
│   ├── database.py          ← SQLite helpers (init, messages, memories)
│   └── sifra.db             ← Auto-created on first run
│
├── features/
│   ├── memory.py            ← Long-term memory (save / show / forget)
│   ├── history.py           ← Conversation history display
│   └── commands.py          ← Slash-command dispatcher & registry
│
├── ui/
│   ├── terminal_ui.py       ← Rich rendering (panels, spinner, messages)
│   └── banner.py            ← Startup banner & branding
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone / download the project

```bash
cd ~/Desktop/Projects/Sifra
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
cp .env.example .env
```

Open `.env` in any text editor and fill in your API key:

```env
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AI_MODEL=gpt-4o-mini
AI_BASE_URL=https://api.openai.com/v1
```

> **Where do I get an API key?**
> - **OpenAI** → https://platform.openai.com/api-keys
> - **Groq** (free tier) → https://console.groq.com
> - **Ollama** (runs locally, free) → https://ollama.com — no key needed, set `AI_API_KEY=ollama`

### 5. Run SIFRA

```bash
python main.py
```

---

## 🔌 Switching AI Providers

Only your `.env` file needs to change — no code edits required.

| Provider | `AI_BASE_URL` | Example `AI_MODEL` |
|---|---|---|
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| Groq | `https://api.groq.com/openai/v1` | `llama3-8b-8192` |
| Ollama (local) | `http://localhost:11434/v1` | `llama3` |
| Together AI | `https://api.together.xyz/v1` | `mistralai/Mistral-7B` |

---

## 💬 Slash Commands

| Command | Description |
|---|---|
| `/help` | Show all available commands |
| `/new` | Start a fresh conversation (clears context) |
| `/history` | Browse previous conversations |
| `/memory` | View saved long-term memories |
| `/forget <key>` | Delete a memory by key |
| `/clear` | Clear the terminal screen |
| `/about` | About SIFRA |
| `/exit` | Exit SIFRA gracefully |

---

## 🧠 Long-term Memory

SIFRA automatically detects and saves important facts you share
(your name, language preferences, project names, etc.) across sessions.

**Example:**
```
You    ▸  My name is Het and I'm building a Flask app.
SIFRA  ▸  Nice to meet you, Het! Flask is a great choice for Python web apps...
```

Next time you open SIFRA, she'll already know your name.

Use `/memory` to see what's saved and `/forget name` to remove anything.

---

## 🗄 Database

SIFRA creates `database/sifra.db` automatically on first run.

| Table | Columns |
|---|---|
| `conversations` | `id`, `created_at` |
| `messages` | `id`, `conversation_id`, `role`, `content`, `timestamp` |
| `memories` | `id`, `memory_key`, `memory_value`, `created_at` |

---

## 🛠 Extending SIFRA

### Add a new slash command

In [`features/commands.py`](features/commands.py):

```python
def cmd_mycommand(args: str = "") -> None:
    """My new command."""
    print_info("Hello from my command!")

# Then add to the registry:
COMMAND_REGISTRY["/mycommand"] = cmd_mycommand
```

### Change SIFRA's personality

Edit [`core/personality.py`](core/personality.py) — the `SIFRA_SYSTEM_PROMPT` string.

---

## 📋 Requirements

- Python 3.11+
- Internet connection (or local Ollama instance)
- An API key from any OpenAI-compatible provider

---

## 📄 License

This project was created as a university Application Development minor project.
Free to use and modify for educational purposes.
