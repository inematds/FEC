"""Adapter Ollama. Importa `ollama` lazily."""

from __future__ import annotations

from typing import Any

from fec_sdk.adapters.base import Adapter, ChatResponse
from fec_sdk.errors import ProviderError
from fec_sdk.messages import Message, Tool, ToolCall


class OllamaAdapter(Adapter):
    def __init__(self, *, model: str, host: str = "http://localhost:11434") -> None:
        try:
            from ollama import Client
        except ImportError as exc:
            raise ImportError("Ollama adapter requires `pip install fec-sdk[ollama]`.") from exc

        self._client = Client(host=host)
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
            resp = self._client.chat(
                model=self._model,
                messages=[_to_ollama(m) for m in messages],
                options={
                    "num_predict": max_tokens,
                    "temperature": temperature,
                    **({"seed": seed} if seed is not None else {}),
                },
                tools=[_to_ollama_tool(t) for t in (tools or [])] or None,
            )
        except Exception as exc:
            raise ProviderError(str(exc), provider="ollama") from exc

        msg = resp["message"]
        tool_calls = [
            ToolCall(id=tc.get("id", ""), name=tc["function"]["name"], arguments=tc["function"]["arguments"])
            for tc in msg.get("tool_calls", [])
        ]
        return ChatResponse(
            content=msg.get("content", "") or "",
            tool_calls=tool_calls,
            stop_reason="end_turn",
            input_tokens=resp.get("prompt_eval_count", 0),
            output_tokens=resp.get("eval_count", 0),
            model=resp.get("model", self._model),
            raw=dict(resp),
        )


def _to_ollama(msg: Message) -> dict[str, Any]:
    return {"role": msg.role.value, "content": msg.content if isinstance(msg.content, str) else str(msg.content)}


def _to_ollama_tool(tool: Tool) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {"name": tool.name, "description": tool.description, "parameters": tool.parameters},
    }
