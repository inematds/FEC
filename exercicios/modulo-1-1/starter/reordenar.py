"""Starter para o exercício 1.1.

Implemente `reordenar` para mitigar "lost in the middle".
"""

from __future__ import annotations


def reordenar(documentos: list[str], pergunta: str) -> list[str]:
    """Reordena documentos para mitigar 'lost in the middle'.

    Args:
        documentos: lista original recuperada pelo RAG; doc relevante está no meio.
        pergunta: texto da pergunta do usuário.

    Returns:
        Lista reordenada (e/ou truncada).
    """
    # TODO: implemente sua mitigação aqui.
    # Estratégias ensinadas no módulo:
    # 1. Reranking simples (por keyword, densidade, etc.) — coloca os mais relevantes no topo/fim.
    # 2. Truncation — recuperar menos e melhor.
    # 3. Ancoragem — repetir a pergunta antes E depois da lista de documentos.
    # 4. Combinação das três.
    return documentos  # placeholder; substitua.
