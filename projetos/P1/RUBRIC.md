# P1 — Rubrica

> _Critérios objetivos. PR não pode virar "completo" sem TODOS os ✅. PLAN item 25._

## Bloqueantes (todos exigidos)

| # | Critério | Como verificar |
|---|----------|----------------|
| 1 | Groundedness ≥ 0.85 no golden FEC-GS-RAG-v1 | `python eval.py --golden evals/v1/datasets/FEC-GS-RAG-v1.json --judge models[frontier]` deve retornar `groundedness >= 0.85` |
| 2 | 100% das respostas têm citação | `eval.py` valida regex `\[arxiv:\d+\.\d+\]` em cada resposta |
| 3 | Custo médio ≤ orçamento | `metrics.json` tem `cost_usd_per_query <= FEC-BUDGET-RAG-v1` (config em budgets.json) |
| 4 | Sandbox jailed em IO de fs | Code review confirma `with FilesystemSandbox()` para qualquer leitura/escrita |
| 5 | Reprodutível em ambiente limpo | Maintainer roda `pip install --require-hashes -r requirements.lock && python eval.py` e obtém mesmo `metrics.json` (módulo seeds) |
| 6 | `report.md` documentando decisões | Seções: chunking, modelo escolhido, decisão de top-k, lost-in-middle mitigation, trade-offs |
| 7 | Sem hardcoded secrets | gitleaks limpo |
| 8 | Roda offline com mock OU caminho OSS | `--provider mock` e/ou `--provider ollama` funcionam |

## Crédito extra (não bloqueante)

| # | Critério | Reconhecimento |
|---|----------|---------------|
| A | Hybrid retrieval (BM25 + densa) com ablation | Mention em `REVISORES.md` |
| B | Reranker fine-tuned local | — |
| C | Análise de erros qualitativa por categoria | — |

## Anti-patterns que invalidam

- ❌ Chamadas à API que ignoram `--require-hashes` lockfile.
- ❌ Solução que só funciona com 1 modelo (não testou com low-cost).
- ❌ `eval.py` que não é determinístico (resultados variam entre runs).
- ❌ Citações placebo (regex bate mas link aponta para abstract errado).

## Como o maintainer revisa

1. Clona o fork em ambiente limpo.
2. `pip install --require-hashes -r requirements.lock`.
3. `python eval.py` — confere `metrics.json` numericamente vs. `report.md`.
4. Code review: sandbox, tratamento de erro, anti-patterns.
5. Roda com modelo low-cost (não só frontier) para validar critério de robustez.
6. Aprovado: comenta no PR e merge para `projetos/P1/submissions/<handle>/`.
