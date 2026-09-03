"""
core/ai_engine.py - Modular AI engine for SIFRA.

This module handles all communication with the AI provider.
It is deliberately decoupled from the rest of the app so you can
swap out the AI backend (OpenAI → Groq → Ollama → etc.) by only
editing this file and your .env values.
"""

from typing import Any, cast
from openai import OpenAI, APIConnectionError, AuthenticationError, RateLimitError
from openai.types.chat import ChatCompletionMessageParam
from config import AI_API_KEY, AI_MODEL, AI_BASE_URL, MAX_CONTEXT_MESSAGES
from core.personality import get_system_prompt
from database.database import get_memory_context_string


class AIEngine:
    """
    Wraps an OpenAI-compatible client.

    The client is compatible with any provider that implements the
    OpenAI API spec (OpenAI, Azure OpenAI, Groq, Ollama, Together AI, etc.)
    You only need to change AI_BASE_URL and AI_MODEL in your .env file.
    """

    def __init__(self) -> None:
        if not AI_API_KEY:
            raise ValueError(
                "AI_API_KEY is not set. "
                "Please add your API key to the .env file."
            )

        self.client = OpenAI(
            api_key=AI_API_KEY,
            base_url=AI_BASE_URL,
        )
        self.model = AI_MODEL

    def _build_messages(self, conversation_history: list[dict[str, Any]]) -> list[ChatCompletionMessageParam]:
        """
        Build the full message list to send to the API.

        The structure is:
          [system prompt]  +  [memory context (if any)]  +  [conversation history]

        The history is trimmed to MAX_CONTEXT_MESSAGES to avoid token overflow.
        """
        system_content = get_system_prompt()

        # Inject long-term memories if they exist
        memory_ctx = get_memory_context_string()
        if memory_ctx:
            system_content = f"{system_content}\n\n{memory_ctx}"

        raw_messages: list[dict[str, Any]] = [{"role": "system", "content": system_content}]

        # Keep only the most recent N messages for context
        trimmed = conversation_history[-MAX_CONTEXT_MESSAGES:]
        raw_messages.extend(trimmed)

        return cast(list[ChatCompletionMessageParam], raw_messages)

    def chat(self, conversation_history: list[dict[str, Any]]) -> str:
        """
        Send the conversation to the AI and return the assistant's reply.

        Args:
            conversation_history: List of {"role": ..., "content": ...} dicts
                                   representing the full session so far.

        Returns:
            The assistant's reply as a plain string.

        Raises:
            ConnectionError: On network / API problems.
            PermissionError: On authentication failures.
            RuntimeError:   On rate limits or unexpected errors.
        """
        messages = self._build_messages(conversation_history)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.75,   # A touch of creativity
                max_tokens=1500,
            )
            content = response.choices[0].message.content
            return (content or "").strip()

        except AuthenticationError:
            raise PermissionError(
                "Invalid API key. Please check AI_API_KEY in your .env file."
            )
        except APIConnectionError:
            raise ConnectionError(
                "Could not reach the AI service. "
                "Please check your internet connection or AI_BASE_URL."
            )
        except RateLimitError:
            raise RuntimeError(
                "You've hit the API rate limit. Please wait a moment and try again."
            )
        except Exception as exc:
            raise RuntimeError(f"Unexpected AI error: {exc}") from exc
