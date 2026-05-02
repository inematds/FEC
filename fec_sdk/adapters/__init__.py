"""Adapters provider-específicos. Importação tardia para não exigir todas as deps.

Uso:
    from fec_sdk.adapters import get_adapter
    client = get_adapter("anthropic", model="claude-sonnet-4-6")
"""

from __future__ import annotations

from typing import Any

from fec_sdk.adapters.base import Adapter, ChatResponse


def get_adapter(provider: str, **kwargs: Any) -> Adapter:
    """Factory provider-neutral. Lança ImportError se a dep do provedor não está instalada."""
    if provider == "mock":
        from fec_sdk.adapters.mock import MockAdapter
        return MockAdapter(**kwargs)
    if provider == "anthropic":
        from fec_sdk.adapters.anthropic_adapter import AnthropicAdapter
        return AnthropicAdapter(**kwargs)
    if provider == "openai":
        from fec_sdk.adapters.openai_adapter import OpenAIAdapter
        return OpenAIAdapter(**kwargs)
    if provider == "ollama":
        from fec_sdk.adapters.ollama_adapter import OllamaAdapter
        return OllamaAdapter(**kwargs)
    raise ValueError(f"Unknown provider: {provider!r}. Choose from anthropic|openai|ollama|mock.")


__all__ = ["Adapter", "ChatResponse", "get_adapter"]
