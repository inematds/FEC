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

DESCRICOES = {
    1: "Os fundamentos operacionais: janela de contexto, atenção, tokens, custo. Pré-requisito de todas as outras trilhas.",
    2: "System prompt, few-shot, formato XML/JSON, ancoragem, versionamento de prompt e o eval primer.",
    3: "RAG bem-feito: chunking, embeddings, BM25 híbrido, reranking, contextual retrieval (Anthropic 2024) e citações obrigatórias.",
    4: "Tool/function calling provider-neutral, agentes single (ReAct), padrões multi-agente e MCP.",
    5: "Memória curto/longo prazo, summarização hierárquica, prompt caching e context distillation.",
    6: "Golden sets, LLM-as-judge, tracing, prompt injection sandboxed, A/B em produção e rollback.",
}


def render_trilha(num: int) -> str:
    t = TRILHAS[num]
    cor = t["cor"]
    modulos_da_trilha = [m for m in MODULOS if m["trilha"] == num]
    ga = sum(1 for m in modulos_da_trilha if m["status"] == "GA")
    beta = sum(1 for m in modulos_da_trilha if m["status"] == "beta")
    total_min = sum(m["minutos"] for m in modulos_da_trilha)

    cards = []
    for idx, m in enumerate(modulos_da_trilha):
        # Mostra os 3 primeiros sub-tópicos como preview
        preview = m["topicos"][:3]
        topicos_html = []
        for i, tp in enumerate(preview, 1):
            topicos_html.append(f"""
        <details class="topico-expansivel border-b border-zinc-800 py-3 px-2 last:border-b-0">
          <summary class="cursor-pointer flex items-center gap-3 text-sm font-medium list-none">
            <span class="topico-numero w-6 h-6 rounded-full bg-{cor}-500/20 border border-{cor}-500/30 text-{cor}-400 text-xs font-bold flex items-center justify-center">{i}</span>
            <span>{tp["emoji"]} {tp["titulo"]}</span>
            <span class="text-zinc-500 text-xs ml-2 hidden md:inline">— {tp["subtitulo"]}</span>
          </summary>
          <div class="mt-3 ml-9 space-y-2 text-xs">
            <div><span class="text-{cor}-400 font-semibold">O que é:</span> <span class="text-zinc-300">{tp["o_que_e"]}</span></div>
            <div><span class="text-{cor}-400 font-semibold">Por que aprender:</span> <span class="text-zinc-300">{tp["por_que"]}</span></div>
            <div><span class="text-{cor}-400 font-semibold">Conceitos-chave:</span> <span class="text-zinc-300">{tp["conceitos"]}</span></div>
          </div>
        </details>""")

        more_topics = len(m["topicos"]) - 3
        more_text = f"<p class='text-xs text-zinc-500 px-2 py-2 italic'>+ {more_topics} sub-tópicos no módulo completo</p>" if more_topics > 0 else ""

        status_badge = (
            f'<span class="px-2 py-0.5 bg-{cor}-500/20 text-{cor}-400 rounded text-xs font-semibold">GA</span>'
            if m["status"] == "GA" else
            f'<span class="px-2 py-0.5 bg-amber-500/20 text-amber-400 rounded text-xs font-semibold">beta</span>'
        )

        cards.append(f"""
      <article class="modulo-card bg-zinc-900 rounded-xl border border-zinc-800 hover:border-{cor}-500/40 mb-6 transition-colors">
        <div class="p-6 border-b border-zinc-800">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <span class="text-{cor}-400 font-bold">{m['numero']}</span>
              {status_badge}
            </div>
            <span class="text-xs text-zinc-500">~{m['minutos']} min · {m['nivel']}</span>
          </div>
          <h3 class="text-2xl font-bold mb-2 text-zinc-100">{m['emoji']} {m['titulo']}</h3>
          <p class="text-sm text-zinc-400">{m['descricao']}</p>
        </div>

        <div class="px-3">
          {''.join(topicos_html)}
          {more_text}
        </div>

        <div class="p-4 bg-zinc-800/30 flex justify-start space-x-3">
          <a href="{m['id']}.html" class="btn px-4 py-2 text-sm bg-{cor}-600 text-white hover:bg-{cor}-500 rounded-lg transition-colors justify-start">
            Ver Completo →
          </a>
        </div>
      </article>
""")

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>T{num} — {t['nome']} · FEC</title>
  <link rel="stylesheet" href="../../assets/css/inema.css">
  <meta name="trilha" content="T{num}">
  <meta name="status" content="GA">
</head>
<body class="bg-zinc-950 text-zinc-100 font-sans antialiased min-h-screen" data-status="GA">

  <nav class="sticky top-0 z-50 bg-zinc-950/95 backdrop-blur border-b border-zinc-800">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <a href="../../index.html" class="flex items-center gap-3">
        <span class="text-2xl font-bold text-primary">FEC</span>
        <span class="text-zinc-400 text-sm hidden md:inline">Formação de Engenharia de Contexto</span>
      </a>
      <div class="flex items-center gap-4 text-sm">
        <a href="../../index.html" class="hover:text-primary transition">← Trilhas</a>
        <a href="https://github.com/inematds/FEC" class="hover:text-primary transition">GitHub</a>
        <a href="https://inema.club" target="_blank" class="text-sky-400 hover:text-sky-300 text-sm font-medium transition">INEMA.CLUB</a>
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

  <main class="max-w-4xl mx-auto px-6 py-12">

    <h2 class="text-2xl font-bold mb-6">📚 Módulos da trilha</h2>

    {''.join(cards)}

    <section class="mt-12 p-6 rounded-lg border border-zinc-700 bg-zinc-900/50">
      <h3 class="text-lg font-bold mb-2">🔬 Bibliografia da trilha</h3>
      <p class="text-sm text-zinc-400 mb-3">Referências datadas, congeladas na release. Lista completa em <code>bibliografia/T{num}.md</code>.</p>
      <a href="../../bibliografia/T{num}.md" class="btn px-4 py-2 border border-zinc-700 text-zinc-200 rounded hover:bg-zinc-800 transition justify-start">
        Bibliografia T{num} →
      </a>
    </section>

  </main>

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
