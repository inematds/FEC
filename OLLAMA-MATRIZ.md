# OLLAMA-MATRIZ — Caminho gratuito (OSS local) por lab

> _Hardware mínimo testado para cada módulo. PLAN itens 52-54._

## Modelos OSS pinados (v1.0.0)

Ver fonte canônica em [`evals/v1/models.json`](./evals/v1/models.json) (papel `oss`).

- **Default:** `qwen2.5-7b-instruct@q4_K_M` — 16 GB RAM mínimo, sem GPU.
- **Alternativas testadas:** Llama-3.1-8B-instruct (q4), Mistral-7B-instruct (q4).

## Matriz por trilha

| Trilha / módulo | Modelo OSS | RAM mínima | GPU? | Lab roda 100% offline? | Notas |
|-----------------|-----------|-----------|-----|------------------------|-------|
| T1.1 Janela e atenção | qwen2.5-7b q4 | 16 GB | não | ✅ | Demonstração visual; precisão não crítica. |
| T1.2 Tokens, custo | qwen2.5-7b q4 | 16 GB | não | ✅ | Tokenizer offline funciona em qualquer modelo. |
| T2.1 Estrutura mensagem | qwen2.5-7b q4 | 16 GB | não | ✅ | |
| T2.2 Versionamento prompt | qwen2.5-7b q4 | 16 GB | não | ✅ | Eval primer roda local. |
| T3.1 Indexação (chunking, embeddings) | bge-large-en-v1.5 | 8 GB | não | ✅ | Embeddings local; indexação 100% offline. |
| T3.2 Reranking | qwen2.5-7b + bge-reranker | 16 GB | não | ✅ | Reranker leve. |
| T3.3 RAG agêntico (beta) | qwen2.5-7b q4 | 16 GB | não | ⚠️ | Rodável, mas qualidade limitada — recomendado API paga. |
| T4.1 Tool calling | qwen2.5-7b instruct | 16 GB | não | ✅ | Suporte a tools nativo no qwen2.5. |
| T4.2 Agentes single | qwen2.5-7b q4 | 16 GB | não | ⚠️ | OK para protótipos; produção exige modelo maior. |
| T4.3 Multi-agente / MCP (beta) | llama-3.1-70b q4 | 48 GB OU GPU 24 GB | recomendado | ❌ | OSS local na prática só com GPU 24GB+; **lab oferece simulação por gravação em `fixtures/recorded/`**. |
| T5.1 Memória | qwen2.5-7b q4 | 16 GB | não | ✅ | Summarização hierárquica funciona. |
| T5.2 Caching (beta) | — | — | — | ❌ | **Sem caching nativo em OSS local.** Lab usa simulação por gravação ou exige API paga. |
| T6.1 Evals | qwen2.5-7b + judge model | 24 GB | recomendado | ⚠️ | Judge ideal é frontier; OSS local roda mas com bias documentado. |
| T6.2 Produção (beta) | qwen2.5-7b q4 | 16 GB | não | ✅ | Tracing/logging são lib-side, não dependem do modelo. |

## Capacidades NÃO disponíveis em OSS local

| Capacidade | Provider | Workaround |
|-----------|---------|-----------|
| Long context >128k confiável | qualquer OSS local 2026-Q2 | API paga OU truncar para 32k |
| Prompt caching nativo | qualquer OSS local | Simulação por gravação em `fixtures/recorded/` |
| Tool calling avançado robusto | OSS pequenos | qwen2.5 OK; modelos &lt;7B falham |
| MCP nativo | qualquer OSS local | Adapter manual |

## Programas de créditos (alternativa)

Quem não tem hardware E não quer pagar pode tentar programas de créditos:

- **Anthropic** — créditos iniciais para novos developers.
- **OpenAI** — créditos free tier (verificar elegibilidade).
- **Google AI Studio** — tier gratuito generoso (Gemini Flash).

Cobertura desses programas não é garantida — verificar no momento de fazer o lab.

## Como configurar Ollama

```bash
# 1. Instalar (Linux/macOS)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Baixar o modelo default
ollama pull qwen2.5:7b-instruct-q4_K_M

# 3. Verificar
ollama run qwen2.5:7b-instruct-q4_K_M "olá, teste"

# 4. Apontar fec_sdk para Ollama local
from fec_sdk.adapters import get_adapter
client = get_adapter("ollama", model="qwen2.5:7b-instruct-q4_K_M")
```

Detalhes específicos do Ollama em [ollama.ai/docs](https://ollama.ai).

## Reportar incompatibilidade

Modelo OSS não roda no hardware listado? Abrir issue com label `ollama` + ambiente exato.
