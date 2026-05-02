# CAPACIDADES — Por provedor

> _⚠️ **Gerado de `evals/v1/capabilities.json`.** NÃO edite manualmente — mudanças no MD são sobrescritas. Edite o JSON via PR (CODEOWNERS protege)._

**Status:** `native` (suporte direto), `adapter` (via `fec_sdk`), `mock` (simulação por gravação), `not_supported`.

## Tool / function calling (`tool-calling`)

Modelo invoca ferramentas estruturadas via JSON.

_Ensinado em:_ `modulo-4-1`

| Provedor | Status | Notas |
|----------|--------|-------|
| anthropic | native |  |
| openai | native |  |
| google | native |  |
| ollama | adapter | Suporte recente; verificar modelo específico. |

## Prompt caching (`prompt-caching`)

Reuso de prefixo de contexto entre requests para reduzir custo/latência.

_Ensinado em:_ `modulo-5-2`

| Provedor | Status | Notas |
|----------|--------|-------|
| anthropic | native |  |
| openai | adapter | Equivalente parcial via cached prompts. |
| google | adapter |  |
| ollama | mock | Sem caching nativo; lab usa simulação por gravação. |

## Long context (>200k tokens) (`long-context`)

Janela de contexto extensa.

_Ensinado em:_ `modulo-1-2`, `modulo-3-2`

| Provedor | Status | Notas |
|----------|--------|-------|
| anthropic | native |  |
| openai | native |  |
| google | native |  |
| ollama | not_supported | OSS local 2026-Q2 raramente >128k confiável. |

## Model Context Protocol (`mcp`)

Protocolo para integração de tools/recursos externos.

_Ensinado em:_ `modulo-4-3`

| Provedor | Status | Notas |
|----------|--------|-------|
| anthropic | native |  |
| openai | adapter |  |
| google | adapter |  |
| ollama | adapter |  |

