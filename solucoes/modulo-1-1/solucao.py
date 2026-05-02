"""Solução do exercício 1.1 — `reordenar`.

> ⚠️ SPOILER. Tente o exercício antes de ver.

Estratégia: reranking simples por overlap de tokens da pergunta + ancoragem
(coloca o melhor doc no fim, segundo melhor no início).
"""

from __future__ import annotations

import re


def _tokenize(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"\w{3,}", text)}


def _score(doc: str, pergunta: str) -> int:
    p_tokens = _tokenize(pergunta)
    d_tokens = _tokenize(doc)
    return len(p_tokens & d_tokens)


def reordenar(documentos: list[str], pergunta: str) -> list[str]:
    """Mitiga 'lost in the middle' via reranking + ancoragem.

    Calcula score de overlap por documento. Coloca o de maior score no FIM
    (zona de recência), o segundo maior no INÍCIO (zona de prefixo), e
    ordena o resto por score decrescente no meio. Trunca a lista para no
    máximo 4 docs para reduzir ainda mais o "miolo".
    """
    if not documentos:
        return documentos

    ranked = sorted(documentos, key=lambda d: _score(d, pergunta), reverse=True)
    top4 = ranked[:4]
    if len(top4) <= 2:
        return top4

    melhor, segundo, *resto = top4
    return [segundo, *resto, melhor]
