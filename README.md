# 🤖 SIFRA – AI Terminal Assistant

> *Your Intelligent Terminal Companion*

SIFRA is a futuristic, conversational AI assistant that runs directly inside your terminal.

Built with **Python** and **Rich**, SIFRA provides natural AI conversations, long-term memory, chat history, slash commands, and a beautiful terminal interface.

Users **do not need their own AI API key**. SIFRA connects securely to a hosted backend server that communicates with the AI provider.

---

# ✨ Features

| Feature | Details |
|---|---|
| 🤖 AI Chat | Natural conversations with SIFRA |
| 🔑 No API Key Required | Users can simply install and run SIFRA |
| 🧠 Long-term Memory | Saves important information across sessions |
| 💬 Chat History | Stores and displays previous conversations |
| ⚡ Slash Commands | Quick commands for controlling SIFRA |
| 🎨 Beautiful UI | Modern terminal interface built with Rich |
| 🔒 Secure Backend | AI provider credentials remain on the backend server |
| 🗄 SQLite Database | Stores conversations and memories locally |

---

# 🚀 Installation Guide

## Step 1 — Install Python

Make sure Python **3.11 or newer** is installed.

Check your Python version:

### macOS / Linux

```bash
python3 --version
```

### Windows

```bash
python --version
```

If Python is not installed, install it from:

https://www.python.org/downloads/

---

## Step 2 — Install Git

Check whether Git is installed:

```bash
git --version
```

If Git is not installed, download it from:

https://git-scm.com/downloads

---

## Step 3 — Clone the SIFRA Repository

Open Terminal, PowerShell, or Command Prompt and run:

```bash
git clone https://github.com/hetjaviya15/Sifra-Terminal-AI.git
```

Then enter the project folder:

```bash
cd Sifra-Terminal-AI
```

---

# 🍎 macOS Setup

## Step 4 — Create a Virtual Environment

```bash
python3 -m venv .venv
```

## Step 5 — Activate the Virtual Environment

```bash
source .venv/bin/activate
```

You should now see something similar to:

```text
(.venv)
```

at the beginning of your terminal line.

---

## Step 6 — Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

This installs all required Python packages.

---

## Step 7 — Create the Environment File

```bash
cp .env.example .env
```

You do **not** need to add your own AI API key.

---

## Step 8 — Run SIFRA

```bash
python3 main.py
```

🎉 SIFRA should now start inside your terminal.

---

# ⚡ macOS Quick Installation

If you want to perform the complete installation at once, open Terminal and paste:

```bash
cd ~/Desktop && \
git clone https://github.com/hetjaviya15/Sifra-Terminal-AI.git && \
cd Sifra-Terminal-AI && \
python3 -m venv .venv && \
source .venv/bin/activate && \
python3 -m pip install -r requirements.txt && \
cp .env.example .env && \
python3 main.py
```

---

# 🔄 Running SIFRA Again on macOS

After installing SIFRA once, you do not need to install dependencies again.

Open Terminal and run:

```bash
cd ~/Desktop/Sifra-Terminal-AI
source .venv/bin/activate
python3 main.py
```

---

# 🪟 Windows Setup

## Step 4 — Create a Virtual Environment

Open PowerShell and run:

```powershell
python -m venv .venv
```

---

## Step 5 — Activate the Virtual Environment

### PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Command Prompt

```cmd
.venv\Scripts\activate
```

---

## Step 6 — Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Step 7 — Create the Environment File

### PowerShell

```powershell
copy .env.example .env
```

### Command Prompt

```cmd
copy .env.example .env
```

No AI API key is required.

---

## Step 8 — Run SIFRA

```bash
python main.py
```

🎉 SIFRA should now start inside your terminal.

---

# ⚡ Windows Quick Installation

Open PowerShell and run:

```powershell
cd $HOME\Desktop
git clone https://github.com/hetjaviya15/Sifra-Terminal-AI.git
cd Sifra-Terminal-AI
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
copy .env.example .env
python main.py
```

---

# 🔄 Running SIFRA Again on Windows

Open PowerShell and run:

```powershell
cd $HOME\Desktop\Sifra-Terminal-AI
.venv\Scripts\Activate.ps1
python main.py
```

---

# 🔐 No API Key Required

Normal SIFRA users do **not** need to create an AI API key.

The application works like this:

```text
User
  ↓
SIFRA Terminal Application
  ↓
Secure SIFRA Backend
  ↓
AI Provider
```

The AI provider credentials remain securely stored on the backend server.

This means users can simply:

```text
Clone → Install → Run → Chat 🤖
```

---

# 💬 Slash Commands

| Command | Description |
|---|---|
| `/help` | Show all available commands |
| `/new` | Start a fresh conversation |
| `/history` | Browse previous conversations |
| `/memory` | View saved long-term memories |
| `/forget <key>` | Delete a saved memory |
| `/clear` | Clear the terminal screen |
| `/about` | Learn more about SIFRA |
| `/exit` | Exit SIFRA gracefully |

---

# 🧠 Long-Term Memory

SIFRA can remember important information across sessions.

Example:

```text
You    ▸ My name is Het and I'm building a Flask application.

SIFRA  ▸ Nice to meet you, Het! I'll remember that you're building a Flask application.
```

To view saved memories:

```text
/memory
```

To delete a memory:

```text
/forget name
```

---

# 💬 Conversation History

SIFRA stores previous conversations locally.

Use:

```text
/history
```

to browse previous conversations.

---

# 🗄 Database

SIFRA automatically creates a SQLite database:

```text
database/sifra.db
```

The database stores:

| Table | Purpose |
|---|---|
| `conversations` | Conversation sessions |
| `messages` | Messages from conversations |
| `memories` | Long-term saved memories |

---

# 📁 Project Structure

```text
Sifra-Terminal-AI/
│
├── main.py
├── config.py
│
├── core/
│   ├── ai_engine.py
│   ├── personality.py
│   └── conversation.py
│
├── database/
│   ├── database.py
│   └── sifra.db
│
├── features/
│   ├── memory.py
│   ├── history.py
│   └── commands.py
│
├── ui/
│   ├── terminal_ui.py
│   └── banner.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🛠 Customizing SIFRA

## Change SIFRA's Personality

Open:

```text
core/personality.py
```

Edit the `SIFRA_SYSTEM_PROMPT` to change SIFRA's personality, communication style, and behavior.

---

## Add a New Slash Command

Open:

```text
features/commands.py
```

Example:

```python
def cmd_mycommand(args: str = "") -> None:
    """My new command."""
    print_info("Hello from my command!")

COMMAND_REGISTRY["/mycommand"] = cmd_mycommand
```

---

# 🛠 Troubleshooting

## ModuleNotFoundError

Make sure the virtual environment is activated.

### macOS

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Windows

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

---

## Python Command Not Found

On macOS, use:

```bash
python3 main.py
```

instead of:

```bash
python main.py
```

---

## Backend Connection Error

Make sure:

- You have an active internet connection.
- The SIFRA backend server is online.
- You are using the latest version of SIFRA.

To update the project:

```bash
git pull
```

Then reinstall dependencies if required:

```bash
python3 -m pip install -r requirements.txt
```

---

# 📋 Requirements

- Python 3.11 or newer
- Git
- Internet connection

### Normal users do NOT need:

- ❌ OpenAI API key
- ❌ Groq API key
- ❌ xAI API key
- ❌ Any paid AI subscription

---

# 📄 License

This project was created as a university Application Development minor project.

Free to use and modify for educational purposes.

---

# 🚀 Enjoy SIFRA!

Clone the repository, run the application, and start chatting with your intelligent terminal companion.

**Made with ❤️ using Python**
