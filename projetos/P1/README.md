# P1 — Buscador citável (RAG sobre ArXiv)

**Status:** GA · entrega após T2-T3.2.
**Tempo estimado:** 4-6h.

## Objetivo

Construa um RAG que responde perguntas sobre um conjunto de abstracts de ArXiv (cs.LG / cs.CL), com **citações obrigatórias** e **groundedness ≥0.85** medido contra o golden `FEC-GS-RAG-v1`.

## O que entregar

- `solution.py` — pipeline RAG completo (indexação + recuperação + geração).
- `eval.py` — script que roda contra `evals/v1/datasets/FEC-GS-RAG-v1.json` e produz `metrics.json`.
- `report.md` — análise dos resultados, decisões de chunking, modelo escolhido.

## Critérios objetivos (rubrica)

Ver [`RUBRIC.md`](./RUBRIC.md). Aprovação exige:

- [ ] **Groundedness ≥ 0.85** no golden de 30 perguntas.
- [ ] **100% das respostas têm citação** (URL/ID do abstract).
- [ ] **Custo médio ≤ orçamento** definido em `evals/v1/budgets.json` (`FEC-BUDGET-RAG-v1`).
- [ ] **Sandbox jailed** para qualquer leitura de filesystem (PLAN item 62a).
- [ ] **Reproduzível:** terceiro rodando `python eval.py` em ambiente limpo obtém os mesmos números.

## Conhecimento aplicado

- T1.1 (lost in the middle) → reordenação de docs recuperados.
- T1.2 (custo) → escolha de modelo low-cost vs frontier para este volume.
- T2.1 (estrutura) → ancoragem da pergunta + formato de resposta com citação.
- T2.2 (eval primer) → comparação A/B de variantes de prompt no harness.
- T3.1 (indexação) → chunking deliberado + embeddings.
- T3.2 (reranking) → BM25 híbrido + reranker.

## Quando NÃO fazer este projeto

Se você ainda não terminou T3.2. Tentar P1 antes só vai te frustrar.

## Datasets

- `fixtures/arxiv-cs-100/` — 100 abstracts (incluído no repo).
- `evals/v1/datasets/FEC-GS-RAG-v1.json` — 30 perguntas com gabarito.

## Submissão

Branch `projetos/p1-<seu-handle>` em fork. PR com label `projeto:P1`.
