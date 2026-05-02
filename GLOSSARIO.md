# GLOSSÁRIO — Formação de Engenharia de Contexto

> _Termos derivados dos módulos via `scripts/build-glossary.py`. Cada entrada deve ter ≥1 backlink de módulo. PLAN item 37._

## A

**Atenção causal** — Mecanismo onde cada token só "olha" tokens anteriores; base do transformer autoregressivo.
*Backlinks:* T1.1.

**Ancoragem** — Padrão de repetir a pergunta antes E depois do contexto recuperado, para mitigar "lost in the middle".
*Backlinks:* T1.1, T2.1.

**Adapter** — No `fec_sdk`, a camada que traduz a interface neutra para o formato específico de um provedor (Anthropic, OpenAI, Ollama).
*Backlinks:* T1.2 (exemplos), T2.1.

## B

**BPE (Byte-Pair Encoding)** — Algoritmo de tokenização sub-palavra usado por GPT, Claude, e muitos OSS. Quebra texto em unidades sub-lexicais aprendidas.
*Backlinks:* T1.1, T1.2.

**BM25** — Algoritmo clássico de ranking sparse. Usado em RAG híbrido junto com embeddings densos.
*Backlinks:* T3.1, T3.2.

## C

**Contextual retrieval** — Padrão Anthropic 2024 que adiciona contexto ao chunk antes de embedar/indexar, melhorando recall.
*Backlinks:* T3.1, T3.2.

**CSP (Content Security Policy)** — Política de segurança em headers/meta HTTP que restringe origens de scripts, frames, etc.
*Backlinks:* (infra; PLAN item 34a).

## E

**Eval primer** — Disciplina ensinada em T2.2 de que toda mudança de prompt entra com mini-eval contra golden set.
*Backlinks:* T2.2, T6.1.

**Embedding (densa)** — Representação vetorial de texto produzida por modelo treinado para similaridade semântica.
*Backlinks:* T3.1.

## F

**Few-shot** — Padrão de incluir 2-N exemplos no prompt para guiar o modelo. Padrão estável (vai no início da janela).
*Backlinks:* T2.1.

## G

**Golden set** — Dataset fixado de exemplos com respostas esperadas, usado para medir qualidade ao longo do tempo. Em FEC: `evals/v1/datasets/`.
*Backlinks:* T6.1, P1, P5.

**Groundedness** — Métrica de quanto da resposta está suportada por fontes citadas.
*Backlinks:* T3.2, P1.

## J

**Janela de contexto** — Sequência total de tokens que o modelo recebe em uma chamada. Inclui system, few-shot, contexto recuperado, user turn, e turns anteriores serializados.
*Backlinks:* T1.1, T1.2.

**Janela efetiva vs nominal** — Diferença entre o tamanho aceito sem erro de API (nominal) e o tamanho onde qualidade se mantém (efetiva). Medida por benchmarks como RULER.
*Backlinks:* T1.2.

## K

**KV cache** — Cache dos estados key/value computados pelo modelo. Reutilizado entre chamadas com prefixo idêntico (base do prompt caching).
*Backlinks:* T1.1, T1.2, T5.2.

## L

**Lost in the middle** — Fenômeno (Liu et al. 2023) onde acurácia degrada quando informação crítica está no meio da janela; permanece alta no início e fim.
*Backlinks:* T1.1.

**LLM-as-judge** — Padrão de usar um modelo para avaliar saída de outro modelo. Tem vieses documentados (favoritismo a outputs longos, bias de posição).
*Backlinks:* T6.1.

## M

**MCP (Model Context Protocol)** — Protocolo Anthropic 2024 para integração de tools/recursos externos com modelos.
*Backlinks:* T4.3 (beta).

**Multi-agente** — Padrão onde 2+ agentes (orquestrador + trabalhadores) cooperam em uma tarefa. Trade-off de custo vs. capacidade vs. confiabilidade.
*Backlinks:* T4.3 (beta), P3 (post-launch).

## P

**Prompt caching** — Cache de prefixo de prompt no provedor; tokens cacheados custam ~10% do preço normal. Anthropic e OpenAI oferecem; Ollama não nativo.
*Backlinks:* T1.2, T5.2 (beta).

**Provider-neutral** — Princípio editorial da FEC: padrões ensinados em forma agnóstica primeiro, depois realização concreta em provedor canônico do módulo.
*Backlinks:* (todos os módulos via `fec_sdk`).

## R

**ReAct** — Padrão de agente onde o modelo alterna entre Reason (raciocínio) e Act (chamada de tool) em loop.
*Backlinks:* T4.2.

**Reranking** — Etapa que reordena candidatos recuperados por um retrieval inicial, usando modelo mais caro/preciso.
*Backlinks:* T3.2.

**RoPE (Rotary Position Embedding)** — Esquema de codificação de posição usado pela maioria dos LLMs modernos (Su et al. 2021).
*Backlinks:* T1.1.

**RAG (Retrieval-Augmented Generation)** — Padrão de recuperar documentos relevantes e adicionar ao contexto antes da geração.
*Backlinks:* T3.1, T3.2, T3.3 (beta), P1.

## S

**Sandbox** — Em FEC, o ambiente jailed (`fec_sdk/sandbox/`) onde tools com side-effect rodam. Bateria `tests/sandbox/test_traversal.py` é gate de GA.
*Backlinks:* (P2, P5; PLAN item 62a).

**SentencePiece** — Biblioteca de tokenização (Kudo & Richardson 2018), base de muitos tokenizers modernos.
*Backlinks:* T1.1, T1.2.

**Spotlight (Anthropic 2024)** — Padrão de defesa contra indirect injection que delimita explicitamente conteúdo recuperado de instrução do usuário.
*Backlinks:* T6.1, P5.

## T

**Token** — Unidade sub-palavra produzida pelo tokenizer; unidade de cobrança e medida de janela.
*Backlinks:* T1.1, T1.2.

**Tool calling** — Mecanismo do modelo invocar funções estruturadas via JSON. Provider-neutral em `fec_sdk`.
*Backlinks:* T4.1, T4.2.

**TTFT (Time To First Token)** — Latência entre o request e o primeiro token gerado. Dominado por prefill em janelas longas.
*Backlinks:* T1.2.

---

> _Última geração: 2026-05-02. Para regenerar a partir dos módulos: `python scripts/build-glossary.py`._
