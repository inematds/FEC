"""Modelo abstrato de mensagens, tools e resultados — provider-neutral.

Cada adapter (anthropic, openai, ollama) traduz para/do formato do provedor.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(BaseModel):
    """Mensagem na janela de contexto (provider-neutral)."""

    model_config = ConfigDict(frozen=True)

    role: MessageRole
    content: str | list[dict[str, Any]]
    """Texto puro ou estrutura multimodal (image, tool_use, tool_result)."""

    name: str | None = None
    """Nome opcional do tool/agente que produziu a mensagem."""


class Tool(BaseModel):
    """Definição de tool disponível ao modelo."""

    model_config = ConfigDict(frozen=True)

    name: str = Field(pattern=r"^[a-z][a-z0-9_]{0,63}$")
    description: str
    parameters: dict[str, Any]
    """JSON Schema 2020-12 dos parâmetros."""


class ToolCall(BaseModel):
    """Chamada que o modelo faz a um tool."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    arguments: dict[str, Any]


class ToolResult(BaseModel):
    """Resultado da execução do tool, devolvido ao modelo."""

    model_config = ConfigDict(frozen=True)

    tool_call_id: str
    content: str | dict[str, Any]
    is_error: bool = False
