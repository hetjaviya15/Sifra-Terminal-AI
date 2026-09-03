"""
core/ai_engine.py - Modular AI engine for SIFRA.

Supports two modes (set MODE in .env):

  MODE=backend  (default & recommended)
    → Calls your private SIFRA FastAPI backend.
      Users need NO AI API key — just SIFRA_BACKEND_URL.

  MODE=direct
    → Calls the AI provider directly.
      Requires AI_API_KEY in .env.
"""

import logging
import httpx
from typing import Any
from openai import OpenAI, APIConnectionError, AuthenticationError, RateLimitError
from openai.types.chat import ChatCompletionMessageParam
from typing import cast

from config import AI_API_KEY, AI_MODEL, AI_BASE_URL, MAX_CONTEXT_MESSAGES
from core.personality import get_system_prompt
from database.database import get_memory_context_string

logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════════════════════
# Backend mode — calls your FastAPI server (synchronous httpx)
# ════════════════════════════════════════════════════════════════════════════

class BackendEngine:
    """
    Sends messages to the SIFRA FastAPI backend using a synchronous HTTP client.
    No AI API key needed on the client machine.
    """

    def __init__(self, backend_url: str) -> None:
        self.chat_url = backend_url.rstrip("/") + "/chat"
        # Synchronous client — no event loop issues
        self._client = httpx.Client(timeout=60.0)

    def chat_sync(self, conversation_history: list[dict[str, Any]]) -> str:
        """Send conversation to the backend and return SIFRA's reply."""
        # Strip system messages — the backend adds its own
        history = [m for m in conversation_history if m.get("role") != "system"]

        # Inject long-term memory context if any exists
        memory_ctx = get_memory_context_string()
        if memory_ctx:
            history = [{"role": "system", "content": memory_ctx}] + history

        # The last message must be from the user
        if not history or history[-1]["role"] != "user":
            raise RuntimeError("No user message found in history.")

        user_message = history[-1]["content"]
        conv_history = history[:-1]

        try:
            response = self._client.post(
                self.chat_url,
                json={
                    "message": user_message,
                    "conversation_history": conv_history,
                },
            )
            response.raise_for_status()
            data = response.json()
            return str(data.get("response", "")).strip()

        except httpx.ConnectError:
            raise ConnectionError(
                f"Cannot connect to the SIFRA backend at {self.chat_url}.\n"
                "Make sure the backend is running:  uvicorn main:app --reload"
            )
        except httpx.TimeoutException:
            raise ConnectionError("Request to SIFRA backend timed out.")
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            try:
                detail = exc.response.json().get("detail", str(exc))
            except Exception:
                detail = str(exc)
            if status == 429:
                raise RuntimeError(f"Rate limit: {detail}")
            elif status in (502, 503):
                raise ConnectionError(f"Backend AI error: {detail}")
            else:
                raise RuntimeError(f"Backend error {status}: {detail}")


# ════════════════════════════════════════════════════════════════════════════
# Direct mode — calls AI provider directly (synchronous OpenAI client)
# ════════════════════════════════════════════════════════════════════════════

class DirectEngine:
    """
    Calls the AI provider directly using a synchronous OpenAI-compatible client.
    Requires AI_API_KEY in .env.
    """

    def __init__(self) -> None:
        if not AI_API_KEY:
            raise ValueError(
                "AI_API_KEY is not set.\n"
                "Add it to .env or switch to backend mode "
                "(MODE=backend + SIFRA_BACKEND_URL)."
            )
        # Synchronous client — no asyncio needed
        self._client = OpenAI(api_key=AI_API_KEY, base_url=AI_BASE_URL)
        self.model = AI_MODEL

    def _build_messages(
        self, conversation_history: list[dict[str, Any]]
    ) -> list[ChatCompletionMessageParam]:
        system_content = get_system_prompt()
        memory_ctx = get_memory_context_string()
        if memory_ctx:
            system_content = f"{system_content}\n\n{memory_ctx}"
        raw: list[dict[str, Any]] = [{"role": "system", "content": system_content}]
        raw.extend(conversation_history[-MAX_CONTEXT_MESSAGES:])
        return cast(list[ChatCompletionMessageParam], raw)

    def chat_sync(self, conversation_history: list[dict[str, Any]]) -> str:
        """Send conversation to AI provider and return the reply."""
        messages = self._build_messages(conversation_history)
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.75,
                max_tokens=1500,
            )
            content = response.choices[0].message.content
            return (content or "").strip()
        except AuthenticationError:
            raise PermissionError("Invalid API key. Check AI_API_KEY in .env.")
        except APIConnectionError:
            raise ConnectionError("Cannot reach the AI service. Check AI_BASE_URL.")
        except RateLimitError:
            raise RuntimeError("Rate limit hit. Please wait and try again.")
        except Exception as exc:
            logger.exception("Unexpected AI error: %s", exc)
            raise RuntimeError(f"Unexpected AI error: {exc}") from exc


# ════════════════════════════════════════════════════════════════════════════
# AIEngine facade — picks the right engine based on MODE in .env
# ════════════════════════════════════════════════════════════════════════════

class AIEngine:
    """
    Public interface used by the rest of SIFRA.

    Set MODE in .env:
      MODE=backend  → BackendEngine (no client API key needed)
      MODE=direct   → DirectEngine  (needs AI_API_KEY in .env)
    """

    def __init__(self) -> None:
        import os
        from dotenv import load_dotenv
        load_dotenv()

        mode = os.getenv("MODE", "backend").strip().lower()
        backend_url = os.getenv("SIFRA_BACKEND_URL", "").strip()

        if mode == "backend":
            if not backend_url:
                raise ValueError(
                    "SIFRA_BACKEND_URL is not set.\n"
                    "Add to .env:  SIFRA_BACKEND_URL=http://127.0.0.1:8000"
                )
            self._engine: BackendEngine | DirectEngine = BackendEngine(backend_url)
            logger.info("AI engine: backend mode → %s", backend_url)
        else:
            self._engine = DirectEngine()
            logger.info("AI engine: direct mode → %s", AI_MODEL)

    def chat(self, conversation_history: list[dict[str, Any]]) -> str:
        """Send conversation and return SIFRA's reply."""
        return self._engine.chat_sync(conversation_history)
