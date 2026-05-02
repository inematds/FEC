# MODELOS — Pinned por release

> _⚠️ **Gerado de `evals/v1/models.json`.** NÃO edite manualmente — mudanças no MD são sobrescritas. Edite o JSON via PR (CODEOWNERS protege)._

**Release:** v1.0.0 · **Pinado em:** 2026-05-02

| Papel | Provedor | ID | Janela | Notas |
|-------|----------|-----|--------|-------|
| frontier | anthropic | `claude-sonnet-4-6@2026-04` | 200000 | Modelo de raciocínio principal para alegações de qualidade no harness. Pinar exato com data. |
| low_cost | openai | `gpt-5-mini@2026-04` | — | Modelo de baixo custo para comparações de cost-effectiveness. |
| oss | ollama | `qwen2.5-7b-instruct@q4_K_M` | 32768 | OSS local rodável em 16GB RAM. Caminho 'free path' (item 52 do PLAN). |

## Política

- IDs incluem data de pinagem (ex.: `claude-sonnet-4-6@2026-04`).
- Modelo deprecado pelo provedor: continua executável via `fixtures/recorded/<modelo>/` por 12 meses.
- Mudança aqui exige bump em `evals/v1/HASHES.lock` (PLAN item 28a).
