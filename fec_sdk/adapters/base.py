"""Interface abstrata de adapter. Adapters provider-específicos herdam daqui."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from fec_sdk.messages import Message, Tool, ToolCall


@dataclass(frozen=True)
class ChatResponse:
    """Resposta provider-neutral de uma chamada de chat."""

    content: str
    tool_calls: list[ToolCall]
    stop_reason: str  # "end_turn", "tool_use", "max_tokens", ...
    input_tokens: int
    output_tokens: int
    model: str
    raw: dict[str, Any]
    """Resposta crua do provedor — para debugging."""


class Adapter(ABC):
    """Adapter base. Subclasses implementam `chat()`."""

    @abstractmethod
    def chat(
        self,
        messages: list[Message],
        *,
        tools: list[Tool] | None = None,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        seed: int | None = None,
    ) -> ChatResponse:
        """Envia mensagens, recebe resposta. Determinístico por default (temperature 0)."""

    @abstractmethod
    def model_id(self) -> str:
        """ID exato do modelo configurado, para logging e manifestos de eval."""
