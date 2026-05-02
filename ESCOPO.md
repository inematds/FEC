# ESCOPO — Formação de Engenharia de Contexto

Este documento delimita explicitamente o que está **dentro** e o que está **fora** da v1.0 da FEC. Existe para alinhar expectativa antes da matrícula e guiar decisões editoriais.

---

## Persona-alvo

Engenheiro de software ou ML que vai colocar agente baseado em LLM em produção. Marcado por nível em cada módulo:

- 🔧 **builder solo** — pessoa única construindo MVP/protótipo.
- 🧱 **eng. de produto** — integrando LLM em produto existente.
- 🏗️ **eng. de plataforma** — desenhando infra para times consumirem.

**NÃO é o curso para você se:**
- nunca chamou uma API LLM via HTTP/SDK (vá para curso introdutório primeiro).
- procura "vibe coding" ou marketing de IA.
- quer aprender a usar ChatGPT como usuário final.

---

## Dentro do escopo (v1.0)

### Conteúdo técnico
- Anatomia da janela de contexto, atenção, "lost in the middle", tokenização, custo.
- System prompt, few-shot, chain-of-thought, formato XML/JSON, ancoragem, versionamento de prompt.
- RAG: chunking, embeddings, BM25/híbrido, reranking, *contextual retrieval*, citações, grounding.
- Tool/function calling provider-neutral; agentes single (ReAct, planner/executor); MCP (beta).
- Memória curto/longo prazo, summarização hierárquica, prompt caching e context distillation (beta).
- Avaliação: golden sets, LLM-as-judge e seus vieses, tracing, prompt injection (sandboxed), custo.

### Práticas de engenharia
- Harness de avaliação congelado e content-addressed (`evals/v1/`).
- Padrões provider-neutral primeiro; adaptadores Anthropic/OpenAI/OSS apenas onde necessário.
- Sandbox obrigatório para tools que tocam filesystem/rede/processo.
- Exercícios com teste automatizado (`pytest`).
- Bibliografia datada com ≥10 referências por trilha.
- Seção "Quando NÃO usar" em todo padrão.

### Projetos cumulativos GA
- **P1** — Buscador citável (RAG sobre ArXiv abstracts).
- **P2** — Agente com tools (busca + cálculo + leitura).
- **P5** — Pipeline em produção (evals + tracing + defesa contra injection).

---

## Fora do escopo (v1.0) — explicitamente

| Tópico | Por que está fora |
|--------|-------------------|
| **Fine-tuning extensivo** | Cobrimos só onde **substitui** contexto; SFT/RLHF/DPO em profundidade são curso separado. |
| **Pré-treinamento ou treinamento do zero** | Fora — escopo é uso/integração de modelos existentes. |
| **Filosofia de IA, AGI, ética abstrata** | Fora — curso é técnico. Segurança aplicada (injection, exfil) está dentro. |
| **"Gurus de prompt" sem evidência** | Fora — toda alegação de ganho roda no harness ou cita paper datado. |
| **Curso de Python ou de APIs HTTP** | Fora — pré-requisito (ver `PRE-REQUISITOS.md`). |
| **Comparação qualitativa de provedores** | Fora sem run no harness — ranking baseado em opinião está banido. |
| **Vendor-specific deep dive** sozinho | Fora — padrão neutro vem primeiro; provedor canônico é exemplo, não foco. |
| **UI/UX de chatbots, frontend de chat** | Fora — escopo é o lado da contexto/inferência. |
| **Construção de modelos de embedding do zero** | Fora — usamos modelos existentes; comparação por benchmark, não treino. |
| **LangChain/LangGraph como pré-requisito** | Frameworks são opcionais e fixados por versão; preferimos SDK puro. |
| **Recomendação de produtos pagos específicos** | Fora — neutralidade editorial; menções factuais, não endosso. |

---

## Política anti-hype

- **Termos banidos:** "definitivo", "tudo o que você precisa", "última fronteira", "revoluciona", "10x developer".
- **Permitido:** declarações factuais com link para evidência (paper, run no harness, RFC).
- **Comparações:** sempre baseadas em harness (`evals/v1/runs/<id>`) ou paper citado com data e delta replicado.

---

## O que muda da v1.0 para versões futuras

Tracks **beta** (3.3 RAG agêntico, 4.3 multi-agente/MCP, 5.2 caching avançado, 6.2 produção avançada) saem com aviso `beta` na v1.0. Promoção para GA exige:

1. ≥2 revisores externos assinando em `REVISORES.md`.
2. Bateria de exercícios estável por ≥3 meses.
3. Harness com modelos atualizados.

Projetos opcionais **P3** (Sistema multi-agente) e **P4** (Memória que escala) ficam em `projetos/post-launch/` — não bloqueiam v1.0.

---

## Contato editorial

Sugestões de mudança de escopo: abrir issue com label `escopo` + RFC em PR. Maintainers triam semanalmente.
