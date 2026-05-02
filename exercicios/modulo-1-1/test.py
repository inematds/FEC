"""Teste do exercício 1.1 — pytest. Simula um modelo "lost in the middle" e
verifica que a reordenação do aluno coloca o doc relevante em zona atendida.

Determinístico, sem chamada de provedor.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Permite rodar com `pytest exercicios/modulo-1-1/test.py` sem instalar pacote
sys.path.insert(0, str(Path(__file__).parent / "starter"))
from reordenar import reordenar  # noqa: E402


# Modelo simplificado de "lost in the middle" para teste:
# atende tokens nos primeiros 25% e últimos 25% da janela.
def _modelo_loss_middle(documentos: list[str], pergunta: str) -> str:
    n = len(documentos)
    if n == 0:
        return ""
    janela_inicio = max(1, n // 4)
    janela_fim = max(1, n // 4)
    atendidos = documentos[:janela_inicio] + documentos[-janela_fim:]
    for doc in atendidos:
        if "FATO_RESPOSTA" in doc:
            return "encontrei"
    return "não sei"


# 5 cenários, todos com FATO_RESPOSTA no MEIO original (índice ~ n/2).
CASOS = [
    {
        "pergunta": "Qual é a janela do modelo X?",
        "documentos": [
            "Doc 0: lorem ipsum dolor sit amet",
            "Doc 1: consectetur adipiscing elit",
            "Doc 2: sed do eiusmod tempor",
            "Doc 3: ut labore et dolore magna",
            "Doc 4: FATO_RESPOSTA: a janela do modelo X é 200000 tokens (relevância: janela modelo X)",
            "Doc 5: ut enim ad minim veniam",
            "Doc 6: quis nostrud exercitation",
            "Doc 7: ullamco laboris nisi",
        ],
    },
    {
        "pergunta": "Como configurar prompt caching?",
        "documentos": [
            "irrelevante 1", "irrelevante 2", "irrelevante 3", "irrelevante 4",
            "FATO_RESPOSTA: prompt caching marca seções estáveis (relevância: prompt caching)",
            "irrelevante 5", "irrelevante 6", "irrelevante 7", "irrelevante 8",
        ],
    },
    {
        "pergunta": "O que é RoPE?",
        "documentos": [
            "ruído 1", "ruído 2", "ruído 3", "ruído 4", "ruído 5",
            "FATO_RESPOSTA: RoPE (Rotary Position Embedding) é um esquema (relevância: RoPE position)",
            "ruído 6", "ruído 7", "ruído 8", "ruído 9", "ruído 10",
        ],
    },
    {
        "pergunta": "Qual o custo de input vs output?",
        "documentos": [
            "x" * 5,  # placeholders
            "FATO_RESPOSTA: input tokens são cobrados independente do uso (relevância: custo input output)",
            "y" * 5,
        ],
    },
    {
        "pergunta": "O que faz attention causal?",
        "documentos": [
            "preâmbulo aleatório 1", "preâmbulo 2",
            "FATO_RESPOSTA: atenção causal mascara tokens futuros (relevância: attention causal)",
            "trailer 1", "trailer 2",
        ],
    },
]


@pytest.mark.parametrize("caso", CASOS, ids=[f"caso-{i}" for i in range(len(CASOS))])
def test_reordenacao_recupera_resposta(caso: dict) -> None:
    docs_original = list(caso["documentos"])
    docs_reordenados = reordenar(docs_original, caso["pergunta"])

    # contrato mínimo: retorna lista de strings
    assert isinstance(docs_reordenados, list)
    assert all(isinstance(d, str) for d in docs_reordenados)
    assert any("FATO_RESPOSTA" in d for d in docs_reordenados), (
        "Sua reordenação descartou o documento relevante. "
        "Truncar é OK, mas mantenha pelo menos o doc com FATO_RESPOSTA."
    )

    resposta = _modelo_loss_middle(docs_reordenados, caso["pergunta"])
    assert resposta == "encontrei", (
        f"Modelo simulado ainda perde o fato após sua reordenação. "
        f"Tente colocar docs com palavras da pergunta no início/fim, ou recuperar menos. "
        f"Pergunta: {caso['pergunta']!r} | Reordenados: {docs_reordenados[:2]}..."
    )


def test_funcao_assinatura_correta() -> None:
    """Smoke test que protege contra mudanças acidentais na API."""
    out = reordenar(["a", "FATO_RESPOSTA: x"], "x")
    assert isinstance(out, list)
