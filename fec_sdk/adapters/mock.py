"""Mock adapter: respostas gravadas/programadas para CI sem rede e laboratórios offline.

Uso:
    >>> from fec_sdk.adapters.mock import MockAdapter
    >>> mock = MockAdapter(scripted=[("hello", "olá!")])
    >>> mock.chat([Message(role=MessageRole.USER, content="hello")]).content
    'olá!'

Quando o lab depende de capacidade não-portável (ex.: prompt caching), o adapter
mock pode reproduzir o comportamento determinístico e medições gravadas.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from fec_sdk.adapters.base import Adapter, ChatResponse
from fec_sdk.messages import Message, Tool, ToolCall


class MockAdapter(Adapter):
    """Adapter sem I/O externo.

    Modos:
    1. `scripted=[(needle, response)]` — busca substring em `messages[-1].content`.
    2. `recorded_dir=Path(...)` — lookup por sha256 das mensagens (gravações).
    3. fallback: ecoa o último prompt do user.
    """

    def __init__(
        self,
        *,
        scripted: list[tuple[str, str]] | None = None,
        recorded_dir: Path | None = None,
        model: str = "mock-model@v1",
    ) -> None:
        self._scripted = scripted or []
        self._recorded_dir = recorded_dir
        self._model = model

    def model_id(self) -> str:
        return self._model

    def chat(
        self,
        messages: list[Message],
        *,
        tools: list[Tool] | None = None,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        seed: int | None = None,
    ) -> ChatResponse:
        text = self._resolve(messages)

        return ChatResponse(
            content=text,
            tool_calls=[],
            stop_reason="end_turn",
            input_tokens=sum(len(_msg_text(m)) for m in messages) // 4,
            output_tokens=len(text) // 4,
            model=self._model,
            raw={"mock": True, "messages": [m.model_dump() for m in messages]},
        )

    def _resolve(self, messages: list[Message]) -> str:
        last_user = next((m for m in reversed(messages) if m.role.value == "user"), None)
        haystack = _msg_text(last_user) if last_user else ""

        for needle, response in self._scripted:
            if needle in haystack:
                return response

        if self._recorded_dir is not None:
            key = self._cache_key(messages)
            file = self._recorded_dir / f"{key}.json"
            if file.exists():
                data: dict[str, Any] = json.loads(file.read_text(encoding="utf-8"))
                return str(data.get("content", ""))

        return f"[mock echo] {haystack}"

    @staticmethod
    def _cache_key(messages: list[Message]) -> str:
        canon = json.dumps([m.model_dump() for m in messages], sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canon.encode("utf-8")).hexdigest()[:16]


def _msg_text(msg: Message | None) -> str:
    if msg is None:
        return ""
    if isinstance(msg.content, str):
        return msg.content
    return " ".join(part.get("text", "") for part in msg.content if isinstance(part, dict))
