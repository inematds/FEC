"""Adapter OpenAI. Importa `openai` lazily."""

from __future__ import annotations

from typing import Any

from fec_sdk.adapters.base import Adapter, ChatResponse
from fec_sdk.errors import ProviderError
from fec_sdk.messages import Message, Tool, ToolCall


class OpenAIAdapter(Adapter):
    def __init__(self, *, model: str, api_key: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError("OpenAI adapter requires `pip install fec-sdk[openai]`.") from exc

        self._client = OpenAI(api_key=api_key)
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
        try:
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=[_to_openai(m) for m in messages],
                max_tokens=max_tokens,
                temperature=temperature,
                seed=seed,
                tools=[_to_openai_tool(t) for t in (tools or [])] or None,
            )
        except Exception as exc:
            raise ProviderError(str(exc), provider="openai") from exc

        choice = resp.choices[0]
        msg = choice.message
        tool_calls = [
            ToolCall(id=tc.id, name=tc.function.name, arguments=_safe_json(tc.function.arguments))
            for tc in (msg.tool_calls or [])
        ]
        return ChatResponse(
            content=msg.content or "",
            tool_calls=tool_calls,
            stop_reason=choice.finish_reason or "stop",
            input_tokens=resp.usage.prompt_tokens if resp.usage else 0,
            output_tokens=resp.usage.completion_tokens if resp.usage else 0,
            model=resp.model,
            raw=resp.model_dump() if hasattr(resp, "model_dump") else {},
        )


def _to_openai(msg: Message) -> dict[str, Any]:
    return {"role": msg.role.value, "content": msg.content}


def _to_openai_tool(tool: Tool) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters,
        },
    }


def _safe_json(s: str) -> dict[str, Any]:
    import json
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return {"_raw": s}
