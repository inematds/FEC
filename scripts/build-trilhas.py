#!/usr/bin/env python3
"""build-trilhas.py — gera os 6 index.html das trilhas no padrão INEMA.

Cards de módulo com 3 sub-tópicos preview + botão "Ver Completo".
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from modulos_spec import MODULOS, TRILHAS  # noqa: E402

REPO = Path(__file__).resolve().parent.parent

CSP = "default-src 'none'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'none'; frame-src 'self'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests"


def _css_version() -> str:
    css = REPO / "assets/css/inema.css"
    if not css.exists():
        return "dev"
    import hashlib
    return hashlib.sha256(css.read_bytes()).hexdigest()[:8]


CSS_V = _css_version()


DESCRICOES = {
    1: "Os fundamentos operacionais: janela de contexto, atenção, tokens, custo. Pré-requisito de todas as outras trilhas.",
    2: "System prompt, few-shot, formato XML/JSON, ancoragem, versionamento de prompt e o eval primer.",
    3: "RAG bem-feito: chunking, embeddings, BM25 híbrido, reranking, contextual retrieval (Anthropic 2024) e citações obrigatórias.",
    4: "Tool/function calling provider-neutral, agentes single (ReAct), padrões multi-agente e MCP.",
    5: "Memória curto/longo prazo, summarização hierárquica, prompt caching e context distillation.",
    6: "Golden sets, LLM-as-judge, tracing, prompt injection sandboxed, A/B em produção e rollback.",
}


# Explicação rica do que cada trilha explora — exibida abaixo do header da trilha
EXPLORA = {
    1: {
        "objetivo": "Construir o modelo mental de como o modelo lê de fato uma mensagem.",
        "topicos": [
            "Janela de contexto como sequência fixa serializada — não 'conversa'.",
            "Atenção causal e KV cache; por que prefixos estáveis são cacheáveis.",
            "Lost in the middle (Liu et al. 2023) e mitigações validadas.",
            "Posição via RoPE; ordem de seções estável→variável→instrução.",
            "Tokens e tokenização (BPE/SentencePiece); custo input vs. output.",
            "Os três níveis de modelo: frontier, low-cost, OSS local.",
        ],
        "para_quem": "Todo aluno. Pré-requisito das outras 5 trilhas — não pule.",
    },
    2: {
        "objetivo": "Tratar prompt como código: estrutura, versionamento, eval automatizado.",
        "topicos": [
            "Anatomia da mensagem em 5 seções estáveis.",
            "System prompt, few-shot canônico, formato declarativo XML/JSON.",
            "Padrão FEC de ordem: estável → variável → âncora → user turn.",
            "Ancoragem dupla; chain-of-thought quando vale.",
            "Prompts versionados em arquivo (Jinja2/templates), SemVer aplicado.",
            "Eval primer: golden set + mini-eval em toda mudança de prompt.",
        ],
        "para_quem": "Quem pretende manter prompts em produção, não 'tunar pra demo'.",
    },
    3: {
        "objetivo": "Construir RAG que responde com citações e atinge groundedness ≥0.85.",
        "topicos": [
            "Chunking deliberado (500 tokens + overlap, fronteira semântica).",
            "Embeddings densos vs BM25; híbrido com Reciprocal Rank Fusion.",
            "Vector stores (FAISS, pgvector, Qdrant) e ANN.",
            "Reranking cross-encoder; contextual retrieval (Anthropic 2024).",
            "Citação obrigatória + saber dizer 'não sei'.",
            "RAG agêntico (multi-hop, self-RAG) e quando NÃO usar.",
        ],
        "para_quem": "Quem precisa que o modelo responda sobre dados próprios.",
    },
    4: {
        "objetivo": "Agentes que chamam ferramentas com sandbox e tracing — não brinquedos de demo.",
        "topicos": [
            "Tool/function calling provider-neutral via JSON Schema.",
            "Description é o prompt do tool; escolha do modelo depende dela.",
            "Sandbox jailed obrigatório (filesystem, rede, processo).",
            "ReAct e planner/executor; controle de loop (max_iter, budget).",
            "Tracing por step (OpenTelemetry GenAI semconv).",
            "Multi-agente: orquestrador-trabalhador, debate, MCP.",
        ],
        "para_quem": "Quem vai colocar agente em produção. T6 vai exigir P5 baseado em T4.",
    },
    5: {
        "objetivo": "Dar 'memória' ao agente sem inflar custo nem janela.",
        "topicos": [
            "Buffer de turns (curto prazo) — solução simples para chats curtos.",
            "Sumarização incremental e hierárquica (MemGPT).",
            "Memória vetorial para longo prazo + recall por similaridade.",
            "Perfil estruturado do usuário no system prompt.",
            "Prompt caching: 10% do preço para tokens cacheados.",
            "Context distillation e compressão (LLMLingua).",
        ],
        "para_quem": "Quem opera chats com histórico longo ou quer cortar custo de input.",
    },
    6: {
        "objetivo": "Levar o sistema LLM para produção com gates objetivos e rollback rápido.",
        "topicos": [
            "Golden sets, métricas por tarefa, LLM-as-judge calibrado (κ ≥0.6).",
            "Tracing estruturado em OTel + custo como métrica de produto.",
            "Prompt injection sandboxed (defesa em camadas).",
            "A/B com significância estatística; canário 5%→25%→100%.",
            "Kill switch e rollback hot &lt;1 min.",
            "Eval contínuo em produção (sampling 1-5%).",
        ],
        "para_quem": "Pré-requisito para o projeto final P5. Disciplina que costura T1-T5.",
    },
}


def render_trilha(num: int) -> str:
    t = TRILHAS[num]
    cor = t["cor"]
    modulos_da_trilha = [m for m in MODULOS if m["trilha"] == num]
    ga = sum(1 for m in modulos_da_trilha if m["status"] == "GA")
    beta = sum(1 for m in modulos_da_trilha if m["status"] == "beta")
    total_min = sum(m["minutos"] for m in modulos_da_trilha)

    cards = []
    modais = []
    for idx, m in enumerate(modulos_da_trilha):
        # MOSTRA TODOS os 6 sub-tópicos (regra crítica INEMA: card no index = todos visíveis)
        topicos_html = []
        for i, tp in enumerate(m["topicos"], 1):
            topicos_html.append(f"""
        <details class="topico-expansivel border-b border-zinc-800 py-3 px-2 last:border-b-0">
          <summary class="cursor-pointer flex items-center gap-3 text-sm font-medium list-none hover:bg-zinc-800/40 rounded p-1 -m-1">
            <span class="topico-numero w-6 h-6 rounded-full bg-{cor}-500/20 border border-{cor}-500/30 text-{cor}-400 text-xs font-bold flex items-center justify-center flex-shrink-0">{i}</span>
            <span class="flex-1"><span>{tp["emoji"]} {tp["titulo"]}</span><span class="text-zinc-500 text-xs ml-2 hidden md:inline">— {tp["subtitulo"]}</span></span>
            <span class="text-zinc-500 text-xs">▾</span>
          </summary>
          <div class="mt-3 ml-9 space-y-2 text-xs bg-zinc-950/40 rounded p-3">
            <div><span class="text-{cor}-400 font-semibold">O que é:</span> <span class="text-zinc-300">{tp["o_que_e"]}</span></div>
            <div><span class="text-{cor}-400 font-semibold">Por que aprender:</span> <span class="text-zinc-300">{tp["por_que"]}</span></div>
            <div><span class="text-{cor}-400 font-semibold">Conceitos-chave:</span> <span class="text-zinc-300">{tp["conceitos"]}</span></div>
          </div>
        </details>""")

        status_badge = (
            f'<span class="px-2 py-0.5 bg-{cor}-500/20 text-{cor}-400 rounded text-xs font-semibold">GA</span>'
            if m["status"] == "GA" else
            f'<span class="px-2 py-0.5 bg-amber-500/20 text-amber-400 rounded text-xs font-semibold">beta</span>'
        )

        modal_id = f"modal-{m['numero'].replace('.', '-')}"

        cards.append(f"""
      <article class="modulo-card bg-zinc-900 rounded-xl border border-zinc-800 hover:border-{cor}-500/40 mb-6 transition-colors">
        <div class="p-6 border-b border-zinc-800">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <span class="text-{cor}-400 font-bold">{m['numero']}</span>
              {status_badge}
            </div>
            <span class="text-xs text-zinc-500">~{m['minutos']} min · {m['nivel']} · {m['tipo']}</span>
          </div>
          <h3 class="text-2xl font-bold mb-2 text-zinc-100">{m['emoji']} {m['titulo']}</h3>
          <p class="text-sm text-zinc-400">{m['descricao']}</p>
        </div>

        <div class="divide-y divide-zinc-800/50 px-3 py-2">
          {''.join(topicos_html)}
        </div>

        <div class="p-4 bg-zinc-800/30 flex justify-start gap-3 border-t border-zinc-800">
          <button data-modal="{modal_id}" class="btn px-4 py-2 text-sm bg-zinc-700 hover:bg-zinc-600 rounded-lg transition-colors justify-start">
            Ver em Modal
          </button>
          <a href="{m['id']}.html" class="btn px-4 py-2 text-sm bg-{cor}-600 text-white hover:bg-{cor}-500 rounded-lg transition-colors justify-start">
            Ver Completo →
          </a>
        </div>
      </article>
""")

        modais.append(f"""
    <div id="{modal_id}" class="fec-modal hidden fixed inset-0 z-50 items-center justify-center p-2 sm:p-4 bg-black/80" data-modal-backdrop>
      <div class="bg-zinc-900 rounded-xl w-full max-w-6xl h-[95vh] flex flex-col border border-zinc-700">
        <div class="p-4 border-b border-zinc-700 flex justify-between items-center flex-shrink-0">
          <div class="flex items-center gap-3">
            <span class="text-{cor}-400 font-bold">{m['numero']}</span>
            <span class="font-semibold text-zinc-100">{m['emoji']} {m['titulo']}</span>
          </div>
          <button data-modal-close class="text-zinc-400 hover:text-zinc-100 text-3xl leading-none px-2" aria-label="Fechar">&times;</button>
        </div>
        <iframe src="{m['id']}.html" class="flex-1 w-full bg-zinc-950" title="{m['titulo']}"></iframe>
      </div>
    </div>""")

    # Bloco "O que explora"
    explora = EXPLORA[num]
    explora_objetivo = explora["objetivo"]
    explora_para_quem = explora["para_quem"]
    explora_topicos_html = "".join(
        f'<li class="flex items-start gap-2"><span class="text-{cor}-400 mt-1">▸</span><span class="text-sm text-zinc-300">{t}</span></li>'
        for t in explora["topicos"]
    )

    # Cards de outras trilhas (mapa do curso)
    outras_cards = []
    for n_other, t_other in TRILHAS.items():
        if n_other == num:
            continue
        c_other = t_other["cor"]
        outras_cards.append(f"""
        <a href="../trilha{n_other}/index.html" class="block p-4 rounded-lg border border-{c_other}-500/30 bg-gradient-to-br from-{c_other}-900/40 to-zinc-900 hover:from-{c_other}-900/60 transition">
          <div class="text-{c_other}-400 text-xs font-semibold mb-1">T{n_other}</div>
          <div class="text-sm font-bold text-zinc-100">{t_other['emoji']} {t_other['nome']}</div>
        </a>""")
    outras_trilhas_cards = "".join(outras_cards)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>T{num} — {t['nome']} · FEC</title>
  <link rel="stylesheet" href="../../assets/css/inema.css?v={CSS_V}">
  <meta name="trilha" content="T{num}">
  <meta name="status" content="GA">
</head>
<body class="bg-zinc-950 text-zinc-100 font-sans antialiased min-h-screen" data-status="GA">

  <nav class="sticky top-0 z-50 bg-zinc-950/95 backdrop-blur border-b border-zinc-800">
    <div class="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3 flex-shrink-0">
        <a href="../../index.html" class="flex items-center gap-3">
          <span class="text-2xl font-bold text-primary">FEC</span>
          <span class="text-zinc-400 text-sm hidden xl:inline">Engenharia de Contexto</span>
        </a>
        <span class="text-zinc-700">|</span>
        <a href="https://inema.club" target="_blank" class="text-sky-400 hover:text-sky-300 text-sm font-medium transition">INEMA.CLUB</a>
      </div>
      <div class="hidden md:flex items-center gap-1.5 text-xs flex-1 justify-center overflow-x-auto px-4">
        <a href="../trilha1/index.html" class="px-2.5 py-1 rounded border border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20 transition whitespace-nowrap{' bg-emerald-500/20' if num==1 else ''}" title="T1 Fundamentos">T1 · Fundamentos</a>
        <a href="../trilha2/index.html" class="px-2.5 py-1 rounded border border-blue-500/30 text-blue-400 hover:bg-blue-500/20 transition whitespace-nowrap{' bg-blue-500/20' if num==2 else ''}" title="T2 Mensagem">T2 · Mensagem</a>
        <a href="../trilha3/index.html" class="px-2.5 py-1 rounded border border-purple-500/30 text-purple-400 hover:bg-purple-500/20 transition whitespace-nowrap{' bg-purple-500/20' if num==3 else ''}" title="T3 RAG">T3 · RAG</a>
        <a href="../trilha4/index.html" class="px-2.5 py-1 rounded border border-amber-500/30 text-amber-400 hover:bg-amber-500/20 transition whitespace-nowrap{' bg-amber-500/20' if num==4 else ''}" title="T4 Tools/Agentes">T4 · Agentes</a>
        <a href="../trilha5/index.html" class="px-2.5 py-1 rounded border border-teal-500/30 text-teal-400 hover:bg-teal-500/20 transition whitespace-nowrap{' bg-teal-500/20' if num==5 else ''}" title="T5 Memória">T5 · Memória</a>
        <a href="../trilha6/index.html" class="px-2.5 py-1 rounded border border-rose-500/30 text-rose-400 hover:bg-rose-500/20 transition whitespace-nowrap{' bg-rose-500/20' if num==6 else ''}" title="T6 Avaliação">T6 · Avaliação</a>
      </div>
      <div class="flex items-center gap-3 text-sm flex-shrink-0">
        <a href="../../index.html" class="md:hidden text-zinc-400">← Trilhas</a>
        <a href="https://github.com/inematds/FEC" class="hidden lg:inline text-zinc-400 hover:text-primary transition">GitHub</a>
      </div>
    </div>
  </nav>

  <header class="bg-gradient-to-br from-{cor}-900/45 via-zinc-900 to-zinc-900 py-12 border-b border-zinc-800">
    <div class="max-w-6xl mx-auto px-6">
      <span class="inline-block px-3 py-1 bg-{cor}-500/20 text-{cor}-400 text-xs font-semibold rounded-full mb-4">TRILHA {num}</span>
      <h1 class="text-3xl sm:text-4xl font-bold mb-4">{t['emoji']} {t['nome']}</h1>
      <p class="text-lg text-zinc-300 max-w-3xl mb-8">{DESCRICOES[num]}</p>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl">
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700">
          <div class="text-xl font-bold text-{cor}-400">{ga}</div>
          <div class="text-xs text-zinc-400">Módulos GA</div>
        </div>
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700">
          <div class="text-xl font-bold text-{cor}-400">{beta}</div>
          <div class="text-xs text-zinc-400">Beta</div>
        </div>
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700">
          <div class="text-xl font-bold text-{cor}-400">~{total_min // 60}h</div>
          <div class="text-xs text-zinc-400">Duração</div>
        </div>
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700">
          <div class="text-xl font-bold text-{cor}-400">{6 * len(modulos_da_trilha)}</div>
          <div class="text-xs text-zinc-400">Tópicos</div>
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-6 py-12">

    <!-- O que esta trilha explora (resumo rico) -->
    <section class="mb-12 bg-gradient-to-br from-{cor}-900/20 to-zinc-900 rounded-xl border border-{cor}-500/30 p-6 md:p-8">
      <div class="grid md:grid-cols-3 gap-6">
        <div class="md:col-span-2">
          <h3 class="text-xl font-bold text-{cor}-400 mb-3 flex items-center"><span class="mr-2">🎯</span> Objetivo desta trilha</h3>
          <p class="text-zinc-200 mb-6 leading-relaxed">{explora_objetivo}</p>
          <h3 class="text-xl font-bold text-{cor}-400 mb-3 flex items-center"><span class="mr-2">🔍</span> O que você vai explorar</h3>
          <ul class="space-y-2">
            {explora_topicos_html}
          </ul>
        </div>
        <div>
          <div class="bg-zinc-900/60 rounded-lg p-4 border border-zinc-800">
            <h4 class="text-{cor}-400 font-semibold mb-2 text-sm">👤 Para quem</h4>
            <p class="text-zinc-300 text-sm">{explora_para_quem}</p>
          </div>
        </div>
      </div>
    </section>

    <h2 class="text-2xl font-bold mb-6">📚 Módulos da trilha</h2>

    {''.join(cards)}

    <section class="mt-12 p-6 rounded-lg border border-zinc-700 bg-zinc-900/50">
      <h3 class="text-lg font-bold mb-2">🔬 Bibliografia da trilha</h3>
      <p class="text-sm text-zinc-400 mb-3">Referências datadas, congeladas na release. Lista completa em <code>bibliografia/T{num}.md</code>.</p>
      <a href="../../bibliografia/T{num}.md" class="btn px-4 py-2 border border-zinc-700 text-zinc-200 rounded hover:bg-zinc-800 transition justify-start">
        Bibliografia T{num} →
      </a>
    </section>

    <!-- Outras trilhas (mapa do curso) -->
    <section class="mt-12">
      <h3 class="text-lg font-bold mb-4">🗺️ Outras trilhas</h3>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
        {outras_trilhas_cards}
      </div>
    </section>

  </main>

  <!-- MODAIS DOS MÓDULOS (carregam módulo via iframe) -->
  {''.join(modais)}

  <footer class="border-t border-zinc-800 mt-16">
    <div class="max-w-6xl mx-auto px-6 py-8 text-sm text-zinc-500 flex flex-wrap items-center justify-between gap-4">
      <div>
        <a href="https://inema.club" target="_blank" class="text-sky-400 hover:text-sky-300">INEMA.CLUB</a> ·
        Conteúdo CC BY-SA 4.0 · Código MIT
      </div>
      <div class="flex gap-6">
        <a href="../../SECURITY.md" class="hover:text-zinc-300">Segurança</a>
        <a href="../../CONTRIBUTING.md" class="hover:text-zinc-300">Contribuir</a>
      </div>
    </div>
  </footer>

  <script src="../../assets/js/inema.js?v={CSS_V}" defer></script>

</body>
</html>
"""


def main() -> int:
    for num in TRILHAS.keys():
        out_path = REPO / "curso" / f"trilha{num}" / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_trilha(num), encoding="utf-8")
        print(f"WROTE  {out_path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
