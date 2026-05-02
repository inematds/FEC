# Modelos pinados em smoke (`auto-smoke`, `production-smoke`)

> _⚠️ Source-of-truth canônica: [`models.json`](./models.json). Este Markdown é referência humana — para automação, use o JSON._

Smoke tests usam exatamente os modelos pinados em `models.json` para o release atual. Mudança aqui exige bump em `HASHES.lock` (item 28a).

## Pins atuais (v1.0.0)

| Papel | Provedor | ID | Pinado em | Janela de contexto |
|-------|----------|-----|-----------|-------------------|
| Frontier | anthropic | claude-sonnet-4-6@2026-04 | 2026-05-02 | 200k |
| Low-cost | openai | gpt-5-mini@2026-04 | 2026-05-02 | — |
| OSS | ollama | qwen2.5-7b-instruct@q4_K_M | 2026-05-02 | 32k |

## Política

- **`auto-smoke`** (Tier A): roda nos 3 modelos diariamente; budget `$0.50/dia × 3 = ~$30/mês`.
- **`production-smoke`** (Tier B): roda nos 3 modelos antes de cada release; budget `$5/run × ≤4/release = ≤$20/mês`.
- Modelo deprecado pelo provedor: `MODELOS.md` (gerado de `models.json`) marca; exemplos antigos continuam executáveis via `fixtures/recorded/<modelo>/` por 12 meses (item 84).
