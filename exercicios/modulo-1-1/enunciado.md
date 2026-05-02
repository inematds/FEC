# Exercício 1.1 — Reordenar para mitigar "lost in the middle"

> Tempo estimado: 30-45 min. Pré-requisitos: módulo 1.1 lido, `pip install fec-sdk` ou `pip install -e .` no repo.

## Contexto

Você recebe 5 cenários. Em cada um, há uma lista de documentos recuperados por um RAG e a posição do
documento que de fato contém a resposta. Por construção, todos os cenários têm o documento relevante
no MEIO da janela (PLAN item ensinado: "lost in the middle"). Sua tarefa é implementar uma estratégia
de mitigação.

## O que entregar

Edite `exercicios/modulo-1-1/starter/reordenar.py`. Implemente:

```python
def reordenar(documentos: list[str], pergunta: str) -> list[str]:
    """Recebe a lista original (relevante no meio) e devolve a lista reordenada
    para mitigar 'lost in the middle'. Pode usar qualquer mitigação ensinada:
    reranking trivial por palavra-chave, top-k truncation, ancoragem, etc."""
```

## Critério de "feito"

Rode:

```bash
pytest exercicios/modulo-1-1/test.py -v
```

Deve passar **≥4 dos 5 casos**. O teste é determinístico, sem chamada de provedor — ele simula um
modelo que segue o "lost in the middle" e verifica se sua reordenação faz a resposta certa aparecer.

## Dicas

- A solução não precisa ser ML. Heurísticas simples (busca por keyword, ranqueamento por densidade
  de termos da pergunta) já passam em ≥4/5.
- Aceita-se truncar a lista — recuperar menos é uma das mitigações ensinadas.
- Se ficar travado, leia novamente "Sub-tópico 4: ordem das seções" do módulo.

## Solução (NÃO olhe antes de tentar)

Em `solucoes/modulo-1-1/solucao.py`. Vai estar lá depois que você entregar.
