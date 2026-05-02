"""Exemplo provider-neutral — medição básica de "lost in the middle".

Roda com qualquer adapter via fec_sdk. Adaptadores específicos:
- exemplos/modulo-1-1/anthropic.py
- exemplos/modulo-1-1/openai.py
- exemplos/modulo-1-1/oss.py
"""

from __future__ import annotations

import argparse

from fec_sdk import Message, MessageRole, check_compat
from fec_sdk.adapters import get_adapter


def medir(provider: str, model: str | None = None) -> None:
    check_compat("modulo-1-1", expected_sdk_version=">=1.0,<2.0")

    if provider == "mock":
        client = get_adapter("mock", scripted=[
            ("início", "200000 tokens"),
            ("meio", "não sei"),
            ("fim", "200000 tokens"),
        ])
    else:
        client = get_adapter(provider, model=model or "")

    fato = "FATO: a janela do modelo X é 200000 tokens."
    ruido = "\n".join(f"Doc {i}: lorem ipsum dolor sit amet." for i in range(20))

    cenarios = {
        "início": fato + "\n" + ruido,
        "meio":   ruido[: len(ruido) // 2] + "\n" + fato + "\n" + ruido[len(ruido) // 2 :],
        "fim":    ruido + "\n" + fato,
    }

    for posicao, contexto in cenarios.items():
        resp = client.chat([
            Message(role=MessageRole.SYSTEM, content="Responda apenas com fatos do contexto. Se não houver, diga 'não sei'."),
            Message(role=MessageRole.USER, content=f"{contexto}\n\nQual a janela do modelo X?"),
        ])
        print(f"[{posicao:>6s}] in={resp.input_tokens:>5d} out={resp.output_tokens:>3d}  →  {resp.content[:80]}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--provider", default="mock", choices=["mock", "anthropic", "openai", "ollama"])
    p.add_argument("--model", default=None)
    args = p.parse_args()
    medir(args.provider, args.model)
