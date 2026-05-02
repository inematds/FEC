"""Especificação dos 14 módulos da FEC v1.0.

Estrutura de cada módulo é consumida por scripts/build-modulos.py.
Atualizar aqui regenera o HTML.
"""

from __future__ import annotations

TRILHAS = {
    1: {"nome": "Fundamentos de Contexto", "cor": "emerald", "emoji": "🧠"},
    2: {"nome": "Engenharia da Mensagem",   "cor": "blue",    "emoji": "✉️"},
    3: {"nome": "RAG e Recuperação",        "cor": "purple",  "emoji": "📚"},
    4: {"nome": "Tools, Agentes e Multi-Agente", "cor": "amber", "emoji": "🛠️"},
    5: {"nome": "Memória e Compressão",     "cor": "teal",    "emoji": "💾"},
    6: {"nome": "Avaliação e Produção",     "cor": "rose",    "emoji": "📊"},
}

MODULOS = [
    # =================== T1 — FUNDAMENTOS ===================
    {
        "id": "modulo-1-1", "trilha": 1, "numero": "1.1", "status": "GA",
        "titulo": "Janela de contexto, atenção e \"lost in the middle\"",
        "emoji": "🪟",
        "descricao": "A anatomia operacional da janela: o que é atenção, por que tokens no meio são esquecidos, e como isso muda decisões de engenharia.",
        "minutos": 60, "nivel": "Básico", "tipo": "Teoria",
        "introducao": (
            "Engenharia de contexto começa com uma realização operacional: o modelo NÃO recebe uma 'conversa'; "
            "ele recebe uma sequência fixa de tokens — a <strong class='text-emerald-400'>janela de contexto</strong>. "
            "O system prompt, o histórico, o resultado de uma busca RAG, o turn atual e até as saídas anteriores, "
            "tudo é serializado nessa mesma sequência. Quem decide a ordem, a estrutura e o que entra é você."
        ),
        "topicos": [
            {
                "emoji": "🪟", "titulo": "A janela é o ambiente físico do modelo", "subtitulo": "Tokens, não conversas",
                "o_que_e": "Sequência fixa de tokens que o modelo lê em uma chamada. System prompt + histórico + contexto recuperado + user turn — tudo junto.",
                "por_que": "Sem essa visão, você assume que o modelo tem 'memória da conversa'. Não tem — você reconstrói a cada chamada.",
                "conceitos": "Janela nominal, janela efetiva, ordem de seções, custo do input total."
            },
            {
                "emoji": "🎯", "titulo": "Atenção causal e KV cache", "subtitulo": "O mecanismo que pesa tokens",
                "o_que_e": "Cada token só 'olha' tokens anteriores. Estados intermediários (KV cache) podem ser reutilizados — base do prompt caching.",
                "por_que": "Entender KV cache explica por que prefixos estáveis no início têm custo amortizado e por que mexer no system prompt invalida cache da sessão.",
                "conceitos": "Self-attention, causal mask, KV cache, attention heads, prefix prefill."
            },
            {
                "emoji": "📍", "titulo": "Posição: rotary embeddings e o efeito recência", "subtitulo": "Por que tokens recentes têm vantagem",
                "o_que_e": "Modelos modernos codificam posição via Rotary Position Embeddings (RoPE). Tokens recentes têm vantagem estrutural; tokens iniciais têm vantagem de fixação.",
                "por_que": "Esse é o mecanismo concreto por trás do 'lost in the middle'. Tokens no meio simplesmente não têm vantagem estrutural nenhuma.",
                "conceitos": "RoPE (Su et al. 2021), prefix bias, recency bias, position interpolation."
            },
            {
                "emoji": "📜", "titulo": "Lost in the middle (Liu et al. 2023)", "subtitulo": "A curva U de atenção",
                "o_que_e": "Em testes controlados, acurácia de QA cai até 30% quando a informação crítica está no meio da janela. Permanece alta no início e fim.",
                "por_que": "RAG ingênuo coloca 50 documentos esperando que o modelo dê peso uniforme. Não dá. Precisa rerankear ou recuperar menos.",
                "conceitos": "Curva U, U-shape attention, mitigação por reranking, ancoragem."
            },
            {
                "emoji": "🧭", "titulo": "Ordem das seções: estável → variável → instrução", "subtitulo": "O padrão que casa atenção e cache",
                "o_que_e": "System prompt e few-shot fixos primeiro (estáveis, cacheáveis), contexto recuperado depois (variável), instrução do usuário no fim (atenção máxima).",
                "por_que": "Esta ordem maximiza cache hit rate (Anthropic 2024) e coloca a instrução do usuário na posição mais 'atendida' pelo modelo.",
                "conceitos": "Prefix stability, cache breakpoints, instruction-at-the-end pattern, ancoragem."
            },
            {
                "emoji": "📏", "titulo": "Janela nominal vs. efetiva", "subtitulo": "200k de marketing ≠ 200k de qualidade",
                "o_que_e": "Janela nominal é o que o modelo aceita sem erro de API. Janela efetiva é onde a qualidade se mantém. Frequentemente bem menor (RULER, Hsieh et al. 2024).",
                "por_que": "Decidir 'cabe' e 'funciona bem' são duas perguntas diferentes. A segunda exige eval no harness.",
                "conceitos": "Effective context length, needle-in-a-haystack, RULER benchmark."
            },
        ],
        "conceito_principal": {
            "emoji": "💡", "titulo": "Janela de contexto: a unidade fundamental de engenharia",
            "texto": "Pense no modelo como uma função pura: recebe uma string (a janela serializada) e devolve uma string (a saída). Tudo o que muda no comportamento mora nessa string de entrada — system prompt, exemplos, contexto recuperado, ordem. Não há 'memória' fora dela.",
            "lista": [
                "Você decide o que entra e em que ordem.",
                "Cada token de entrada custa, mesmo se o modelo 'ignora' por atenção baixa.",
                "Mudanças no início da janela invalidam cache; mudanças no fim, não."
            ]
        },
        "dados_pesquisa": {
            "titulo": "Liu et al. (2023) — Lost in the Middle (ArXiv:2307.03172)",
            "items": [
                "<strong>30%</strong> — queda média de acurácia quando info crítica está no meio.",
                "<strong>U-shape</strong> — curva replicada em modelos de janela 4k até 32k+.",
                "<strong>Mitigação validada:</strong> reranking + recuperar menos resolvem na prática."
            ]
        },
        "dica_pratica": {
            "emoji": "🎯", "titulo": "Heurística rápida",
            "texto": "Antes de aumentar a janela, pergunte: o modelo precisa de TODO esse contexto, ou só de 3-5 trechos relevantes? Reranking + top-5 quase sempre bate 'jogar 50 docs'."
        },
        "fazer_evitar": [
            ("Manter system prompt e few-shot estáveis no início (cacheáveis)", "Mexer no system prompt a cada turn (invalida cache)"),
            ("Rerankear documentos antes de incluir no contexto", "Concatenar 50 docs sem ordem e esperar que o modelo encontre"),
            ("Repetir a pergunta antes E depois do contexto (ancoragem)", "Colocar a pergunta só no início, longe do fim atendido"),
            ("Medir janela efetiva no harness (eval)", "Confiar que '200k = 200k' funciona igual"),
        ],
        "quando_nao_usar": [
            "<strong>Tarefas pontuais e estruturadas</strong> (classificação binária, extração de campo único): system prompt curto + user turn é suficiente.",
            "<strong>Quando RAG resolve</strong>: 3-5 documentos relevantes batem 50 documentos despejados.",
            "<strong>Quando latência importa</strong>: 100k tokens adicionam centenas de ms de prefill mesmo com cache.",
            "<strong>Modelos OSS pequenos</strong>: janela efetiva raramente passa 8-16k mesmo se anunciada como 32k+.",
        ],
        "exemplo_codigo": (
            "from fec_sdk import Message, MessageRole, check_compat\n"
            "from fec_sdk.adapters import get_adapter\n\n"
            "check_compat(\"modulo-1-1\", expected_sdk_version=\">=1.0,<2.0\")\n\n"
            "client = get_adapter(\"mock\", scripted=[(\"Liu\", \"Posição 12 (meio)\")])\n\n"
            "doc_relevante = \"FATO: a janela do modelo X é 200000 tokens.\"\n"
            "ruido = \"\\n\".join(f\"Doc {i}: lorem ipsum...\" for i in range(20))\n\n"
            "# Doc relevante NO MEIO — prejudicial\n"
            "contexto = ruido + \"\\n\" + doc_relevante + \"\\n\" + ruido\n\n"
            "resp = client.chat([\n"
            "    Message(role=MessageRole.SYSTEM, content=\"Responda apenas com fatos do contexto.\"),\n"
            "    Message(role=MessageRole.USER, content=f\"{contexto}\\n\\nQual a janela do modelo X?\"),\n"
            "])\n"
            "print(resp.content)"
        ),
        "exercicio": "Em <code>exercicios/modulo-1-1/</code> você recebe 5 cenários onde o doc relevante está no meio. Sua função <code>reordenar(documentos)</code> deve aplicar uma das mitigações ensinadas e fazer ≥4/5 casos passarem. Rode <code>pytest exercicios/modulo-1-1/test.py</code>.",
        "bibliografia": [
            ("Liu et al. (2023)", "Lost in the Middle: How Language Models Use Long Contexts", "https://arxiv.org/abs/2307.03172"),
            ("Su et al. (2021)", "RoFormer: Enhanced Transformer with Rotary Position Embedding", "https://arxiv.org/abs/2104.09864"),
            ("Hsieh et al. (2024)", "RULER: What's the Real Context Size of your Long-Context LMs?", "https://arxiv.org/abs/2404.06654"),
            ("Anthropic (2024)", "Prompt caching with Claude", "https://docs.anthropic.com"),
        ],
        "resumo": [
            "<strong>Janela de contexto</strong> é a unidade operacional — sequência fixa de tokens.",
            "<strong>Atenção é não-uniforme</strong> — início e fim atendem mais que o meio.",
            "<strong>Lost in the middle</strong> documentado: até 30% de queda quando info está no meio.",
            "<strong>Ordem importa</strong>: estável→variável→instrução maximiza cache e atenção.",
            "<strong>Janela nominal ≠ efetiva</strong> — meça no harness antes de assumir.",
        ],
        "proximo_id": "modulo-1-2",
        "proximo_titulo": "Tokens, custo e limites práticos",
    },

    {
        "id": "modulo-1-2", "trilha": 1, "numero": "1.2", "status": "GA",
        "titulo": "Tokens, custo e limites práticos por modelo",
        "emoji": "🔢",
        "descricao": "Como contar tokens, estimar custo antes de chamar a API, e escolher entre frontier / low-cost / OSS para o caso certo.",
        "minutos": 55, "nivel": "Básico", "tipo": "Prático",
        "introducao": (
            "Engenharia de contexto sem cálculo de custo é wishful thinking. "
            "Cada provedor tem um tokenizer próprio, cada modelo tem um preço diferente, "
            "e a diferença entre frontier e low-cost pode ser de <strong class='text-emerald-400'>50× no custo</strong> por 1M tokens. "
            "Aqui você aprende a estimar antes de pagar — e a escolher o modelo certo para a tarefa."
        ),
        "topicos": [
            {
                "emoji": "🔤", "titulo": "Tokenização: BPE e SentencePiece", "subtitulo": "Por que tokens ≠ palavras",
                "o_que_e": "BPE/SentencePiece quebram texto em unidades sub-palavra aprendidas. 'engenharia' pode virar 3 tokens; 'engineering' pode virar 1.",
                "por_que": "Estimativa de custo precisa do tokenizer correto. Heurísticas universais ('1 token ≈ 4 chars') falham em PT-BR (~3 chars/token), código e emoji.",
                "conceitos": "BPE (Sennrich 2016), SentencePiece (Kudo 2018), vocabulário, multi-byte tokens, UNK."
            },
            {
                "emoji": "💰", "titulo": "Custo: input vs. output (cuidado com a ratio)", "subtitulo": "Output é caro mas input é volume",
                "o_que_e": "Output tokens custam 3-5× mais que input. Mas em janelas longas, você gasta mais em input total porque ele é grande.",
                "por_que": "Otimização incorreta — tentar reduzir output enquanto a janela está inflada — não move custo significativamente.",
                "conceitos": "Pricing por 1M tokens, ratio input/output, batch discounts, prompt caching."
            },
            {
                "emoji": "🏗️", "titulo": "Os três níveis de modelo", "subtitulo": "Frontier, low-cost, OSS local",
                "o_que_e": "Frontier (~$3-15/M): raciocínio complexo, contexto grande. Low-cost (~$0.10-0.30/M): volume alto, classificação. OSS local: $0/chamada, hardware-bound.",
                "por_que": "Engenheiros pulam direto para frontier por inércia. Em volume, isso queima orçamento sem ganho.",
                "conceitos": "Capability vs. context vs. cost, model routing, hierarchical inference."
            },
            {
                "emoji": "⏱️", "titulo": "Latência: prefill vs. decode", "subtitulo": "TTFT em janelas longas",
                "o_que_e": "Prefill é o tempo para o modelo 'ler' o input. Decode é o tempo de geração. Janela longa = prefill longo = TTFT (time-to-first-token) grande.",
                "por_que": "Para UX de chat ao vivo, prefill domina o 'tempo até primeiro token'. Cache reduz drasticamente — entender isso é entender UX real.",
                "conceitos": "TTFT, tokens/sec, KV cache reuse, streaming."
            },
            {
                "emoji": "🔁", "titulo": "Prompt caching: como obter desconto real", "subtitulo": "10% do preço para tokens cacheados",
                "o_que_e": "Anthropic e OpenAI oferecem cache de prefixo. Tokens cacheados custam ~10% do preço normal de input.",
                "por_que": "Em chat com system prompt + few-shot grandes, cache pode reduzir custo de input em 80-90%. Detalhado em T5.2.",
                "conceitos": "Cache breakpoint, TTL, hit rate, prefix stability."
            },
            {
                "emoji": "🆓", "titulo": "OSS local: a matriz de hardware", "subtitulo": "O que cabe na sua máquina",
                "o_que_e": "Qwen2.5-7B q4 cabe em 16GB RAM. Llama-3.1-8B-instruct também. Modelos >13B exigem GPU. Detalhes em <code>OLLAMA-MATRIZ.md</code>.",
                "por_que": "O caminho gratuito do curso usa OSS — entenda o que cabe antes de tentar T4.3 (multi-agente).",
                "conceitos": "Quantização (q4, q5, q8), VRAM/RAM, throughput CPU vs. GPU, vLLM."
            },
        ],
        "conceito_principal": {
            "emoji": "🧮", "titulo": "Estimar custo ANTES de chamar",
            "texto": "Use o tokenizer offline do provedor para calcular tokens de uma chamada antes de mandar. Custos não-triviais devem ser orçados, não chutados.",
            "lista": [
                "Anthropic: <code>client.messages.count_tokens()</code> ou Anthropic Tokenizer.",
                "OpenAI: biblioteca <code>tiktoken</code> roda local sem chamar API.",
                "Google: <code>model.count_tokens()</code> também local.",
                "OSS: tokenizer do HuggingFace (<code>AutoTokenizer.from_pretrained</code>)."
            ]
        },
        "dados_pesquisa": {
            "titulo": "Comparação real de custo (2026-Q2, ordens de grandeza)",
            "items": [
                "<strong>Frontier (ex: Claude Sonnet 4.6):</strong> ~$3 input / $15 output por 1M tokens.",
                "<strong>Low-cost (ex: GPT-5 mini):</strong> ~$0.15 input / $0.60 output por 1M tokens.",
                "<strong>Cache hit (Anthropic):</strong> 10% do preço normal — economiza 90%.",
                "<strong>OSS local (qwen2.5-7b):</strong> $0 por chamada (custo de hardware amortizado).",
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Regra dos 80%",
            "texto": "Se a tarefa é estruturada (classificação, extração) E o input cabe em &lt;8k tokens, low-cost ou OSS resolvem 80% dos casos com 1/20 do custo. Só vá para frontier quando precisar do reasoning."
        },
        "fazer_evitar": [
            ("Estimar tokens com tokenizer offline antes de mandar", "Chutar 'mais ou menos' o tamanho da janela"),
            ("Usar low-cost para tarefas estruturadas em volume", "Mandar tudo para frontier por inércia"),
            ("Habilitar prompt caching em chats com prefixo grande", "Reescrever o system prompt a cada turn (invalida cache)"),
            ("Pinar versão exata do modelo (com data)", "Apontar para apelido genérico que pode mudar"),
        ],
        "quando_nao_usar": [
            "<strong>Quando a chamada é única ou rara</strong>: custo total é trivial; gaste seu tempo em qualidade, não em centavos.",
            "<strong>Em prototipagem inicial</strong>: use frontier para estabelecer o teto de qualidade; otimize depois.",
            "<strong>Quando otimização frita qualidade</strong>: trocar frontier por low-cost que cai groundedness em 20% NÃO é economia.",
            "<strong>Quando privacidade exige local</strong>: custo deixa de ser o critério; OSS é a única opção.",
        ],
        "exemplo_codigo": (
            "from fec_sdk import check_compat\n"
            "check_compat(\"modulo-1-2\", expected_sdk_version=\">=1.0,<2.0\")\n\n"
            "# Estimativa local — sem chamar API\n"
            "system_prompt = \"Você é um assistente conciso.\"\n"
            "user_query = \"Resuma este texto em 3 bullets.\"\n"
            "contexto = open(\"documento.txt\").read()\n\n"
            "# PT-BR: ~3 chars/token (use tokenizer real do provedor para precisão)\n"
            "tokens_input  = (len(system_prompt) + len(user_query) + len(contexto)) // 3\n"
            "tokens_output = 200  # estimativa do tamanho da resposta\n\n"
            "# Frontier hipotético\n"
            "custo_frontier  = tokens_input * 3.00 / 1_000_000 + tokens_output * 15.00 / 1_000_000\n"
            "# Low-cost\n"
            "custo_low_cost  = tokens_input * 0.15 / 1_000_000 + tokens_output * 0.60 / 1_000_000\n\n"
            "print(f\"Frontier: ${custo_frontier:.4f} | Low-cost: ${custo_low_cost:.4f}\")"
        ),
        "exercicio": "Em <code>exercicios/modulo-1-2/</code>: dado um conjunto de chamadas LLM, decida qual modelo (frontier/low-cost/OSS) usar para minimizar custo mantendo qualidade. Teste em <code>pytest exercicios/modulo-1-2/test.py</code>.",
        "bibliografia": [
            ("Sennrich et al. (2016)", "Neural Machine Translation of Rare Words with Subword Units (BPE)", "https://arxiv.org/abs/1508.07909"),
            ("Kudo & Richardson (2018)", "SentencePiece: simple subword tokenizer", "https://arxiv.org/abs/1808.06226"),
            ("Hsieh et al. (2024)", "RULER: long-context benchmark", "https://arxiv.org/abs/2404.06654"),
            ("Anthropic (2024)", "Prompt caching with Claude", "https://docs.anthropic.com"),
        ],
        "resumo": [
            "<strong>Tokens não são palavras</strong> — use tokenizer do provedor para estimativa.",
            "<strong>Output 3-5× mais caro</strong> que input, mas input domina em janelas longas.",
            "<strong>Três níveis de modelo</strong>: frontier, low-cost, OSS — cada um para um caso.",
            "<strong>Prompt caching</strong> reduz input cacheado para 10% do preço.",
            "<strong>OSS local</strong> é viável para muitos labs do curso (ver OLLAMA-MATRIZ.md).",
        ],
        "proximo_id": "../trilha2/index.html",
        "proximo_titulo": "T2 — Engenharia da Mensagem",
    },

    # =================== T2 — ENGENHARIA DA MENSAGEM ===================
    {
        "id": "modulo-2-1", "trilha": 2, "numero": "2.1", "status": "GA",
        "titulo": "Estrutura da mensagem: system, few-shot, XML/JSON, ancoragem",
        "emoji": "✉️",
        "descricao": "A anatomia de um prompt bem-engenhado: 5 seções estáveis, formato declarativo, exemplos few-shot e por que ancoragem do user turn no fim importa.",
        "minutos": 55, "nivel": "Intermediário", "tipo": "Prático",
        "introducao": (
            "Engenheiros que mandam 'string solta' entregam resultados imprevisíveis. "
            "<strong class='text-blue-400'>Estrutura é a primeira alavanca de qualidade</strong> — antes de RAG, antes de tools, antes de eval. "
            "Aqui você aprende a anatomia: system prompt, few-shot, formato declarativo (XML/JSON), e o padrão 'instruction at the end'."
        ),
        "topicos": [
            {
                "emoji": "🎭", "titulo": "System prompt: persona e regras", "subtitulo": "O contrato do modelo",
                "o_que_e": "Mensagem do tipo 'system' que define persona, regras, formato de saída e restrições. Estável entre turns — alvo prioritário do prompt caching.",
                "por_que": "Sem system prompt explícito, o modelo improvisa o comportamento a cada chamada. Você perde controle e reprodutibilidade.",
                "conceitos": "Persona, role, regras, formato de saída, prompt cache anchor."
            },
            {
                "emoji": "📚", "titulo": "Few-shot: ensinando por exemplo", "subtitulo": "2-N exemplos canônicos",
                "o_que_e": "Padrão de incluir 2-N exemplos input→output no prompt para guiar o modelo. Funciona melhor que descrição abstrata para tarefas com formato específico.",
                "por_que": "In-context learning: o modelo extrapola do padrão dos exemplos. Para classificação, extração estruturada e tradução, few-shot consistentemente bate zero-shot.",
                "conceitos": "In-context learning, GPT-3 paper (Brown et al. 2020), exemplo canônico, ordem dos exemplos."
            },
            {
                "emoji": "🏷️", "titulo": "Formato declarativo: XML, JSON, Markdown", "subtitulo": "Tags que ancoram",
                "o_que_e": "Usar tags XML (<code>&lt;documento&gt;</code>, <code>&lt;pergunta&gt;</code>) ou JSON Schema declara seções e ajuda o modelo a separá-las.",
                "por_que": "Modelos modernos foram fine-tunados em prompts com estrutura. XML reduz confusão entre 'o que é instrução' e 'o que é dado'.",
                "conceitos": "XML tags, JSON Schema, structured outputs, delimitadores."
            },
            {
                "emoji": "📍", "titulo": "Ordem das seções: estável → variável → instrução", "subtitulo": "O padrão FEC",
                "o_que_e": "System prompt e few-shot fixos primeiro (cacheáveis); contexto recuperado depois (variável); instrução do usuário no fim.",
                "por_que": "Maximiza cache hit rate e coloca a pergunta na zona de atenção alta (recência).",
                "conceitos": "Cache stability, instruction-at-end, anchoring, prefix-suffix split."
            },
            {
                "emoji": "🪢", "titulo": "Ancoragem: repita a pergunta antes E depois", "subtitulo": "Mitigação contra lost-in-middle",
                "o_que_e": "Quando o contexto recuperado é grande, repetir a pergunta no início E no fim do bloco de contexto reduz a chance de o modelo esquecer.",
                "por_que": "Liu et al. (2023) mostra que info no meio é menos atendida. Ancoragem é uma das mitigações validadas.",
                "conceitos": "Anchoring, repetition prompt, query injection."
            },
            {
                "emoji": "🔧", "titulo": "Chain-of-thought: pensar antes de responder", "subtitulo": "Raciocínio explícito",
                "o_que_e": "Padrão de pedir ao modelo para 'pensar passo a passo' antes da resposta final. Tags como <code>&lt;raciocinio&gt;</code> antes de <code>&lt;resposta&gt;</code>.",
                "por_que": "Em problemas multi-passo (matemática, lógica), CoT melhora acurácia significativamente. Wei et al. (2022).",
                "conceitos": "CoT (Wei 2022), zero-shot CoT (Kojima 2022), reasoning models, scratchpad."
            },
        ],
        "conceito_principal": {
            "emoji": "🧱", "titulo": "Anatomia de uma mensagem bem-engenhada",
            "texto": "Toda mensagem tem 5 seções (algumas opcionais). Pensar nelas como blocos te dá controle sobre comportamento e custo.",
            "lista": [
                "<strong>1. System prompt</strong> — persona, regras (ESTÁVEL, cacheável)",
                "<strong>2. Few-shot</strong> — 2-N exemplos canônicos (ESTÁVEL, cacheável)",
                "<strong>3. Contexto recuperado</strong> — RAG, tools, dados externos (VARIÁVEL)",
                "<strong>4. Pergunta âncora</strong> (opcional) — repetição da pergunta no início do contexto",
                "<strong>5. User turn</strong> — pergunta de fato (FIM, atenção alta)"
            ]
        },
        "dados_pesquisa": {
            "titulo": "Wei et al. (2022) — Chain-of-Thought",
            "items": [
                "<strong>+17.9%</strong> em GSM8K (problemas matemáticos) com CoT vs. resposta direta.",
                "<strong>Padrão 'Vamos pensar passo a passo'</strong> dispara CoT em zero-shot (Kojima 2022).",
                "<strong>CoT é caro</strong> — gera mais output tokens, custo aumenta proporcionalmente."
            ]
        },
        "dica_pratica": {
            "emoji": "🎯", "titulo": "Use XML para separar dado de instrução",
            "texto": "Quando o prompt tem dados de usuário (texto livre, documento), envolva em tags como <code>&lt;documento_usuario&gt;...&lt;/documento_usuario&gt;</code>. Reduz risco de prompt injection (o modelo não confunde texto do doc com instrução)."
        },
        "fazer_evitar": [
            ("Definir persona e formato no system prompt", "Esperar que o modelo 'adivinhe' o comportamento"),
            ("Incluir 2-3 exemplos canônicos para tarefas estruturadas", "Descrever o formato em prosa sem mostrar exemplo"),
            ("Usar XML/JSON para separar seções claramente", "Concatenar tudo em um único bloco de texto"),
            ("Colocar a instrução no fim (zona de atenção alta)", "Enterrar a instrução no meio de contexto longo"),
        ],
        "quando_nao_usar": [
            "<strong>Tarefas simples e bem-tipadas</strong>: para 'traduza esta frase', system prompt + user turn já bastam.",
            "<strong>Quando você não tem exemplos canônicos</strong>: few-shot ruim atrapalha mais que ajuda — prefira zero-shot.",
            "<strong>Modelos pequenos OSS</strong>: alguns ignoram XML/JSON estrutural; teste primeiro.",
            "<strong>CoT em modelos de raciocínio (o-series)</strong>: já fazem internamente; pedir CoT explícito é redundante e caro.",
        ],
        "exemplo_codigo": (
            "from fec_sdk import Message, MessageRole\n"
            "from fec_sdk.adapters import get_adapter\n\n"
            "client = get_adapter(\"mock\", scripted=[(\"sentimento\", \"positivo\")])\n\n"
            "system = \"\"\"Você classifica sentimento em pt-BR.\n"
            "Saída: apenas 'positivo', 'negativo' ou 'neutro'.\n\n"
            "<exemplos>\n"
            "<exemplo><entrada>Adorei o produto, recomendo!</entrada><saida>positivo</saida></exemplo>\n"
            "<exemplo><entrada>Decepcionante, não recomendo.</entrada><saida>negativo</saida></exemplo>\n"
            "<exemplo><entrada>É um produto comum.</entrada><saida>neutro</saida></exemplo>\n"
            "</exemplos>\"\"\"\n\n"
            "resp = client.chat([\n"
            "    Message(role=MessageRole.SYSTEM, content=system),\n"
            "    Message(role=MessageRole.USER, content=\"<entrada>Excelente, superou expectativas!</entrada>\"),\n"
            "])\n"
            "print(resp.content)  # 'positivo'"
        ),
        "exercicio": "Reescreva um prompt 'string solta' em estrutura completa (system + few-shot + XML). O teste verifica que sua estrutura passa em 5/5 entradas com formato consistente. Em <code>exercicios/modulo-2-1/</code>.",
        "bibliografia": [
            ("Brown et al. (2020)", "Language Models are Few-Shot Learners (GPT-3)", "https://arxiv.org/abs/2005.14165"),
            ("Wei et al. (2022)", "Chain-of-Thought Prompting", "https://arxiv.org/abs/2201.11903"),
            ("Kojima et al. (2022)", "Large Language Models are Zero-Shot Reasoners", "https://arxiv.org/abs/2205.11916"),
            ("Anthropic (2024)", "Prompt engineering best practices", "https://docs.anthropic.com"),
        ],
        "resumo": [
            "<strong>5 seções</strong>: system + few-shot + contexto + âncora + user.",
            "<strong>System prompt</strong> define persona, regras, formato — estável e cacheável.",
            "<strong>Few-shot</strong> 2-3 exemplos canônicos batem zero-shot em tarefas estruturadas.",
            "<strong>XML/JSON</strong> separa dado de instrução, reduz confusão e injection.",
            "<strong>Pergunta no fim</strong> + ancoragem em contexto longo = atenção máxima.",
        ],
        "proximo_id": "modulo-2-2",
        "proximo_titulo": "Templates e versionamento de prompt",
    },

    {
        "id": "modulo-2-2", "trilha": 2, "numero": "2.2", "status": "GA",
        "titulo": "Templates, versionamento de prompt e eval primer",
        "emoji": "📝",
        "descricao": "Prompts viram código: têm versão, diff, teste. Toda mudança em prompt deve passar por mini-eval no harness antes de ir para produção.",
        "minutos": 60, "nivel": "Intermediário", "tipo": "Prático",
        "introducao": (
            "Prompts são código. Você não muda código de produção sem teste — não mude prompt sem eval. "
            "Aqui você aprende a tratar prompts como artefatos versionáveis: <strong class='text-blue-400'>template, hash, golden set, comparação A/B</strong>. "
            "É a sementeira da disciplina que se aprofunda em T6."
        ),
        "topicos": [
            {
                "emoji": "📦", "titulo": "Prompt como código: template + variáveis", "subtitulo": "Separar dado de prompt",
                "o_que_e": "Padrão template com placeholders (Jinja2, f-string, mustache). O prompt fica em arquivo versionado; dados entram no momento da chamada.",
                "por_que": "Prompts hardcoded em código Python ficam impossíveis de revisar e versionar. Templates externos permitem PR review do prompt isoladamente.",
                "conceitos": "Template engine, variáveis, schema de input, sanitização."
            },
            {
                "emoji": "🔢", "titulo": "Versionamento: SemVer aplicado a prompts", "subtitulo": "v1.0.0 do prompt",
                "o_que_e": "Major: mudança que invalida saídas anteriores (formato, persona). Minor: capability nova compatível. Patch: correção de typo, clareza.",
                "por_que": "Sem versionamento, regressão silenciosa é certeza. Você muda 'só uma palavra' e quebra 30% dos casos sem perceber.",
                "conceitos": "SemVer, prompt diff, breaking change, hash de prompt."
            },
            {
                "emoji": "🎯", "titulo": "Golden set: o conjunto de validação", "subtitulo": "20-50 exemplos canônicos",
                "o_que_e": "Conjunto fixado de input → output esperado, usado para medir se o prompt continua funcionando após mudança.",
                "por_que": "É o teste automatizado do prompt. Sem golden set, 'A/B' vira 'achei que melhorou'.",
                "conceitos": "Golden set, regression test, eval frozen, harness."
            },
            {
                "emoji": "⚖️", "titulo": "Eval primer: medir antes de mergear", "subtitulo": "A regra que enraíza em T6",
                "o_que_e": "Toda mudança em prompt entra com mini-eval contra o golden set. Métrica primária + 1-2 secundárias. Diff documentado.",
                "por_que": "Disciplina anti-regressão. Sem isso, o prompt vai sendo 'melhorado' ad hoc até parar de funcionar.",
                "conceitos": "Mini-eval, A/B no harness, statistical significance, eval cost."
            },
            {
                "emoji": "📊", "titulo": "Métricas: exact match, BLEU, LLM-as-judge", "subtitulo": "Escolha pela tarefa",
                "o_que_e": "Exact match para classificação. BLEU/ROUGE para tradução/sumarização. LLM-as-judge para qualidade subjetiva (com cuidado dos vieses).",
                "por_que": "Cada tipo de tarefa pede sua métrica. LLM-as-judge é poderoso mas tem vieses — detalhado em T6.1.",
                "conceitos": "Exact match, BLEU, ROUGE, LLM-as-judge, judge bias."
            },
            {
                "emoji": "🔁", "titulo": "Iterativa, não one-shot: o ciclo do prompt", "subtitulo": "Hipótese → eval → diff",
                "o_que_e": "Ciclo: hipótese de mudança → escrever variant → rodar contra golden → comparar métricas → decidir.",
                "por_que": "Prompt engineering não é arte intuitiva — é ciência empírica. Ciclos rápidos e medidos batem 'feeling'.",
                "conceitos": "Hypothesis-driven, eval cycle, prompt diff, A/B significant."
            },
        ],
        "conceito_principal": {
            "emoji": "🧬", "titulo": "Prompt-as-code: o ciclo de vida",
            "texto": "Trate o prompt exatamente como você trata código de produção: arquivo versionado, PR com diff, CI que roda eval, deploy só com aprovação.",
            "lista": [
                "<strong>Edita</strong>: novo arquivo <code>prompts/classify_v1.2.0.j2</code>.",
                "<strong>Testa</strong>: <code>pytest evals/classify/</code> roda contra golden set.",
                "<strong>Compara</strong>: diff métrica vs. versão anterior em PR.",
                "<strong>Deploy</strong>: merge só se métrica não regrediu (≥0 delta) E PR aprovado."
            ]
        },
        "dados_pesquisa": {
            "titulo": "Por que isso importa: regressão silenciosa é o normal",
            "items": [
                "<strong>30%+</strong> dos casos quebram em mudanças 'pequenas' não-validadas (estudo interno comum).",
                "<strong>Modelo do provedor é atualizado sem aviso</strong> — eval contínuo captura.",
                "<strong>Prompt drift</strong>: ao longo de meses, prompts viram colcha de retalhos sem ninguém perceber.",
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Comece pequeno",
            "texto": "Não precisa de Weights & Biases dia 1. <code>prompts/v1.0.0.txt</code> + 20 exemplos em <code>golden.jsonl</code> + <code>pytest test_prompt.py</code> já estabelece a disciplina."
        },
        "fazer_evitar": [
            ("Versionar prompts em arquivos separados", "Hardcoded como string em código Python"),
            ("Rodar mini-eval em toda mudança de prompt", "'Eu testei manualmente em 2 casos'"),
            ("Documentar o diff e métricas no PR", "Mergear com 'melhora performance' sem números"),
            ("Pinar versão do modelo no eval", "Eval que vira ruído porque o modelo muda"),
        ],
        "quando_nao_usar": [
            "<strong>Em prototipagem inicial (primeiras horas)</strong>: vá rápido, depois codifique a disciplina.",
            "<strong>Para prompts triviais usados 1 vez</strong>: 'resumir este texto' não precisa de SemVer.",
            "<strong>Quando golden set ainda não existe</strong>: defina-o antes de virar disciplina obrigatória.",
        ],
        "exemplo_codigo": (
            "# prompts/classify_v1.0.0.j2\n"
            "# (template Jinja2 — versionado em git)\n\n"
            "from jinja2 import Template\n"
            "from fec_sdk import Message, MessageRole\n"
            "from fec_sdk.adapters import get_adapter\n\n"
            "TEMPLATE = Template(open(\"prompts/classify_v1.0.0.j2\").read())\n\n"
            "def classificar(texto: str, modelo: str = \"mock\") -> str:\n"
            "    prompt = TEMPLATE.render(texto=texto)\n"
            "    client = get_adapter(modelo, model=\"mock-v1\")\n"
            "    resp = client.chat([\n"
            "        Message(role=MessageRole.SYSTEM, content=prompt),\n"
            "        Message(role=MessageRole.USER, content=texto),\n"
            "    ])\n"
            "    return resp.content.strip()\n\n"
            "# tests/test_classify.py\n"
            "def test_golden():\n"
            "    golden = json.load(open(\"evals/classify/golden_v1.jsonl\"))\n"
            "    correct = sum(1 for ex in golden if classificar(ex[\"in\"]) == ex[\"out\"])\n"
            "    assert correct / len(golden) >= 0.85  # baseline pinado"
        ),
        "exercicio": "Você recebe um prompt v1.0.0 + golden set de 20 exemplos. Modifique para v1.1.0 melhorando ≥1 caso sem regredir nenhum. Diff documentado. Em <code>exercicios/modulo-2-2/</code>.",
        "bibliografia": [
            ("Jinja2 docs", "Template engine de referência", "https://jinja.palletsprojects.com"),
            ("Anthropic (2024)", "Prompt evaluation best practices", "https://docs.anthropic.com"),
            ("Reimers & Gurevych (2019)", "Sentence-BERT (para similaridade)", "https://arxiv.org/abs/1908.10084"),
            ("Lin (2004)", "ROUGE: Recall-oriented eval", "https://aclanthology.org/W04-1013/"),
        ],
        "resumo": [
            "<strong>Prompts são código</strong> — versione em arquivo separado.",
            "<strong>SemVer</strong> aplicado: major/minor/patch para prompts.",
            "<strong>Golden set</strong> de 20-50 exemplos é o teste automatizado.",
            "<strong>Mini-eval</strong> em toda mudança — antes de mergear.",
            "<strong>Eval primer</strong> aqui é semente do que aprofunda em T6.1.",
        ],
        "proximo_id": "../trilha3/index.html",
        "proximo_titulo": "T3 — RAG e Recuperação",
    },

    # =================== T3 — RAG E RECUPERAÇÃO ===================
    {
        "id": "modulo-3-1", "trilha": 3, "numero": "3.1", "status": "GA",
        "titulo": "Indexação: chunking, embeddings e BM25 híbrido",
        "emoji": "📚",
        "descricao": "Como transformar um corpus em um índice consultável: estratégias de chunking, embeddings densos, BM25 sparse, e por que híbrido bate ambos.",
        "minutos": 60, "nivel": "Intermediário", "tipo": "Prático",
        "introducao": (
            "RAG bom é resultado de <strong class='text-purple-400'>indexação boa</strong>. "
            "Cada decisão — tamanho do chunk, modelo de embedding, índice sparse vs. denso — "
            "tem trade-offs concretos de recall, latência e custo. Aqui você aprende a navegar essas decisões."
        ),
        "topicos": [
            {
                "emoji": "✂️", "titulo": "Chunking: dividir o corpus", "subtitulo": "Tamanho, overlap, fronteiras semânticas",
                "o_que_e": "Quebrar documentos em pedaços (chunks) de 200-1000 tokens com overlap de 10-20%. Pode ser por caracteres, sentenças ou parágrafos.",
                "por_que": "Chunks muito grandes diluem relevância; muito pequenos perdem contexto. Overlap evita corte abrupto entre fronteiras.",
                "conceitos": "Sliding window, semantic chunking, fronteira de seção, recursive splitter."
            },
            {
                "emoji": "🧮", "titulo": "Embeddings densos: vetores semânticos", "subtitulo": "Modelos sentence-transformers",
                "o_que_e": "Converte texto em vetor (768-3072 dim) onde proximidade vetorial ≈ similaridade semântica. Modelos: bge, mpnet, OpenAI ada/text-3.",
                "por_que": "Captura sinônimos e paráfrase que BM25 perde ('automóvel' vs 'carro'). Base do retrieval moderno.",
                "conceitos": "Cosine similarity, dual encoder, MTEB benchmark, dimensionalidade."
            },
            {
                "emoji": "🔤", "titulo": "BM25: o sparse clássico que ainda manda", "subtitulo": "TF-IDF refinado",
                "o_que_e": "Algoritmo probabilístico de relevância baseado em frequência de termo (TF) e raridade (IDF). Não usa ML.",
                "por_que": "Robusto, rápido, captura match exato (números, IDs, nomes próprios) que embeddings densas erram.",
                "conceitos": "TF-IDF, BM25, sparse vector, lexical match, rare term boost."
            },
            {
                "emoji": "🤝", "titulo": "Híbrido: BM25 + denso, fusão por RRF", "subtitulo": "O melhor dos dois",
                "o_que_e": "Roda ambos em paralelo, funde rankings via Reciprocal Rank Fusion (RRF) ou peso linear (alpha).",
                "por_que": "Ganhos consistentes em benchmarks (BEIR). Cada método cobre falhas do outro: BM25 pega match exato, denso pega paráfrase.",
                "conceitos": "RRF, alpha-fusion, hybrid search, ColBERT (alternativa late-interaction)."
            },
            {
                "emoji": "🗂️", "titulo": "Vector stores: o que escolher", "subtitulo": "FAISS, pgvector, Qdrant, Pinecone",
                "o_que_e": "Bancos de dados otimizados para nearest-neighbor search em vetores. Local (FAISS, pgvector) ou hosted (Qdrant Cloud, Pinecone).",
                "por_que": "Sem isso, busca em 100k embeddings vira O(n) inviável. Vector stores fazem ANN (HNSW, IVF) em ms.",
                "conceitos": "ANN (approximate nearest neighbor), HNSW, IVF, recall@k, índice em memória vs. disco."
            },
            {
                "emoji": "🏷️", "titulo": "Metadata e filtros: além do match semântico", "subtitulo": "Filtragem antes/depois do retrieval",
                "o_que_e": "Anexar metadados a cada chunk (data, autor, categoria, idioma) e filtrar por eles antes ou depois da busca vetorial.",
                "por_que": "Pergunta 'eventos de 2024' não deve trazer chunks de 2019, mesmo que semanticamente similares. Filtros resolvem.",
                "conceitos": "Metadata filtering, pre-filter, post-filter, namespace."
            },
        ],
        "conceito_principal": {
            "emoji": "🏗️", "titulo": "Pipeline canônico de indexação",
            "texto": "Cada documento entra, é processado por uma pipeline determinística e sai como N chunks indexados. Reproducibilidade vem de fixar cada passo.",
            "lista": [
                "<strong>1. Parse</strong>: extrai texto (PDF→text, HTML→text), normaliza encoding.",
                "<strong>2. Chunk</strong>: divide com strategy + tamanho + overlap declarados.",
                "<strong>3. Embed</strong>: passa cada chunk pelo modelo de embedding.",
                "<strong>4. Index</strong>: armazena vetor + metadata em vector store + BM25.",
                "<strong>5. Hash</strong>: registra sha256 do corpus para reproducibilidade."
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Comece com 500 tokens + 50 overlap",
            "texto": "Para a maioria dos corpora técnicos em PT-BR, chunks de ~500 tokens com 10% overlap dão recall razoável. Ajuste depois com base em eval real, não em achismo."
        },
        "fazer_evitar": [
            ("Hash do corpus + versão da pipeline em metadata", "Re-indexar e perder reproducibilidade"),
            ("Híbrido (BM25 + denso) com RRF como default", "Confiar só em embeddings densas"),
            ("Filtros de metadata (data, idioma, fonte)", "Match puramente semântico em corpus heterogêneo"),
            ("Chunks com fronteira semântica (parágrafo)", "Cortar no meio de sentença ou fórmula"),
        ],
        "quando_nao_usar": [
            "<strong>Quando contexto longo basta</strong>: corpus pequeno (&lt;50k tokens) cabe direto na janela.",
            "<strong>Quando a query exige raciocínio multi-hop</strong>: agente (T4) funciona melhor que RAG estático.",
            "<strong>Quando o corpus muda a cada chamada</strong>: indexar não vale a pena; passe contexto direto.",
        ],
        "exemplo_codigo": (
            "from fec_sdk import check_compat\n"
            "check_compat(\"modulo-3-1\")\n\n"
            "# Pseudo-código provider-neutral\n"
            "from fec_sdk.indexing import Pipeline, Chunker, EmbedderHTTP, BM25\n\n"
            "pipeline = Pipeline([\n"
            "    Chunker(size=500, overlap=50, strategy=\"paragraph\"),\n"
            "    EmbedderHTTP(model=\"bge-large-en-v1.5\"),\n"
            "])\n\n"
            "# Indexa todos os docs\n"
            "for doc in corpus:\n"
            "    chunks = pipeline.run(doc)\n"
            "    vector_store.add(chunks, metadata={\"doc_id\": doc.id, \"date\": doc.date})\n\n"
            "# BM25 em paralelo\n"
            "bm25 = BM25(chunks)\n"
            "# Híbrido: query → top-50 BM25 ∪ top-50 denso → RRF → top-10"
        ),
        "exercicio": "Indexe um corpus de 100 abstracts ArXiv (em <code>fixtures/arxiv-cs-100/</code>) com pipeline determinística. Eval de recall@10 deve atingir ≥0.7 no golden FEC-GS-RAG-v1. Em <code>exercicios/modulo-3-1/</code>.",
        "bibliografia": [
            ("Robertson & Zaragoza (2009)", "BM25 and Beyond", "https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf"),
            ("Reimers & Gurevych (2019)", "Sentence-BERT", "https://arxiv.org/abs/1908.10084"),
            ("Cormack et al. (2009)", "Reciprocal Rank Fusion (RRF)", "https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf"),
            ("Thakur et al. (2021)", "BEIR benchmark", "https://arxiv.org/abs/2104.08663"),
        ],
        "resumo": [
            "<strong>Chunking</strong>: 500 tokens + overlap, fronteira semântica.",
            "<strong>Embeddings densas</strong> capturam paráfrase; <strong>BM25</strong> pega match exato.",
            "<strong>Híbrido com RRF</strong> bate ambos consistentemente.",
            "<strong>Vector stores</strong> usam ANN (HNSW, IVF) para escalar.",
            "<strong>Metadata + filtros</strong> são tão importantes quanto similaridade.",
        ],
        "proximo_id": "modulo-3-2",
        "proximo_titulo": "Recuperação e reranking",
    },

    {
        "id": "modulo-3-2", "trilha": 3, "numero": "3.2", "status": "GA",
        "titulo": "Recuperação, reranking e contextual retrieval",
        "emoji": "🔍",
        "descricao": "Do índice à resposta: top-k retrieval, rerankers cross-encoder, contextual retrieval (Anthropic 2024) e citações obrigatórias.",
        "minutos": 60, "nivel": "Intermediário", "tipo": "Prático",
        "introducao": (
            "Retrieval ingênuo recupera 50 docs e despeja na janela. RAG bom <strong class='text-purple-400'>recupera 100, rerankeia para 5, e mostra citação</strong>. "
            "Aqui você aprende a fechar o ciclo: top-k, reranker, contextual retrieval, e como forçar o modelo a citar a fonte."
        ),
        "topicos": [
            {
                "emoji": "🎯", "titulo": "Top-k retrieval: quanto recuperar", "subtitulo": "Trade-off recall vs. ruído",
                "o_que_e": "Pegar os k chunks mais similares à query. k=3-10 é o range típico para passar à geração.",
                "por_que": "k baixo perde recall; k alto enche a janela de ruído (vide lost-in-the-middle). Otimize empiricamente.",
                "conceitos": "Recall@k, precision@k, k-tuning, MRR (mean reciprocal rank)."
            },
            {
                "emoji": "🏆", "titulo": "Reranker cross-encoder: precisão alta", "subtitulo": "BGE-reranker, Cohere Rerank",
                "o_que_e": "Modelo cross-encoder que recebe (query, chunk) e retorna score. Mais preciso que dual encoder, mas mais lento.",
                "por_que": "Padrão: recupera top-50 com encoder rápido, rankeia para top-5 com cross-encoder. Ganho consistente em recall.",
                "conceitos": "Cross-encoder vs dual encoder, BGE reranker, Cohere Rerank, latency budget."
            },
            {
                "emoji": "🪄", "titulo": "Contextual retrieval (Anthropic 2024)", "subtitulo": "Embed com contexto do documento",
                "o_que_e": "Antes de embedar cada chunk, injeta uma descrição curta do documento de onde veio. Reduz miss em 35-50% (Anthropic 2024).",
                "por_que": "Chunk isolado perde contexto; com contexto, embedding fica mais informativo. Custo: chamada extra ao LLM por chunk no index time.",
                "conceitos": "Contextual retrieval, document-level prefix, prompt caching no index, late chunking."
            },
            {
                "emoji": "📌", "titulo": "Citações obrigatórias na geração", "subtitulo": "Rastreabilidade da resposta",
                "o_que_e": "Padrão de incluir IDs/URLs dos chunks recuperados no prompt e exigir que a resposta cite a fonte de cada afirmação.",
                "por_que": "Sem citação, você não sabe se o modelo grounded a resposta ou alucinou. Eval (T6) precisa de citação para medir groundedness.",
                "conceitos": "Citation patterns, source tracking, groundedness, attribution."
            },
            {
                "emoji": "🚫", "titulo": "Saber dizer 'não sei'", "subtitulo": "Quando não há contexto suficiente",
                "o_que_e": "System prompt instrui: 'se a resposta não está no contexto, diga não sei'. Reduz alucinação.",
                "por_que": "Modelos preferem responder algo a admitir ignorância. Instrução explícita + few-shot de 'não sei' equilibra.",
                "conceitos": "Abstention, calibration, hallucination, RAG-fail-safe."
            },
            {
                "emoji": "♻️", "titulo": "Re-rankeio adaptativo: query rewriting", "subtitulo": "Query expansion e HyDE",
                "o_que_e": "Antes de buscar, o LLM reescreve/expande a query (sinônimos, sub-perguntas) ou gera resposta hipotética (HyDE) usada como query.",
                "por_que": "Query do usuário é frequentemente curta e ambígua. Reescrita melhora recall sem custar muito.",
                "conceitos": "Query rewriting, HyDE (Gao et al. 2022), multi-query retrieval, query decomposition."
            },
        ],
        "conceito_principal": {
            "emoji": "🎯", "titulo": "Pipeline de retrieval em 5 passos",
            "texto": "Cada passo tem decisão clara e métrica de saúde. Sem instrumentação, você não sabe onde o pipeline degrada.",
            "lista": [
                "<strong>1. Query rewrite</strong> (opcional): expansão / HyDE.",
                "<strong>2. Hybrid retrieval</strong>: BM25 + denso → top-50 via RRF.",
                "<strong>3. Rerank</strong>: cross-encoder → top-5.",
                "<strong>4. Format</strong>: monta prompt com IDs visíveis.",
                "<strong>5. Generate + cite</strong>: modelo responde com citação obrigatória."
            ]
        },
        "dados_pesquisa": {
            "titulo": "Anthropic Contextual Retrieval (2024)",
            "items": [
                "<strong>-49%</strong> em failure rate (recall@20) com contextual retrieval + reranker.",
                "<strong>-35%</strong> só com contextual retrieval (sem reranker).",
                "<strong>Custo:</strong> uma chamada extra ao LLM por chunk no index time (mitigado por prompt caching).",
            ]
        },
        "fazer_evitar": [
            ("Reranker cross-encoder após top-50 inicial", "Passar top-50 direto à geração"),
            ("Citação obrigatória + ID visível no prompt", "Esperar que o modelo 'use' o contexto sem citar"),
            ("Instrução 'diga não sei' + few-shot de abstenção", "Sempre forçar uma resposta"),
            ("Eval de groundedness no harness", "Confiar que 'a resposta parece boa'"),
        ],
        "quando_nao_usar": [
            "<strong>Query muito específica e bem-formada</strong>: query rewrite pode atrapalhar.",
            "<strong>Latência crítica</strong>: cross-encoder rerank adiciona 100-500ms.",
            "<strong>Top-k já é alto e modelo aguenta</strong>: rerank dispensável se atenção der conta.",
        ],
        "exemplo_codigo": (
            "from fec_sdk import Message, MessageRole\n"
            "from fec_sdk.adapters import get_adapter\n"
            "from fec_sdk.retrieval import HybridRetriever, CrossEncoderReranker  # pseudo\n\n"
            "retriever = HybridRetriever(vector_store, bm25)\n"
            "reranker = CrossEncoderReranker(model=\"bge-reranker-large\")\n\n"
            "def responder(query: str) -> dict:\n"
            "    candidatos = retriever.search(query, k=50)        # top-50\n"
            "    top5 = reranker.rerank(query, candidatos, k=5)    # top-5\n\n"
            "    contexto = \"\\n\\n\".join(\n"
            "        f\"<chunk id={c.id}>{c.text}</chunk>\" for c in top5\n"
            "    )\n"
            "    system = (\n"
            "        \"Responda APENAS com base no contexto. \"\n"
            "        \"Cite o id de cada chunk usado, ex.: [chunk:42]. \"\n"
            "        \"Se a resposta não está no contexto, diga 'não sei'.\"\n"
            "    )\n"
            "    client = get_adapter(\"mock\")\n"
            "    resp = client.chat([\n"
            "        Message(role=MessageRole.SYSTEM, content=system),\n"
            "        Message(role=MessageRole.USER, content=f\"{contexto}\\n\\n{query}\"),\n"
            "    ])\n"
            "    return {\"answer\": resp.content, \"citations\": [c.id for c in top5]}"
        ),
        "exercicio": "Use o índice de 3.1 + reranker para responder 30 perguntas do golden FEC-GS-RAG-v1 com groundedness ≥0.85. Implementação em <code>exercicios/modulo-3-2/</code>.",
        "bibliografia": [
            ("Anthropic (2024)", "Introducing Contextual Retrieval", "https://www.anthropic.com/news/contextual-retrieval"),
            ("Gao et al. (2022)", "Precise Zero-Shot Dense Retrieval (HyDE)", "https://arxiv.org/abs/2212.10496"),
            ("Khattab & Zaharia (2020)", "ColBERT", "https://arxiv.org/abs/2004.12832"),
            ("Liu et al. (2023)", "Lost in the Middle", "https://arxiv.org/abs/2307.03172"),
        ],
        "resumo": [
            "<strong>Top-k</strong>: 3-10 é o range; meça empiricamente.",
            "<strong>Reranker cross-encoder</strong> após top-50 dá ganho consistente.",
            "<strong>Contextual retrieval</strong> (Anthropic 2024): -35-49% em failure rate.",
            "<strong>Citação obrigatória</strong> é pré-requisito de eval de groundedness.",
            "<strong>Saber dizer 'não sei'</strong> é parte do design, não exceção.",
        ],
        "proximo_id": "modulo-3-3",
        "proximo_titulo": "RAG agêntico e self-RAG (beta)",
    },

    {
        "id": "modulo-3-3", "trilha": 3, "numero": "3.3", "status": "beta",
        "titulo": "RAG agêntico e self-RAG (beta)",
        "emoji": "🤖",
        "descricao": "Quando o RAG estático não basta: agente que decide se busca, o que busca, e quando parar. Self-RAG, multi-hop, e quando o custo NÃO compensa.",
        "minutos": 70, "nivel": "Avançado", "tipo": "Avançado",
        "introducao": (
            "RAG estático recupera de uma vez. <strong class='text-purple-400'>RAG agêntico decide</strong>: busca? o quê? quantas vezes? "
            "Você ganha em qualidade (multi-hop, query refinement) e perde em custo/latência. "
            "Este módulo é <em>beta</em> — padrões ainda evoluem rapidamente."
        ),
        "topicos": [
            {
                "emoji": "🔄", "titulo": "Multi-hop: encadear buscas", "subtitulo": "Quando uma busca não basta",
                "o_que_e": "Pergunta exige info de múltiplas fontes em sequência. Agente busca, lê, refina query, busca de novo.",
                "por_que": "Perguntas como 'compare A e B em 2024' precisam de 2+ buscas. RAG estático falha.",
                "conceitos": "Multi-hop QA, iterative retrieval, query refinement, ReAct."
            },
            {
                "emoji": "🤔", "titulo": "Self-RAG: decidir se buscar", "subtitulo": "Asai et al. 2023",
                "o_que_e": "Modelo emite token especial decidindo se precisa buscar. Se não, responde do parâmetro; se sim, busca e cita.",
                "por_que": "Nem toda pergunta precisa de RAG. Self-RAG evita custo e latência quando o conhecimento paramétrico basta.",
                "conceitos": "Self-RAG, retrieve-or-not, calibração de confiança, paramétrico vs. retrieval."
            },
            {
                "emoji": "🧭", "titulo": "Query decomposition", "subtitulo": "Quebrar pergunta complexa",
                "o_que_e": "LLM decompõe pergunta em sub-perguntas, busca cada uma, junta as evidências.",
                "por_que": "Para perguntas compostas ('o que mudou de A para B?'), decomposição melhora recall.",
                "conceitos": "Query decomposition, sub-question answering, fan-out, planner."
            },
            {
                "emoji": "🛡️", "titulo": "Guards: critic step e verificação", "subtitulo": "Checar antes de entregar",
                "o_que_e": "Após resposta, segundo passo verifica: a resposta está grounded? Cita fonte? Se não, refaz.",
                "por_que": "Qualidade > velocidade em casos sensíveis. Critic step pega regressões.",
                "conceitos": "Critic loop, verification step, self-correction, faithfulness."
            },
            {
                "emoji": "🚦", "titulo": "Stopping criteria", "subtitulo": "Quando o agente para de buscar",
                "o_que_e": "Critério explícito: max iterações, confiança suficiente, ou custo orçado atingido.",
                "por_que": "Sem critério, o agente loopa. Loops em produção são desastre de custo.",
                "conceitos": "Max iterations, confidence threshold, cost budget, early stop."
            },
            {
                "emoji": "💸", "titulo": "Quando NÃO usar RAG agêntico", "subtitulo": "O custo é real",
                "o_que_e": "Cada hop custa: tokens + latência + risco de loop. Para 80% dos casos, RAG estático com bom reranker basta.",
                "por_que": "RAG agêntico pode 3-10× o custo de RAG estático sem ganho proporcional.",
                "conceitos": "Cost amortization, complexity vs benefit, default to simple."
            },
        ],
        "conceito_principal": {
            "emoji": "⚖️", "titulo": "Trade-off explícito: custo vs qualidade",
            "texto": "RAG agêntico é uma promoção condicional do RAG estático — só compensa quando a pergunta REALMENTE exige.",
            "lista": [
                "Pergunta single-hop, fonte clara → <strong>RAG estático.</strong>",
                "Pergunta multi-hop, fontes múltiplas → <strong>RAG agêntico (com cap).</strong>",
                "Verificação crítica → <strong>+ critic loop.</strong>",
                "Sempre: max_iterations + budget cap."
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Comece estático, escale para agêntico",
            "texto": "Antes de adotar RAG agêntico, esgote RAG estático com reranker e contextual retrieval. Ganho de 3.2 frequentemente fecha a lacuna sem custo agêntico."
        },
        "fazer_evitar": [
            ("max_iterations explícito (ex.: 3)", "Loop indefinido"),
            ("Budget de tokens por chamada agêntica", "Custos fora de controle"),
            ("Logs de cada hop com query e resultado", "Debug impossível em produção"),
            ("RAG agêntico só onde estático falha", "Adotar por padrão"),
        ],
        "quando_nao_usar": [
            "<strong>Latência baixa exigida</strong>: cada hop é uma roundtrip.",
            "<strong>Volume alto</strong>: custo escala linearmente.",
            "<strong>Quando RAG estático já passa em eval</strong>: complexidade extra é dívida técnica.",
        ],
        "exemplo_codigo": (
            "# Pseudo-código de loop agêntico simplificado\n"
            "def agentic_rag(query: str, max_hops: int = 3) -> dict:\n"
            "    historico = []\n"
            "    for hop in range(max_hops):\n"
            "        decisao = llm_decide(query, historico)  # buscar? parar? refinar?\n"
            "        if decisao == \"parar\":\n"
            "            return llm_responder_final(query, historico)\n"
            "        elif decisao == \"buscar\":\n"
            "            sub_query = llm_refinar_query(query, historico)\n"
            "            chunks = retriever.search(sub_query, k=5)\n"
            "            historico.append({\"hop\": hop, \"query\": sub_query, \"chunks\": chunks})\n"
            "    return llm_responder_final(query, historico)  # fallback"
        ),
        "exercicio": "Implemente RAG agêntico com max 3 hops contra um conjunto multi-hop de 10 perguntas. Compare com RAG estático: medir custo e acurácia.",
        "bibliografia": [
            ("Asai et al. (2023)", "Self-RAG: Learning to Retrieve, Generate, and Critique", "https://arxiv.org/abs/2310.11511"),
            ("Yao et al. (2022)", "ReAct: Synergizing Reasoning and Acting", "https://arxiv.org/abs/2210.03629"),
            ("Trivedi et al. (2022)", "Multi-Hop QA via Iterative Retrieval", "https://arxiv.org/abs/2212.10509"),
            ("Anthropic (2024)", "Contextual Retrieval", "https://www.anthropic.com/news/contextual-retrieval"),
        ],
        "resumo": [
            "<strong>Multi-hop</strong> resolve perguntas que single-hop falha.",
            "<strong>Self-RAG</strong>: decidir se buscar reduz custo em casos triviais.",
            "<strong>Decomposition</strong>: quebrar pergunta complexa em sub-perguntas.",
            "<strong>Stopping criteria</strong> obrigatório (max_iterations, budget).",
            "<strong>Default ao simples</strong>: estático com reranker resolve 80% dos casos.",
        ],
        "proximo_id": "../trilha4/index.html",
        "proximo_titulo": "T4 — Tools, Agentes e Multi-Agente",
    },

    # =================== T4 — TOOLS, AGENTES E MULTI-AGENTE ===================
    {
        "id": "modulo-4-1", "trilha": 4, "numero": "4.1", "status": "GA",
        "titulo": "Tool/function calling provider-neutral",
        "emoji": "🛠️",
        "descricao": "Como o modelo invoca funções estruturadas. JSON Schema como contrato, tratamento de erro, sandbox obrigatório.",
        "minutos": 65, "nivel": "Intermediário", "tipo": "Hands-on",
        "introducao": (
            "Tool calling transforma o LLM em <strong class='text-amber-400'>orquestrador de funções</strong>. "
            "O modelo decide qual chamar, com quais argumentos, e usa o resultado para continuar. "
            "Aqui você aprende a desenhar tools robustos — JSON Schema bem definido, erro tipado, sandbox obrigatório."
        ),
        "topicos": [
            {
                "emoji": "📋", "titulo": "JSON Schema: o contrato do tool", "subtitulo": "Tipo, descrição, validação",
                "o_que_e": "Cada tool tem schema declarativo: nome, descrição, parâmetros tipados (string, number, enum, etc.) com required.",
                "por_que": "Schema bom = chamada confiável. Modelo usa descrição para escolher e schema para formatar argumentos.",
                "conceitos": "JSON Schema 2020-12, parameter validation, required fields, oneOf."
            },
            {
                "emoji": "✏️", "titulo": "Descrição do tool: o prompt do prompt", "subtitulo": "Onde a magia acontece",
                "o_que_e": "Texto livre que descreve quando usar o tool. É lido pelo LLM ao decidir ferramenta.",
                "por_que": "Modelos escolhem tool com base na descrição. 'busca_web' vs 'busca_web_para_eventos_recentes_e_notícias' muda comportamento.",
                "conceitos": "Tool description, disambiguation, when-to-use clauses."
            },
            {
                "emoji": "🚦", "titulo": "Erro tipado: sucesso, retry, abort", "subtitulo": "Como o tool comunica falha",
                "o_que_e": "Resultado do tool inclui campo de status. Modelo lê e decide retry, fallback ou parar.",
                "por_que": "Sem tipo de erro, modelo tenta de novo cegamente ou desiste. Estrutura permite recovery inteligente.",
                "conceitos": "Result types, ToolError, retry-able vs fatal, exponential backoff."
            },
            {
                "emoji": "🔒", "titulo": "Sandbox obrigatório (PLAN item 62a)", "subtitulo": "Filesystem, processo, rede",
                "o_que_e": "Toda tool que toca FS/rede/processo roda dentro de FilesystemSandbox + NetworkPolicy do fec_sdk.",
                "por_que": "Prompt injection consegue fazer tool ler ~/.aws/credentials se não houver sandbox. PLAN item 62a é gate de GA.",
                "conceitos": "Path traversal, deny-by-default, allowlist, jail."
            },
            {
                "emoji": "🔄", "titulo": "Loop: tool → resultado → próximo passo", "subtitulo": "ReAct simplificado",
                "o_que_e": "Modelo decide chamar tool → executa → resultado vira mensagem do role 'tool' → modelo continua.",
                "por_que": "Esse é o building block de agentes. Um loop simples já resolve muitas tarefas.",
                "conceitos": "Tool result message, role=tool, tool_use_id, conversation continuation."
            },
            {
                "emoji": "🎚️", "titulo": "Tool choice: forçar ou deixar o modelo decidir", "subtitulo": "auto, any, specific",
                "o_que_e": "Parâmetro que controla quando o modelo pode chamar tool: auto (decide), any (deve chamar algum), specific (deve chamar X).",
                "por_que": "Em alguns fluxos você QUER forçar uso de tool (ex.: extract). Em outros, deixar livre é melhor.",
                "conceitos": "tool_choice, parallel tool calls, required tool."
            },
        ],
        "conceito_principal": {
            "emoji": "🛠️", "titulo": "Tool é interface: schema + executor",
            "texto": "Cada tool tem dois lados: o schema que o LLM lê, e o executor que roda quando chamado. Ambos vivem juntos.",
            "lista": [
                "<strong>Schema</strong>: nome, descrição, JSON Schema dos params.",
                "<strong>Executor</strong>: função Python que recebe args validados, retorna resultado.",
                "<strong>Sandbox</strong>: executor roda jailed se tocar FS/rede.",
                "<strong>Erro</strong>: tipo claro (retry-able, fatal, partial).",
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Description é prompt — itere",
            "texto": "Comece com descrição básica. Em casos onde o modelo escolhe errado, refine a descrição (não a lógica do tool). Eval no harness mostra impacto."
        },
        "fazer_evitar": [
            ("Sandbox obrigatório para tools com side-effect", "<code>os.system(arg)</code> direto"),
            ("Erro tipado com retry-able vs fatal", "Levantar exceção genérica"),
            ("Description com 'when to use' explícito", "Description vaga: 'busca informação'"),
            ("Validar JSON Schema dos args antes de executar", "Confiar que o modelo preencheu certo"),
        ],
        "quando_nao_usar": [
            "<strong>Tarefa pode ser feita só com prompt</strong>: tool adiciona complexidade desnecessária.",
            "<strong>Modelo OSS pequeno sem suporte estável a tool</strong>: força adapter ou mock.",
            "<strong>Latência crítica</strong>: tool call adiciona 1+ roundtrip.",
        ],
        "exemplo_codigo": (
            "from fec_sdk import Message, MessageRole, Tool, ToolResult\n"
            "from fec_sdk.adapters import get_adapter\n"
            "from fec_sdk.sandbox import FilesystemSandbox\n\n"
            "tool_ler_arquivo = Tool(\n"
            "    name=\"ler_arquivo\",\n"
            "    description=\"Lê arquivo .txt ou .md em path RELATIVO ao sandbox.\",\n"
            "    parameters={\n"
            "        \"type\": \"object\",\n"
            "        \"properties\": {\"path\": {\"type\": \"string\"}},\n"
            "        \"required\": [\"path\"],\n"
            "    }\n"
            ")\n\n"
            "with FilesystemSandbox() as fs:\n"
            "    fs.write_text(\"nota.md\", \"FEC v1.0\")\n\n"
            "    client = get_adapter(\"mock\")\n"
            "    resp = client.chat(\n"
            "        [Message(role=MessageRole.USER, content=\"Leia nota.md\")],\n"
            "        tools=[tool_ler_arquivo],\n"
            "    )\n\n"
            "    if resp.tool_calls:\n"
            "        for call in resp.tool_calls:\n"
            "            try:\n"
            "                conteudo = fs.read_text(call.arguments[\"path\"])\n"
            "                resultado = ToolResult(tool_call_id=call.id, content=conteudo)\n"
            "            except Exception as e:\n"
            "                resultado = ToolResult(tool_call_id=call.id, content=str(e), is_error=True)"
        ),
        "exercicio": "Defina 3 tools (ler arquivo, calcular, buscar termo) com sandbox e schema. Bateria <code>tests/sandbox/</code> deve passar em todos. Em <code>exercicios/modulo-4-1/</code>.",
        "bibliografia": [
            ("OpenAI (2023)", "Function calling guide", "https://platform.openai.com/docs/guides/function-calling"),
            ("Anthropic (2024)", "Tool use with Claude", "https://docs.anthropic.com/en/docs/tool-use"),
            ("JSON Schema", "JSON Schema 2020-12 spec", "https://json-schema.org/draft/2020-12/release-notes.html"),
            ("Schick et al. (2023)", "Toolformer: Language Models Can Teach Themselves to Use Tools", "https://arxiv.org/abs/2302.04761"),
        ],
        "resumo": [
            "<strong>Tool = schema + executor</strong>; ambos vivem juntos.",
            "<strong>JSON Schema</strong> como contrato; validar args antes de executar.",
            "<strong>Description</strong> é o prompt do prompt — itere com eval.",
            "<strong>Sandbox</strong> obrigatório (PLAN item 62a) para FS/rede/processo.",
            "<strong>Erro tipado</strong>: retry-able vs fatal; modelo recupera melhor.",
        ],
        "proximo_id": "modulo-4-2",
        "proximo_titulo": "Agentes single (ReAct, planner/executor)",
    },

    {
        "id": "modulo-4-2", "trilha": 4, "numero": "4.2", "status": "GA",
        "titulo": "Agentes single: ReAct e planner/executor",
        "emoji": "🤖",
        "descricao": "Agente é loop tool→pensa→tool. ReAct, planner/executor, controle de loop, e como debugar via tracing.",
        "minutos": 70, "nivel": "Avançado", "tipo": "Hands-on",
        "introducao": (
            "Agente é o próximo passo após tool calling: <strong class='text-amber-400'>loop autônomo</strong> de pensar→agir até concluir. "
            "ReAct é o padrão dominante; planner/executor é alternativa para tarefas estruturadas. "
            "Aqui você aprende a controlar o loop — sem isso, agente vira disaster de custo."
        ),
        "topicos": [
            {
                "emoji": "🧭", "titulo": "ReAct: Reason + Act", "subtitulo": "Yao et al. 2022",
                "o_que_e": "Loop: modelo pensa em texto livre ('Pensamento: preciso buscar X') → decide tool ('Ação: search(X)') → recebe resultado ('Observação: ...') → repete.",
                "por_que": "Padrão simples e eficaz. Pensamento explícito facilita debug e melhora qualidade em tarefas multi-passo.",
                "conceitos": "ReAct (Yao 2022), Thought-Action-Observation, scratchpad, reasoning trace."
            },
            {
                "emoji": "📐", "titulo": "Planner / Executor: separar plano de execução", "subtitulo": "Decomposição prévia",
                "o_que_e": "Primeiro passo: LLM gera plano em N passos. Segundo passo: executor segue passo por passo.",
                "por_que": "Para tarefas estruturadas conhecidas (workflows), plano explícito é mais auditável que ReAct.",
                "conceitos": "Plan-and-execute, BabyAGI, hierarchical planning."
            },
            {
                "emoji": "⛔", "titulo": "Controle de loop: max_iterations, max_tokens", "subtitulo": "Limites duros",
                "o_que_e": "Agente tem budget explícito: máximo de iterações, máximo de tokens, timeout total.",
                "por_que": "Sem isso, agente loopa em produção e queima orçamento. Limite duro é seguro.",
                "conceitos": "Max iterations, token budget, wall-clock timeout, infinite loop detection."
            },
            {
                "emoji": "🔍", "titulo": "Tracing por step: a chave para debug", "subtitulo": "Cada decisão fica registrada",
                "o_que_e": "Cada step do agente vira entry estruturada (timestamp, tool, args, result, next). Salvo em traces/.",
                "por_que": "Sem tracing, debugar agente em produção é impossível. P2 do curso exige.",
                "conceitos": "Step trace, OpenTelemetry, structured logging, step replay."
            },
            {
                "emoji": "🛡️", "titulo": "Recovery: tool error, JSON inválido, loop", "subtitulo": "Padrões de robustez",
                "o_que_e": "Estratégias para quando algo dá errado: retry com fix, abort com mensagem, fallback para LLM puro.",
                "por_que": "Em produção, ferramentas falham, JSON vem malformado, modelos respondem fora do schema. Sem recovery, agente quebra.",
                "conceitos": "Retry policies, JSON repair, graceful degradation, partial success."
            },
            {
                "emoji": "💸", "titulo": "Orçamento de custo por agente", "subtitulo": "Budget cap antes de loop",
                "o_que_e": "Antes de iniciar o agente, declarar 'esta tarefa custa no máximo X tokens / Y dólares'. Aborta se atingir.",
                "por_que": "Cap nativo de provedor é última linha; cap explícito no agente é controle real.",
                "conceitos": "Per-task budget, cost estimation, soft limit, hard limit."
            },
        ],
        "conceito_principal": {
            "emoji": "🔁", "titulo": "Anatomia de um agente robusto",
            "texto": "Não é só 'modelo + tools'. É um sistema com instrumentação, limites e recovery — como qualquer sistema de produção.",
            "lista": [
                "<strong>Loop core</strong>: ReAct ou planner/executor.",
                "<strong>Limites</strong>: max_iterations, max_tokens, timeout.",
                "<strong>Tracing</strong>: cada step estruturado.",
                "<strong>Recovery</strong>: retry, abort, fallback.",
                "<strong>Sandbox</strong>: tools sempre jailed.",
            ]
        },
        "dados_pesquisa": {
            "titulo": "Yao et al. (2022) — ReAct",
            "items": [
                "<strong>+34%</strong> em HotpotQA com ReAct vs CoT puro.",
                "<strong>Reasoning trace explícito</strong> é o que dá ganho — facilita debug humano também.",
                "<strong>Loops longos degradam</strong>: tarefas além de 8-10 steps quase sempre regridem.",
            ]
        },
        "fazer_evitar": [
            ("max_iterations sempre declarado (ex.: 10)", "Loop sem limite — disaster em produção"),
            ("Tracing estruturado por step", "Print debug ad hoc"),
            ("Tools com erro tipado para recovery inteligente", "Exceção genérica que para o agente"),
            ("Budget de custo explícito por tarefa", "Confiar só no cap do provedor"),
        ],
        "quando_nao_usar": [
            "<strong>Tarefa one-shot estruturada</strong>: prompt + tool calling resolve sem loop.",
            "<strong>Latência crítica (UX live)</strong>: agente faz N roundtrips, latência multiplica.",
            "<strong>Sem tracing</strong>: agente sem instrumentação é dívida técnica imediata.",
        ],
        "exemplo_codigo": (
            "from fec_sdk import Message, MessageRole\n"
            "from fec_sdk.adapters import get_adapter\n\n"
            "def react_agent(query: str, tools, max_iter: int = 10) -> str:\n"
            "    msgs = [Message(role=MessageRole.USER, content=query)]\n"
            "    client = get_adapter(\"mock\")\n"
            "    trace = []\n\n"
            "    for step in range(max_iter):\n"
            "        resp = client.chat(msgs, tools=tools)\n"
            "        trace.append({\"step\": step, \"content\": resp.content,\n"
            "                      \"tool_calls\": [tc.model_dump() for tc in resp.tool_calls]})\n\n"
            "        if not resp.tool_calls:\n"
            "            return resp.content  # agente decidiu parar\n\n"
            "        # Executa cada tool e adiciona resultado\n"
            "        for call in resp.tool_calls:\n"
            "            result = executar_tool(call)  # com sandbox, retry, etc.\n"
            "            msgs.append(Message(role=MessageRole.TOOL, content=str(result), name=call.name))\n\n"
            "    return \"max_iterations excedido\"  # fallback explícito"
        ),
        "exercicio": "Implemente ReAct agent com 3 tools + max_iterations + tracing estruturado. Bateria de 30 traços-canário (golden FEC-GS-AGENT-v1) deve passar 30/30 sem loop infinito. Em <code>exercicios/modulo-4-2/</code>.",
        "bibliografia": [
            ("Yao et al. (2022)", "ReAct: Synergizing Reasoning and Acting", "https://arxiv.org/abs/2210.03629"),
            ("Wang et al. (2023)", "Plan-and-Solve Prompting", "https://arxiv.org/abs/2305.04091"),
            ("Anthropic (2024)", "Building Effective Agents", "https://www.anthropic.com/research/building-effective-agents"),
            ("OpenAI (2024)", "Practices for Governing Agentic AI Systems", "https://openai.com/index/practices-for-governing-agentic-ai-systems"),
        ],
        "resumo": [
            "<strong>Agente é loop</strong>: ReAct (pensa-age) ou planner/executor.",
            "<strong>max_iterations</strong> obrigatório — sem isso, loop em produção.",
            "<strong>Tracing por step</strong> é pré-requisito de debugability.",
            "<strong>Recovery</strong>: retry, abort, fallback — não exceção crua.",
            "<strong>Budget</strong> de custo explícito por tarefa.",
        ],
        "proximo_id": "modulo-4-3",
        "proximo_titulo": "Multi-agente e MCP (beta)",
    },

    {
        "id": "modulo-4-3", "trilha": 4, "numero": "4.3", "status": "beta",
        "titulo": "Multi-agente e MCP (beta)",
        "emoji": "👥",
        "descricao": "Padrões multi-agente: orquestrador-trabalhador, debate, blackboard. MCP (Model Context Protocol). Quando NÃO multiplicar.",
        "minutos": 70, "nivel": "Avançado", "tipo": "Avançado",
        "introducao": (
            "Multi-agente é tentador mas frequentemente <strong class='text-amber-400'>injustificado</strong>. "
            "Aqui você aprende padrões reais (orquestrador-trabalhador, debate, blackboard), o que MCP traz, "
            "e — crucialmente — quando UM agente bem-feito bate três meia-bocas."
        ),
        "topicos": [
            {
                "emoji": "🎼", "titulo": "Orquestrador + trabalhadores especializados", "subtitulo": "O padrão mais comum",
                "o_que_e": "Um agente coordenador delega sub-tarefas a agentes especializados (busca, código, análise). Cada um tem tools próprios.",
                "por_que": "Especialização por contexto: cada trabalhador tem prompt e tools focados. Orquestrador foca em planejamento.",
                "conceitos": "Orchestrator-worker, specialization, hand-off, delegation."
            },
            {
                "emoji": "💬", "titulo": "Debate: dois agentes argumentam", "subtitulo": "Du et al. 2023",
                "o_que_e": "Dois agentes resolvem a mesma tarefa, comparam respostas, debatem discordâncias até convergir.",
                "por_que": "Em raciocínio adversarial, debate consistente bate single agent. Custo: 2-3× mais tokens.",
                "conceitos": "Multi-agent debate, adversarial reasoning, consensus protocol."
            },
            {
                "emoji": "🗂️", "titulo": "Blackboard: estado compartilhado", "subtitulo": "Memória comum",
                "o_que_e": "Agentes leem e escrevem em um 'quadro' compartilhado. Comunicação assíncrona via state, não messaging direto.",
                "por_que": "Para workflows longos onde agentes trabalham em paralelo em sub-tarefas, blackboard é mais escalável que conversation.",
                "conceitos": "Blackboard architecture, shared state, async coordination."
            },
            {
                "emoji": "🔌", "titulo": "MCP: Model Context Protocol", "subtitulo": "Anthropic 2024",
                "o_que_e": "Protocolo aberto para conectar LLMs a fontes de dados e tools externos. Inspirado em LSP do mundo de IDE.",
                "por_que": "Padroniza integração: um servidor MCP serve tools/resources que qualquer cliente pode consumir.",
                "conceitos": "MCP, tools, resources, prompts, transport (stdio, SSE)."
            },
            {
                "emoji": "🤝", "titulo": "Handoff: passar contexto entre agentes", "subtitulo": "Resumir + delegar",
                "o_que_e": "Quando agente A passa para B, sumariza o estado relevante. Não passar histórico inteiro = economia + atenção.",
                "por_que": "Histórico cresce; contexto cresce; lost-in-the-middle entra em jogo. Handoff explícito mitiga.",
                "conceitos": "Context compression, state handoff, summary message."
            },
            {
                "emoji": "🚫", "titulo": "Quando UM agente é melhor", "subtitulo": "A maioria dos casos",
                "o_que_e": "Tarefas que cabem em um único contexto coerente, sem trabalho paralelizável real, são piores com multi-agente.",
                "por_que": "Multi-agente adiciona: handoff loss, custo extra, complexidade de tracing. Default ao single agent é honesto.",
                "conceitos": "Default to simple, complexity budget, when-not-to."
            },
        ],
        "conceito_principal": {
            "emoji": "🎯", "titulo": "Default ao single agent",
            "texto": "Multi-agente é uma promoção condicional do single agent — só compensa quando há benefício REAL (especialização, debate, paralelismo).",
            "lista": [
                "Tarefa cabe em 1 agente bem-feito? <strong>Use 1.</strong>",
                "Especialização exige tools/contexto distintos? <strong>Orquestrador + trabalhadores.</strong>",
                "Crítica adversarial valida raciocínio? <strong>Debate.</strong>",
                "Trabalho paralelo independente? <strong>Blackboard.</strong>",
                "Sempre: handoff explícito + tracing global."
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Comece com 1 agente, prove que precisa de mais",
            "texto": "Antes de multi-agente, esgote single agent com bons tools e prompts. Multi-agente é resposta a problema medido, não default."
        },
        "fazer_evitar": [
            ("Tracing global atravessa todos os agentes", "Tracing isolado por agente"),
            ("Handoff com sumário explícito", "Passar histórico inteiro entre agentes"),
            ("Comparação de custo single vs multi no harness", "Adotar multi por inércia"),
            ("MCP server para tools reusáveis", "Reimplementar tools em cada agente"),
        ],
        "quando_nao_usar": [
            "<strong>Tarefa cabe em single agent</strong>: multi adiciona overhead sem ganho.",
            "<strong>Latência crítica</strong>: cada agente é roundtrip; multi multiplica.",
            "<strong>Sem tracing global</strong>: debug em multi-agente sem trace é desastre.",
        ],
        "exemplo_codigo": (
            "# Padrão orquestrador + trabalhadores (esquemático)\n"
            "def orquestrador(query: str) -> str:\n"
            "    plano = llm_planejar(query)  # decompõe em sub-tarefas\n"
            "    resultados = []\n"
            "    for tarefa in plano:\n"
            "        if tarefa.tipo == \"busca\":\n"
            "            r = trabalhador_busca(tarefa.descricao)\n"
            "        elif tarefa.tipo == \"código\":\n"
            "            r = trabalhador_codigo(tarefa.descricao)\n"
            "        # ... outros especialistas\n"
            "        resultados.append({\"tarefa\": tarefa, \"resultado\": r.summary})  # handoff = sumário\n"
            "    return llm_consolidar(query, resultados)"
        ),
        "exercicio": "Compare single agent vs orquestrador+trabalhadores em uma tarefa multi-domínio. Tabela com custo, latência, qualidade. Justifique a escolha. Em <code>projetos/post-launch/P3/</code>.",
        "bibliografia": [
            ("Du et al. (2023)", "Improving Factuality and Reasoning via Multi-Agent Debate", "https://arxiv.org/abs/2305.14325"),
            ("Anthropic (2024)", "Model Context Protocol", "https://modelcontextprotocol.io"),
            ("Park et al. (2023)", "Generative Agents", "https://arxiv.org/abs/2304.03442"),
            ("Hong et al. (2023)", "MetaGPT", "https://arxiv.org/abs/2308.00352"),
        ],
        "resumo": [
            "<strong>Default ao single agent</strong> — multi exige justificativa medida.",
            "<strong>Orquestrador-trabalhador</strong> é o padrão mais útil.",
            "<strong>Debate</strong> bate single em raciocínio adversarial (custo 2-3×).",
            "<strong>MCP</strong> padroniza integração de tools/resources.",
            "<strong>Handoff</strong> = sumário, não histórico inteiro.",
        ],
        "proximo_id": "../trilha5/index.html",
        "proximo_titulo": "T5 — Memória e Compressão",
    },

    # =================== T5 — MEMÓRIA E COMPRESSÃO ===================
    {
        "id": "modulo-5-1", "trilha": 5, "numero": "5.1", "status": "GA",
        "titulo": "Estratégias de memória: curto, longo prazo e summarização hierárquica",
        "emoji": "💾",
        "descricao": "Como dar 'memória' a um agente: buffer de turn, summarização hierárquica, vetor de longo prazo, recall sob demanda.",
        "minutos": 60, "nivel": "Intermediário", "tipo": "Prático",
        "introducao": (
            "Modelos não têm memória entre chamadas — você reconstrói a janela cada vez. "
            "Aqui você aprende a <strong class='text-teal-400'>simular memória</strong>: buffer de últimos turns, sumarização incremental, "
            "vetor para longo prazo, recall por similaridade. Um chat 'que lembra' é resultado dessas técnicas combinadas."
        ),
        "topicos": [
            {
                "emoji": "📥", "titulo": "Buffer de turns: memória de curto prazo", "subtitulo": "Últimos N turns",
                "o_que_e": "Manter os últimos N turns inteiros na janela. Simples, eficaz para conversas curtas.",
                "por_que": "Em chats curtos (5-10 turns), buffer puro basta. Modelos atendem bem com janela &lt;10k.",
                "conceitos": "Sliding window, message buffer, FIFO eviction."
            },
            {
                "emoji": "📝", "titulo": "Summarização incremental", "subtitulo": "Comprimir o que sai do buffer",
                "o_que_e": "Quando buffer estoura, sumariza turns antigos em parágrafo. Sumário fica no system prompt.",
                "por_que": "Mantém continuidade sem inflar janela. Trade-off: perde detalhe do que foi sumarizado.",
                "conceitos": "Recursive summarization, sliding-window summarization, hierarchical."
            },
            {
                "emoji": "🌳", "titulo": "Sumarização hierárquica: árvore de memória", "subtitulo": "Múltiplos níveis",
                "o_que_e": "Sumariza turns em sumário-de-1; sumários-de-1 em sumário-de-2; etc. Estrutura tipo árvore.",
                "por_que": "Para chats longos (centenas de turns), hierarquia preserva detalhe nos níveis superiores.",
                "conceitos": "Tree summarization, multi-level memory, MemGPT."
            },
            {
                "emoji": "🗃️", "titulo": "Memória vetorial: longo prazo", "subtitulo": "Embedding de turns + recall",
                "o_que_e": "Cada turn vira embedding indexado. No próximo turn, busca turns relevantes ao tópico atual e injeta.",
                "por_que": "Permite chats que 'lembram' de conversas de meses atrás sem manter tudo na janela.",
                "conceitos": "Long-term memory, episodic memory, recall on demand, retrieval-augmented memory."
            },
            {
                "emoji": "🔍", "titulo": "Recall sob demanda: tool de memória", "subtitulo": "Agente busca a memória",
                "o_que_e": "Padrão alternativo: agente tem tool 'buscar_memoria' e decide quando precisa de info antiga.",
                "por_que": "Mais explícito que injection automático. Custo: mais roundtrips, mas precisão maior.",
                "conceitos": "Active recall, memory tool, on-demand retrieval."
            },
            {
                "emoji": "🧠", "titulo": "Personalização: persona + perfil do usuário", "subtitulo": "Memória como facto",
                "o_que_e": "Mantém ficha estruturada do usuário (nome, preferências, contexto profissional) atualizada incremental.",
                "por_que": "Diferente de memória conversacional — é estado do usuário. Cabe no system prompt como JSON pequeno.",
                "conceitos": "User profile, structured memory, preference modeling."
            },
        ],
        "conceito_principal": {
            "emoji": "🏗️", "titulo": "Camadas de memória",
            "texto": "Não é uma estratégia única — é um stack de camadas, cada uma com trade-off de custo, fidelidade e velocidade.",
            "lista": [
                "<strong>Curto prazo</strong>: buffer dos últimos N turns (simples, alto detalhe).",
                "<strong>Médio prazo</strong>: sumarização hierárquica (compacto, perde detalhe).",
                "<strong>Longo prazo</strong>: vetor + recall (escala, exige busca).",
                "<strong>Estado do usuário</strong>: ficha estruturada (estável, no system prompt).",
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Não invente memória — comece com buffer",
            "texto": "Para a maioria dos casos, buffer de 10 últimos turns + system prompt resolve. Adicione sumarização quando buffer estourar; vetor quando precisar de meses-atrás real."
        },
        "fazer_evitar": [
            ("Buffer simples para chats curtos (&lt;10 turns)", "Implementar memória vetorial dia 1"),
            ("Sumarização incremental quando buffer estoura", "Crescer janela indefinidamente"),
            ("Ficha estruturada do usuário no system prompt", "Spreadar info do usuário em N turns"),
            ("Recall explícito via tool em casos críticos", "Injection automático sem controle"),
        ],
        "quando_nao_usar": [
            "<strong>Chat estateless de 1-2 turns</strong>: nem precisa de memória, contexto da query basta.",
            "<strong>Quando privacy não permite armazenar</strong>: conformidade limita memória persistente.",
            "<strong>Casos onde fato muda</strong>: memória vetorial não distingue atual de antigo bem.",
        ],
        "exemplo_codigo": (
            "from collections import deque\n"
            "from fec_sdk import Message, MessageRole\n"
            "from fec_sdk.adapters import get_adapter\n\n"
            "class ChatComMemoria:\n"
            "    def __init__(self, max_buffer: int = 10):\n"
            "        self.buffer = deque(maxlen=max_buffer)\n"
            "        self.sumario_antigo = \"\"\n"
            "        self.client = get_adapter(\"mock\")\n\n"
            "    def turn(self, user_msg: str) -> str:\n"
            "        # Constrói janela: system com sumário + buffer + nova msg\n"
            "        system = f\"Histórico antigo (sumarizado): {self.sumario_antigo}\"\n"
            "        msgs = [Message(role=MessageRole.SYSTEM, content=system)] + list(self.buffer)\n"
            "        msgs.append(Message(role=MessageRole.USER, content=user_msg))\n\n"
            "        resp = self.client.chat(msgs)\n\n"
            "        # Atualiza buffer\n"
            "        self.buffer.append(Message(role=MessageRole.USER, content=user_msg))\n"
            "        self.buffer.append(Message(role=MessageRole.ASSISTANT, content=resp.content))\n\n"
            "        # Se buffer está cheio, sumariza o que cai fora\n"
            "        if len(self.buffer) == self.buffer.maxlen:\n"
            "            self._atualizar_sumario()\n\n"
            "        return resp.content\n\n"
            "    def _atualizar_sumario(self):\n"
            "        # Pseudo: chama LLM para sumarizar buffer + sumário antigo\n"
            "        pass"
        ),
        "exercicio": "Implemente chat com 3 camadas (buffer + sumarização + vetorial). Teste com 50 turns, medindo custo médio e recall de fatos antigos. Em <code>exercicios/modulo-5-1/</code>.",
        "bibliografia": [
            ("Packer et al. (2023)", "MemGPT: Towards LLMs as Operating Systems", "https://arxiv.org/abs/2310.08560"),
            ("Park et al. (2023)", "Generative Agents (memória episódica)", "https://arxiv.org/abs/2304.03442"),
            ("Wu et al. (2022)", "Recursive Summarization", "https://arxiv.org/abs/2105.10311"),
            ("LangChain memory", "Padrões de memória em frameworks", "https://python.langchain.com/docs/modules/memory/"),
        ],
        "resumo": [
            "<strong>Memória é construção</strong> — modelos não têm memória nativa.",
            "<strong>Buffer simples</strong> resolve chats curtos.",
            "<strong>Sumarização hierárquica</strong> escala para chats longos.",
            "<strong>Vetor + recall</strong> permite memória de longo prazo.",
            "<strong>Estado do usuário</strong> = ficha estruturada no system prompt.",
        ],
        "proximo_id": "modulo-5-2",
        "proximo_titulo": "Caching e compressão (beta)",
    },

    {
        "id": "modulo-5-2", "trilha": 5, "numero": "5.2", "status": "beta",
        "titulo": "Prompt caching e context distillation (beta)",
        "emoji": "⚡",
        "descricao": "Como reduzir custo em 80-90% com prompt caching. Quando context distillation (treinar um modelo pequeno) substitui contexto.",
        "minutos": 65, "nivel": "Avançado", "tipo": "Avançado",
        "introducao": (
            "Prompt caching é a alavanca de custo mais subestimada: <strong class='text-teal-400'>10% do preço para tokens cacheados</strong>. "
            "Em chats com prefix grande, isso é redução de 80-90% real. "
            "Context distillation vai além: substitui contexto longo por modelo treinado. Ambos têm trade-offs concretos."
        ),
        "topicos": [
            {
                "emoji": "💰", "titulo": "Prompt caching (Anthropic, OpenAI)", "subtitulo": "10% do preço para hits",
                "o_que_e": "Provedor cacheia o prefixo da janela. Próxima chamada com mesmo prefixo: tokens cacheados custam ~10% do normal.",
                "por_que": "Em chat com system prompt + few-shot grandes, redução real de 80-90% no custo de input.",
                "conceitos": "Prompt cache, cache_control, cache breakpoints, TTL (5min Anthropic), hit rate."
            },
            {
                "emoji": "🎯", "titulo": "Cache breakpoints: onde marcar", "subtitulo": "Estável vs variável",
                "o_que_e": "Você marca pontos do prompt como 'cacheável'. Anthropic: até 4 breakpoints. OpenAI: automático para prefixos &gt;1024 tokens.",
                "por_que": "Cache só vale se o prefixo até o breakpoint for ESTÁVEL. Mexer no system prompt invalida tudo daquele ponto pra frente.",
                "conceitos": "Cache anchor, prefix stability, partial invalidation."
            },
            {
                "emoji": "📊", "titulo": "Medir hit rate: você está economizando?", "subtitulo": "Métrica explícita",
                "o_que_e": "Cada chamada retorna métricas: tokens lidos do cache vs. tokens novos. Hit rate = cached / total.",
                "por_que": "Sem medir hit rate, você não sabe se cache está funcionando. Pequena mudança no prefix derruba hit para 0.",
                "conceitos": "Hit rate, cache miss, cache invalidation, observability."
            },
            {
                "emoji": "🧪", "titulo": "Context distillation: substituir contexto por modelo", "subtitulo": "Treinar pequeno",
                "o_que_e": "Treinar (fine-tune) um modelo pequeno usando inputs e outputs do modelo grande com contexto longo. Modelo pequeno aprende sem precisar do contexto.",
                "por_que": "Para tarefa fixada e volume alto, distillation reduz custo dramaticamente — sem precisar do contexto a cada chamada.",
                "conceitos": "Knowledge distillation, fine-tuning, teacher-student, dataset curation."
            },
            {
                "emoji": "📦", "titulo": "Compressão por sumarização", "subtitulo": "LLMLingua, sumário do contexto",
                "o_que_e": "Comprimir contexto longo em representação mais densa antes de mandar (via sumarização ou modelo de compressão).",
                "por_que": "Para tarefas onde detalhe completo não é crítico, compressão reduz tokens sem cair muito a qualidade.",
                "conceitos": "LLMLingua (Jiang 2023), compression ratio, lossy compression."
            },
            {
                "emoji": "⚠️", "titulo": "Quando caching/distillation NÃO valem", "subtitulo": "Casos onde não compensa",
                "o_que_e": "Cache não vale com prefix instável. Distillation não vale com tarefa que muda rápido. Compressão não vale com tarefa que exige fidelidade.",
                "por_que": "Cada técnica tem zona de aplicabilidade — assumir que sempre vale é o erro mais comum.",
                "conceitos": "Applicability, regression risk, distillation drift."
            },
        ],
        "conceito_principal": {
            "emoji": "💰", "titulo": "Hierarquia de otimização de custo",
            "texto": "Antes de invocar técnicas avançadas, esgote as simples. Caching é low-hanging fruit; distillation é trabalho pesado.",
            "lista": [
                "<strong>1. Reduzir tokens</strong>: prompts mais curtos, RAG bom em vez de contexto longo.",
                "<strong>2. Trocar de modelo</strong>: low-cost onde frontier é desnecessário.",
                "<strong>3. Prompt caching</strong>: ganha 80% sem mudar capability.",
                "<strong>4. Compressão</strong>: lossy mas eficaz em casos certos.",
                "<strong>5. Distillation</strong>: trabalho de ML, ganho permanente."
            ]
        },
        "dados_pesquisa": {
            "titulo": "Anthropic Prompt Caching (2024)",
            "items": [
                "<strong>~10%</strong> do preço normal para tokens lidos do cache.",
                "<strong>5 min de TTL</strong> (Anthropic) — chamadas espaçadas perdem cache.",
                "<strong>Hit rate típico em chats:</strong> 70-95% se prefix bem estruturado.",
            ]
        },
        "fazer_evitar": [
            ("Marcar cache_control após system prompt + few-shot", "Sem caching habilitado em prefixos repetidos"),
            ("Medir hit rate em produção", "Assumir que cache 'está funcionando'"),
            ("Estabilizar system prompt antes de cachear", "Mexer no prefix invalidando cache"),
            ("Distillation com eval rigoroso vs modelo grande", "Distillation que regrede silenciosamente"),
        ],
        "quando_nao_usar": [
            "<strong>Prefix muda a cada turn</strong>: cache nunca hita.",
            "<strong>Volume baixo</strong>: economia absoluta é trivial; complexidade não vale.",
            "<strong>Tarefa que muda rápido</strong>: distillation envelhece, modelo grande adapta.",
        ],
        "exemplo_codigo": (
            "# Anthropic prompt caching (esquemático)\n"
            "import anthropic\n\n"
            "client = anthropic.Anthropic()\n\n"
            "system_grande = \"\"\"Você é um assistente especializado...\n"
            "[10k tokens de regras, exemplos, etc.]\"\"\"\n\n"
            "# Marcar cache_control no fim do prefix estável\n"
            "resp = client.messages.create(\n"
            "    model=\"claude-sonnet-4-6@2026-04\",\n"
            "    system=[\n"
            "        {\"type\": \"text\", \"text\": system_grande,\n"
            "         \"cache_control\": {\"type\": \"ephemeral\"}}\n"
            "    ],\n"
            "    messages=[{\"role\": \"user\", \"content\": \"pergunta atual\"}],\n"
            "    max_tokens=500,\n"
            ")\n\n"
            "# resp.usage tem: input_tokens, cache_creation_input_tokens, cache_read_input_tokens\n"
            "hit_rate = resp.usage.cache_read_input_tokens / (\n"
            "    resp.usage.cache_read_input_tokens + resp.usage.cache_creation_input_tokens\n"
            ")"
        ),
        "exercicio": "Em chat de 20 turns com system prompt de 5k tokens, meça custo SEM cache e COM cache. Hit rate alvo: ≥80%. Em <code>exercicios/modulo-5-2/</code> ou simulação por gravação.",
        "bibliografia": [
            ("Anthropic (2024)", "Prompt caching with Claude", "https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching"),
            ("OpenAI (2024)", "Prompt caching", "https://platform.openai.com/docs/guides/prompt-caching"),
            ("Hinton et al. (2015)", "Distilling Knowledge in a Neural Network", "https://arxiv.org/abs/1503.02531"),
            ("Jiang et al. (2023)", "LLMLingua: Compressing Prompts", "https://arxiv.org/abs/2310.05736"),
        ],
        "resumo": [
            "<strong>Prompt caching</strong>: 10% do preço para hits — ganho real 80%.",
            "<strong>Hit rate</strong> precisa ser MEDIDO; pequena mudança derruba.",
            "<strong>Distillation</strong> substitui contexto longo por modelo treinado.",
            "<strong>Compressão</strong> é lossy — eval obrigatório.",
            "<strong>Hierarquia de otimização</strong>: simples primeiro, complexo depois.",
        ],
        "proximo_id": "../trilha6/index.html",
        "proximo_titulo": "T6 — Avaliação e Produção",
    },

    # =================== T6 — AVALIAÇÃO E PRODUÇÃO ===================
    {
        "id": "modulo-6-1", "trilha": 6, "numero": "6.1", "status": "GA",
        "titulo": "Evals: golden sets, LLM-as-judge e tracing",
        "emoji": "📊",
        "descricao": "A disciplina que costura T1-T5: golden sets, métricas, LLM-as-judge (e seus vieses), tracing estruturado, prompt injection sandboxed.",
        "minutos": 70, "nivel": "Avançado", "tipo": "Hands-on",
        "introducao": (
            "Eval é o que separa engenharia de contexto de <strong class='text-rose-400'>chute organizado</strong>. "
            "Aqui você aprende a montar harness reproduzível, escolher métricas, lidar com vieses do LLM-as-judge, "
            "e instrumentar tracing — pré-requisito de toda produção séria."
        ),
        "topicos": [
            {
                "emoji": "🎯", "titulo": "Golden set: o que entra, o que não", "subtitulo": "Curadoria deliberada",
                "o_que_e": "Conjunto fixo de exemplos com gabarito. Cobertura: casos típicos + edge cases + adversariais. Tamanho: 30-200.",
                "por_que": "Sem golden set, você não tem como medir se o sistema melhorou ou regrediu. Curadoria é trabalho real.",
                "conceitos": "Golden set, edge cases, adversarial examples, distribution coverage, frozen set."
            },
            {
                "emoji": "📐", "titulo": "Métricas por tipo de tarefa", "subtitulo": "Não existe métrica universal",
                "o_que_e": "Classificação: accuracy, F1. Geração: BLEU, ROUGE. RAG: groundedness, citation accuracy. Agente: task completion.",
                "por_que": "Métrica errada esconde regressão. Para cada tarefa, escolher 1 primária + 1-2 secundárias.",
                "conceitos": "Primary metric, secondary metrics, distribution-level vs example-level."
            },
            {
                "emoji": "⚖️", "titulo": "LLM-as-judge: poderoso e enviesado", "subtitulo": "Calibração obrigatória",
                "o_que_e": "Usar um modelo para julgar saída de outro. Útil para qualidade subjetiva (groundedness, helpfulness).",
                "por_que": "Permite eval em escala. Mas tem vieses (favorece outputs longos, bias de posição em comparação) — calibrar com humanos.",
                "conceitos": "LLM judge, calibration, Cohen's kappa, position bias, length bias."
            },
            {
                "emoji": "🔍", "titulo": "Tracing estruturado: cada step visível", "subtitulo": "OpenTelemetry, Honeycomb, Phoenix",
                "o_que_e": "Cada chamada vira span: timestamp, modelo, prompt, resposta, custo, latência. Hierarquia preserva sub-chamadas (RAG, agente).",
                "por_que": "Sem tracing, debug em produção é impossível. Padrão da indústria amadurece (OTel para LLMs).",
                "conceitos": "Trace, span, OpenTelemetry, semconv, Phoenix (Arize)."
            },
            {
                "emoji": "🛡️", "titulo": "Prompt injection sandboxed", "subtitulo": "Defesa em camadas",
                "o_que_e": "Padrões para detectar e neutralizar: spotlight (Anthropic), input/output guard, allow-list de tools, separação de escopo.",
                "por_que": "Em produção, payloads vão tentar exfiltrar dados ou abusar tools. Defesa em camadas é única abordagem séria.",
                "conceitos": "Spotlight, input guard, output guard, tool allow-list, escape boundaries."
            },
            {
                "emoji": "💸", "titulo": "Custo é uma métrica de produto", "subtitulo": "Tracker em produção",
                "o_que_e": "Tracking de tokens in/out, modelo, hit de cache por request. Dashboard com custo por feature/usuário.",
                "por_que": "Sem tracking, custo escala silenciosamente. Surpresa de fatura mensal é falha de instrumentação.",
                "conceitos": "Cost per request, cost per user, cache hit dashboard, budget alerts."
            },
        ],
        "conceito_principal": {
            "emoji": "📋", "titulo": "Harness FEC-EVAL: o padrão que você implementa",
            "texto": "Espelho do que está em <code>evals/v1/</code> do curso. Reprodutibilidade vem de fixar TUDO: dataset, judge, modelo, sementes.",
            "lista": [
                "<strong>Dataset</strong>: golden set versionado, hash sha256.",
                "<strong>Judge prompt</strong>: versionado, calibrado contra humanos (Cohen κ ≥0.6).",
                "<strong>Modelos pinados</strong>: ID exato + data (ex.: <code>claude-sonnet-4-6@2026-04</code>).",
                "<strong>Sementes</strong>: temperature 0, seed fixa.",
                "<strong>Manifest</strong>: sha256 de todos os inputs + métricas em JSON content-addressed.",
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Comece com 30 exemplos",
            "texto": "Não precisa de 1000. 30 exemplos bem-curados (típicos + edge + adversariais) já estabelecem a disciplina. Depois, cresça para 200 conforme casos surgem em produção."
        },
        "fazer_evitar": [
            ("Golden set versionado em git, hash registrado", "Golden em planilha que muda sem aviso"),
            ("Calibrar LLM-as-judge contra 30 amostras humanas (κ ≥0.6)", "Confiar no judge sem validar"),
            ("Tracing estruturado desde dia 1", "Adicionar tracing depois do incidente"),
            ("Custo como métrica visível no dashboard", "Descobrir custo no fechamento da fatura"),
        ],
        "quando_nao_usar": [
            "<strong>Protótipo descartável</strong>: eval custa tempo; nem tudo precisa.",
            "<strong>Métrica errada selecionada</strong>: eval inválido é pior que sem eval.",
            "<strong>LLM-as-judge não-calibrado</strong>: números enganosos.",
        ],
        "exemplo_codigo": (
            "# Eval mínimo no padrão FEC-EVAL\n"
            "import json\n"
            "import hashlib\n"
            "from fec_sdk.adapters import get_adapter\n\n"
            "def rodar_eval(golden_path: str, sistema: callable) -> dict:\n"
            "    golden = json.load(open(golden_path))\n"
            "    judge = get_adapter(\"anthropic\", model=\"claude-sonnet-4-6@2026-04\")\n\n"
            "    resultados = []\n"
            "    for ex in golden[\"examples\"]:\n"
            "        resposta = sistema(ex[\"question\"])\n"
            "        score = judge_groundedness(judge, ex, resposta)\n"
            "        resultados.append({\"id\": ex[\"id\"], \"score\": score})\n\n"
            "    metricas = {\n"
            "        \"groundedness_mean\": sum(r[\"score\"] for r in resultados) / len(resultados),\n"
            "        \"n_examples\": len(resultados),\n"
            "    }\n\n"
            "    # Manifest content-addressed\n"
            "    manifest = {\n"
            "        \"dataset_sha256\": hashlib.sha256(open(golden_path, \"rb\").read()).hexdigest(),\n"
            "        \"judge_model\": judge.model_id(),\n"
            "        \"metrics\": metricas,\n"
            "    }\n"
            "    return manifest"
        ),
        "exercicio": "Implemente eval de groundedness contra FEC-GS-RAG-v1. Calibre seu judge com 10 amostras humanas. Reporte κ + métricas. Em <code>exercicios/modulo-6-1/</code>.",
        "bibliografia": [
            ("Zheng et al. (2023)", "Judging LLM-as-a-Judge", "https://arxiv.org/abs/2306.05685"),
            ("Anthropic (2024)", "Defending against prompt injection (Spotlight)", "https://www.anthropic.com"),
            ("Greshake et al. (2023)", "Indirect Prompt Injection", "https://arxiv.org/abs/2302.12173"),
            ("OpenTelemetry", "GenAI semconv", "https://opentelemetry.io/docs/specs/semconv/gen-ai/"),
        ],
        "resumo": [
            "<strong>Golden set versionado</strong> é a base de eval reproduzível.",
            "<strong>Métrica certa para a tarefa</strong> — não existe universal.",
            "<strong>LLM-as-judge</strong>: poderoso, mas calibrar contra humanos.",
            "<strong>Tracing estruturado</strong> + custo são pré-requisitos de produção.",
            "<strong>Defesa contra injection</strong> em camadas: input + output + sandbox.",
        ],
        "proximo_id": "modulo-6-2",
        "proximo_titulo": "Operacionalização avançada (beta)",
    },

    {
        "id": "modulo-6-2", "trilha": 6, "numero": "6.2", "status": "beta",
        "titulo": "Operacionalização avançada: A/B, canários, rollback (beta)",
        "emoji": "🚀",
        "descricao": "Levar para produção: A/B em prompt, canários por modelo, rollback, observabilidade contínua. O que se aprende rodando, não no laboratório.",
        "minutos": 65, "nivel": "Avançado", "tipo": "Avançado",
        "introducao": (
            "Tudo que você aprendeu até aqui se prova em <strong class='text-rose-400'>produção</strong>. "
            "Aqui você vê padrões para deploy seguro: A/B, canário, rollback rápido, observabilidade. "
            "Este módulo é <em>beta</em> — práticas amadurecem com a indústria."
        ),
        "topicos": [
            {
                "emoji": "🆎", "titulo": "A/B em prompt: variant + métrica primária", "subtitulo": "Decisão por dado, não opinião",
                "o_que_e": "Roteia % do tráfego para variant. Mede métrica primária (groundedness, satisfação) com significância estatística.",
                "por_que": "Mudanças em prompt são frequentes; A/B distingue 'achei que melhorou' de 'melhorou medido'.",
                "conceitos": "A/B test, variant routing, statistical significance, sample size."
            },
            {
                "emoji": "🐤", "titulo": "Canário: rollout incremental", "subtitulo": "5% → 25% → 100%",
                "o_que_e": "Liberar mudança para 5% do tráfego, observar métricas + custo + erro. Subir gradualmente se OK.",
                "por_que": "Mudança de modelo (de Claude 4.5 para 4.6) pode quebrar 5% dos casos. Canário pega antes do fan-out.",
                "conceitos": "Canary release, progressive rollout, blast radius, kill switch."
            },
            {
                "emoji": "↩️", "titulo": "Rollback rápido: pré-requisito de canário", "subtitulo": "1 click",
                "o_que_e": "Botão 'voltar' que reverte para versão anterior em segundos. Versão anterior precisa estar 'quente' (warm cache).",
                "por_que": "Sem rollback, canário é teatro. Quando dá problema, você precisa MUITO de voltar rápido.",
                "conceitos": "Hot rollback, warm standby, version pinning, traffic shift."
            },
            {
                "emoji": "📈", "titulo": "Observabilidade contínua: o que monitorar", "subtitulo": "Métricas + alertas",
                "o_que_e": "Dashboards: latência p50/p95, erro rate, custo, hit de cache, qualidade (LLM-judge contínuo). Alertas em desvios.",
                "por_que": "Em produção, problemas se manifestam por números antes de virarem reclamação. Instrumentação detecta cedo.",
                "conceitos": "SLO, SLI, alerting, dashboard, distribution shift detection."
            },
            {
                "emoji": "🛑", "titulo": "Kill switch: parar feature instantaneamente", "subtitulo": "Botão de emergência",
                "o_que_e": "Flag de configuração que desabilita a feature LLM. Tráfego volta para fallback estático ou erro educativo.",
                "por_que": "Modelo do provedor pode degradar do nada. Kill switch dá tempo de investigar sem disaster.",
                "conceitos": "Feature flag, kill switch, fallback, graceful degradation."
            },
            {
                "emoji": "🔁", "titulo": "Eval contínuo em produção", "subtitulo": "Não só pré-deploy",
                "o_que_e": "% pequena do tráfego é avaliada em tempo real (LLM-judge automático). Detecta drift sem esperar reclamação.",
                "por_que": "Modelos provider mudam; corpus muda; usuários mudam. Eval só pré-deploy envelhece.",
                "conceitos": "Production eval, live judge, drift detection, sampling rate."
            },
        ],
        "conceito_principal": {
            "emoji": "🚦", "titulo": "Anatomia do deploy seguro de LLM",
            "texto": "Não é sobre ter coragem — é sobre ter os switches certos antes de precisar deles.",
            "lista": [
                "<strong>1. A/B em pequena %</strong> com métrica primária e timeline.",
                "<strong>2. Canário</strong>: 5% → 25% → 100% se métricas OK.",
                "<strong>3. Rollback</strong> hot, em &lt;1 min.",
                "<strong>4. Kill switch</strong> independente do rollback.",
                "<strong>5. Eval contínuo</strong> + alertas.",
            ]
        },
        "dica_pratica": {
            "emoji": "💡", "titulo": "Implemente kill switch antes de qualquer rollout",
            "texto": "Não confie em rollback. Kill switch deve estar em produção e testado antes da primeira liberação. Sem isso, você está exposto a desastre."
        },
        "fazer_evitar": [
            ("A/B com métrica primária e sample size calculado", "Eyeballing 'parece melhor'"),
            ("Canário 5% → 25% → 100% por dia", "Big bang rollout"),
            ("Kill switch testado e documentado", "'Vamos torcer pra não dar problema'"),
            ("Eval contínuo em produção sampling 1-5%", "Eval só em CI"),
        ],
        "quando_nao_usar": [
            "<strong>Volume baixo</strong>: A/B precisa de N significativo; com pouco tráfego, espera mais.",
            "<strong>Mudança trivial e auditada</strong>: typo de prompt não precisa de canário.",
            "<strong>Sem instrumentação básica</strong>: implemente tracing ANTES de pensar em rollout sofisticado.",
        ],
        "exemplo_codigo": (
            "# Esquema de feature flag + canário\n"
            "from random import random\n\n"
            "def chamar_modelo(query: str, user_id: str) -> str:\n"
            "    # Kill switch — flag externo (ex.: ConfigCat, LaunchDarkly, env var)\n"
            "    if feature_flag(\"llm_enabled\") is False:\n"
            "        return fallback_estatico(query)\n\n"
            "    # Canário: 5% recebe variant nova\n"
            "    if hash(user_id) % 100 < 5:\n"
            "        variant = \"v1.1.0\"\n"
            "    else:\n"
            "        variant = \"v1.0.0\"  # estável\n\n"
            "    resposta = pipeline_llm(query, variant=variant)\n\n"
            "    # Eval contínuo: 1% do tráfego é judgeado\n"
            "    if random() < 0.01:\n"
            "        score = judge_async(query, resposta)\n"
            "        emit_metric(\"groundedness\", score, tags={\"variant\": variant})\n\n"
            "    return resposta"
        ),
        "exercicio": "Adicione A/B + canário + kill switch + eval contínuo ao P5 (pipeline em produção). Demonstre rollback em 1 min. Em <code>projetos/P5/</code>.",
        "bibliografia": [
            ("Google SRE Book", "Production rollout best practices", "https://sre.google/sre-book/"),
            ("Honeycomb", "Observability for LLM systems", "https://www.honeycomb.io"),
            ("Arize AI", "ML observability", "https://arize.com/llm-observability"),
            ("Anthropic (2024)", "Building safer agentic systems", "https://www.anthropic.com"),
        ],
        "resumo": [
            "<strong>A/B em prompt</strong> com métrica primária e significância.",
            "<strong>Canário</strong> 5%→25%→100% — não big bang.",
            "<strong>Kill switch</strong> antes de qualquer rollout.",
            "<strong>Rollback hot</strong> &lt;1 min — pré-requisito de canário.",
            "<strong>Eval contínuo</strong> em produção captura drift.",
        ],
        "proximo_id": "../../projetos/P5/README.md",
        "proximo_titulo": "Projeto Final P5 — Pipeline em produção",
    },

]

