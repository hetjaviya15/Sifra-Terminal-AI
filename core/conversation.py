"""
core/conversation.py - Session-level conversation state manager.

Tracks the in-memory message history for the current session,
persists each exchange to the database, and delegates AI calls
to the AIEngine.
"""

from core.ai_engine import AIEngine
from database.database import create_conversation, save_message


class Conversation:
    """
    Manages a single chat session.

    Attributes:
        conversation_id: The DB row ID for this session.
        history:         In-memory list of {"role", "content"} dicts.
        engine:          The AI engine instance.
    """

    def __init__(self, engine: AIEngine) -> None:
        self.engine: AIEngine = engine
        self.conversation_id: int = create_conversation()
        self.history: list[dict] = []  # in-memory context for this session

    def send(self, user_message: str) -> str:
        """
        Send a user message, get SIFRA's reply, and persist both.

        Args:
            user_message: The raw text typed by the user.

        Returns:
            SIFRA's reply as a string.
        """
        # Add user turn to in-memory history
        self.history.append({"role": "user", "content": user_message})

        # Get AI response (may raise exceptions — caller handles them)
        reply = self.engine.chat(self.history)

        # Add assistant turn to in-memory history
        self.history.append({"role": "assistant", "content": reply})

        # Persist both turns to the database
        save_message(self.conversation_id, "user", user_message)
        save_message(self.conversation_id, "assistant", reply)

        return reply

    def reset(self, engine: AIEngine | None = None) -> None:
        """
        Start a brand-new conversation (clears in-memory history).
        Creates a fresh DB conversation record.

        Args:
            engine: Optionally swap the AI engine on reset.
        """
        if engine:
            self.engine = engine
        self.conversation_id = create_conversation()
        self.history = []
