"""Adapter Anthropic. Importa `anthropic` lazily."""

from __future__ import annotations

from typing import Any

from fec_sdk.adapters.base import Adapter, ChatResponse
from fec_sdk.errors import ProviderError
from fec_sdk.messages import Message, MessageRole, Tool, ToolCall


class AnthropicAdapter(Adapter):
    def __init__(self, *, model: str, api_key: str | None = None) -> None:
        try:
            import anthropic
        except ImportError as exc:
            raise ImportError(
                "Anthropic adapter requires `pip install fec-sdk[anthropic]`."
            ) from exc

        self._client = anthropic.Anthropic(api_key=api_key)
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
        system, others = _split_system(messages)

        try:
            resp = self._client.messages.create(
                model=self._model,
                system=system or "",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[_to_anthropic(m) for m in others],
                tools=[_to_anthropic_tool(t) for t in (tools or [])] or None,
            )
        except Exception as exc:  # anthropic.APIError, network, etc.
            raise ProviderError(str(exc), provider="anthropic") from exc

        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        for block in resp.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(id=block.id, name=block.name, arguments=block.input))

        return ChatResponse(
            content="".join(text_parts),
            tool_calls=tool_calls,
            stop_reason=resp.stop_reason or "end_turn",
            input_tokens=resp.usage.input_tokens,
            output_tokens=resp.usage.output_tokens,
            model=resp.model,
            raw=resp.model_dump() if hasattr(resp, "model_dump") else {},
        )


def _split_system(messages: list[Message]) -> tuple[str | None, list[Message]]:
    system_msgs = [m for m in messages if m.role == MessageRole.SYSTEM]
    others = [m for m in messages if m.role != MessageRole.SYSTEM]
    sys_text = "\n\n".join(
        m.content if isinstance(m.content, str) else "" for m in system_msgs
    ) or None
    return sys_text, others


def _to_anthropic(msg: Message) -> dict[str, Any]:
    return {"role": msg.role.value, "content": msg.content}


def _to_anthropic_tool(tool: Tool) -> dict[str, Any]:
    return {"name": tool.name, "description": tool.description, "input_schema": tool.parameters}
