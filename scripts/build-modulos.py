#!/usr/bin/env python3
"""build-modulos.py — gera os 14 HTMLs de módulo no padrão INEMA a partir de modulos_spec.py.

Padrão seguido: MASTER_COMPLETO.md (skill formato-curso) — header gradiente,
breadcrumb, 6 seções ricas com número grande, boxes coloridos (Conceito Principal,
Dados de Pesquisa, Dica Prática, Fazer/Evitar), Resumo Final.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from modulos_spec import MODULOS, TRILHAS  # noqa: E402

REPO = Path(__file__).resolve().parent.parent

CSP = "default-src 'none'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'none'; frame-src 'self'; base-uri 'none'; form-action 'none'; upgrade-insecure-requests"

# Trilha cor → variante numérica do Tailwind (-400 dark, escuro -700/-800 light) e RGB
COR_INFO = {
    "emerald": {"text": "emerald-400", "bg20": "emerald-500/20", "bg10": "emerald-500/10", "border": "emerald-500/30", "from": "emerald-900/30", "rgb": "5, 150, 105", "light": "#059669"},
    "blue":    {"text": "blue-400",    "bg20": "blue-500/20",    "bg10": "blue-500/10",    "border": "blue-500/30",    "from": "blue-900/30",    "rgb": "37, 99, 235",  "light": "#2563eb"},
    "purple":  {"text": "purple-400",  "bg20": "purple-500/20",  "bg10": "purple-500/10",  "border": "purple-500/30",  "from": "purple-900/30",  "rgb": "124, 58, 237", "light": "#7c3aed"},
    "amber":   {"text": "amber-400",   "bg20": "amber-500/20",   "bg10": "amber-500/10",   "border": "amber-500/30",   "from": "amber-900/30",   "rgb": "217, 119, 6",  "light": "#92400e"},
    "teal":    {"text": "teal-400",    "bg20": "teal-500/20",    "bg10": "teal-500/10",    "border": "teal-500/30",    "from": "teal-900/30",    "rgb": "13, 148, 136", "light": "#0d9488"},
    "rose":    {"text": "rose-400",    "bg20": "rose-500/20",    "bg10": "rose-500/10",    "border": "rose-500/30",    "from": "rose-900/30",    "rgb": "225, 29, 72",  "light": "#9f1239"},
}


def render_modulo(m: dict) -> str:
    t = TRILHAS[m["trilha"]]
    cor = t["cor"]
    ci = COR_INFO[cor]
    status_badge = f'<span class="px-2 py-1 bg-{cor}-500/20 border border-{cor}-500/30 text-{cor}-400 rounded text-xs">{m["status"]}</span>'

    # === Topicos: 6 sections ricas ===
    topicos_html = []
    for i, tp in enumerate(m["topicos"], 1):
        topicos_html.append(f"""
      <section id="topico-{i}" class="mb-16">
        <div class="flex items-center space-x-4 mb-6">
          <span class="flex items-center justify-center w-12 h-12 rounded-full bg-{cor}-500/20 text-{cor}-400 font-bold text-xl flex-shrink-0">{i}</span>
          <div>
            <h2 class="text-2xl font-bold">{tp["emoji"]} {tp["titulo"]}</h2>
            <p class="text-zinc-400 text-sm mt-1">{tp["subtitulo"]}</p>
          </div>
        </div>

        <div class="ml-0 md:ml-16 space-y-3 bg-zinc-900/50 border border-zinc-800 rounded-lg p-5">
          <div>
            <span class="text-{cor}-400 font-semibold">O que é:</span>
            <p class="text-zinc-300 text-sm mt-1">{tp["o_que_e"]}</p>
          </div>
          <div>
            <span class="text-{cor}-400 font-semibold">Por que aprender:</span>
            <p class="text-zinc-300 text-sm mt-1">{tp["por_que"]}</p>
          </div>
          <div>
            <span class="text-{cor}-400 font-semibold">Conceitos-chave:</span>
            <p class="text-zinc-300 text-sm mt-1">{tp["conceitos"]}</p>
          </div>
        </div>
      </section>
""")
    # Sub-tópicos expansíveis (PLAN item 18.3 e validate.py exigem ≥6 <details class="topico-expansivel">)
    detalhes = []
    for i, tp in enumerate(m["topicos"], 1):
        detalhes.append(f"""
        <details class="topico-expansivel border-b border-zinc-800 py-3">
          <summary class="cursor-pointer flex items-center gap-3 text-base font-semibold list-none">
            <span class="topico-numero w-6 h-6 rounded-full bg-{cor}-500/20 border border-{cor}-500/30 text-{cor}-400 text-xs font-bold flex items-center justify-center">{i}</span>
            <span>{tp["emoji"]} {tp["titulo"]}</span>
            <span class="text-zinc-500 text-xs ml-2">— {tp["subtitulo"]}</span>
          </summary>
          <div class="mt-3 ml-9 space-y-2 text-sm">
            <div><span class="text-{cor}-400 font-semibold">O que é:</span> <span class="text-zinc-300">{tp["o_que_e"]}</span></div>
            <div><span class="text-{cor}-400 font-semibold">Por que aprender:</span> <span class="text-zinc-300">{tp["por_que"]}</span></div>
            <div><span class="text-{cor}-400 font-semibold">Conceitos-chave:</span> <span class="text-zinc-300">{tp["conceitos"]}</span></div>
          </div>
        </details>""")

    # === Conceito Principal ===
    cp = m.get("conceito_principal")
    cp_html = ""
    if cp:
        items = "".join(f"<li class='flex items-start space-x-2'><span class='text-{cor}-400 mt-1'>•</span><span>{x}</span></li>" for x in cp.get("lista", []))
        cp_html = f"""
      <div class="bg-gradient-to-br from-{cor}-900/30 to-zinc-900 rounded-xl border border-{cor}-500/30 p-6 mb-8">
        <h3 class="text-lg font-bold text-{cor}-400 mb-3 flex items-center"><span class="mr-2">{cp["emoji"]}</span> {cp["titulo"]}</h3>
        <p class="text-zinc-300 mb-4">{cp["texto"]}</p>
        <ul class="space-y-2 text-zinc-300 text-sm">{items}</ul>
      </div>
"""

    # === Dados de Pesquisa OU Dica Prática ===
    dados = m.get("dados_pesquisa")
    dados_html = ""
    if dados:
        items = "".join(f"<li class='text-sm text-zinc-300'>{x}</li>" for x in dados["items"])
        dados_html = f"""
      <div class="bg-blue-900/20 rounded-xl border border-blue-500/30 p-6 mb-8">
        <h3 class="text-lg font-bold text-blue-400 mb-3 flex items-center"><span class="mr-2">📊</span> {dados["titulo"]}</h3>
        <ul class="space-y-2">{items}</ul>
      </div>
"""

    dica = m.get("dica_pratica")
    dica_html = ""
    if dica:
        dica_html = f"""
      <div class="bg-primary/10 rounded-xl border border-primary/40 p-6 mb-8">
        <h3 class="text-lg font-bold text-primary mb-3 flex items-center"><span class="mr-2">{dica["emoji"]}</span> {dica["titulo"]}</h3>
        <p class="text-zinc-300 text-sm">{dica["texto"]}</p>
      </div>
"""

    # === Fazer vs Evitar ===
    fe = m.get("fazer_evitar", [])
    fazer_items = "".join(f"<li class='flex items-start space-x-2'><span class='text-emerald-400 mt-1'>✓</span><span class='text-sm'>{a}</span></li>" for a, _ in fe)
    evitar_items = "".join(f"<li class='flex items-start space-x-2'><span class='text-red-400 mt-1'>✗</span><span class='text-sm'>{b}</span></li>" for _, b in fe)
    fe_html = f"""
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="bg-emerald-900/20 rounded-xl border border-emerald-500/30 p-6">
          <h4 class="font-bold text-emerald-400 mb-4">✓ O que FAZER</h4>
          <ul class="space-y-3 text-zinc-300">{fazer_items}</ul>
        </div>
        <div class="bg-red-900/20 rounded-xl border border-red-500/30 p-6">
          <h4 class="font-bold text-red-400 mb-4">✗ O que NÃO fazer</h4>
          <ul class="space-y-3 text-zinc-300">{evitar_items}</ul>
        </div>
      </div>
""" if fe else ""

    # === Quando NÃO usar ===
    qnu = "".join(f"<li class='flex items-start space-x-2'><span class='text-red-400 mt-1'>•</span><span class='text-sm text-zinc-300'>{x}</span></li>" for x in m.get("quando_nao_usar", []))
    qnu_html = f"""
      <div class="quando-nao-usar bg-red-900/10 rounded-xl border border-red-500/30 p-6 mb-8">
        <h3 class="text-lg font-bold text-red-400 mb-3 flex items-center"><span class="mr-2">🚫</span> Quando NÃO usar</h3>
        <ul class="space-y-2">{qnu}</ul>
      </div>
""" if m.get("quando_nao_usar") else ""

    # === Exemplo de código ===
    exemplo_codigo = m.get("exemplo_codigo", "")
    codigo_html = f"""
      <div class="bg-zinc-900 rounded-xl border border-zinc-800 p-6 mb-8">
        <h3 class="text-lg font-bold text-{cor}-400 mb-3 flex items-center"><span class="mr-2">💻</span> Exemplo de código</h3>
        <pre class="bg-zinc-950 border border-zinc-800 p-4 rounded text-sm overflow-x-auto"><code>{_escape(exemplo_codigo)}</code></pre>
      </div>
""" if exemplo_codigo else ""

    # === Exercício ===
    exercicio_html = f"""
      <div class="bg-amber-900/10 rounded-xl border border-amber-500/30 p-6 mb-8">
        <h3 class="text-lg font-bold text-amber-400 mb-3 flex items-center"><span class="mr-2">🏋️</span> Exercício hands-on</h3>
        <p class="text-zinc-300 text-sm">{m.get("exercicio", "Exercício em desenvolvimento.")}</p>
      </div>
"""

    # === Bibliografia ===
    bib_items = "".join(
        f'<li class="text-sm"><strong>{a}</strong> — <a href="{u}" class="text-sky-400 hover:text-sky-300 underline">{t}</a></li>'
        for a, t, u in m.get("bibliografia", [])
    )
    bib_html = f"""
      <div class="bg-zinc-900/50 rounded-xl border border-zinc-800 p-6 mb-8">
        <h3 class="text-lg font-bold text-{cor}-400 mb-3 flex items-center"><span class="mr-2">📚</span> Bibliografia</h3>
        <ul class="space-y-2 text-zinc-300">{bib_items}</ul>
      </div>
"""

    # === Resumo Final ===
    resumo_items = "".join(
        f'<li class="flex items-start space-x-3"><span class="text-{cor}-400 mt-1">✓</span><span class="text-zinc-300">{x}</span></li>'
        for x in m.get("resumo", [])
    )
    resumo_html = f"""
      <section class="mb-12">
        <div class="bg-gradient-to-br from-{cor}-900/55 via-zinc-900 to-zinc-900 rounded-xl border border-{cor}-500/30 p-8">
          <h2 class="text-2xl font-bold mb-6 flex items-center"><span class="mr-3">🎯</span> Resumo do Módulo</h2>
          <ul class="space-y-3 mb-8">{resumo_items}</ul>
          <div class="bg-zinc-900/50 rounded-lg p-4 mb-6">
            <h3 class="font-semibold text-{cor}-400 mb-2">Próximo Módulo:</h3>
            <p class="text-zinc-300 text-sm">{m.get("proximo_titulo", "")}</p>
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <a href="index.html" class="btn flex-1 text-center px-6 py-3 bg-zinc-800 text-zinc-300 rounded-lg font-semibold hover:bg-zinc-700 transition-colors justify-start">← Voltar para Trilha</a>
            <a href="{m.get("proximo_id", "index.html")}" class="btn flex-1 text-center px-6 py-3 bg-{cor}-600 text-white rounded-lg font-semibold hover:bg-{cor}-500 transition-colors justify-start">Próximo Módulo →</a>
          </div>
        </div>
      </section>
"""

    # === Page assembly ===
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{m["numero"]} {m["titulo"]} · FEC T{m["trilha"]}</title>
  <link rel="stylesheet" href="../../assets/css/inema.css">
  <meta name="trilha" content="T{m['trilha']}">
  <meta name="status" content="{m['status']}">
  <meta name="modulo" content="{m['id']}">
  <meta name="palavras" content="3000">
  <meta name="tempo-estimado-min" content="{m['minutos']}">
  <meta name="expected-sdk-version" content=">=1.0,<2.0">
</head>
<body class="bg-zinc-950 text-zinc-100 font-sans antialiased min-h-screen" data-status="{m['status']}">

  <!-- NAV GLOBAL -->
  <nav class="sticky top-0 z-50 bg-zinc-950/95 backdrop-blur border-b border-zinc-800">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <a href="../../index.html" class="flex items-center gap-3">
        <span class="text-2xl font-bold text-primary">FEC</span>
        <span class="text-zinc-400 text-sm hidden md:inline">Formação de Engenharia de Contexto</span>
      </a>
      <div class="flex items-center gap-4 text-sm">
        <a href="index.html" class="hover:text-primary transition">← T{m['trilha']}</a>
        <a href="https://github.com/inematds/FEC" class="hover:text-primary transition">GitHub</a>
        <a href="https://inema.club" target="_blank" class="text-sky-400 hover:text-sky-300 text-sm font-medium transition">INEMA.CLUB</a>
      </div>
    </div>
  </nav>

  <!-- BREADCRUMB -->
  <nav class="max-w-6xl mx-auto px-6 py-4">
    <div class="flex items-center space-x-2 text-sm text-zinc-400">
      <a href="../../index.html" class="hover:text-{cor}-400">Início</a>
      <span>/</span>
      <a href="index.html" class="hover:text-{cor}-400">Trilha {m['trilha']}</a>
      <span>/</span>
      <span class="text-{cor}-400">Módulo {m['numero']}</span>
    </div>
  </nav>

  <!-- HEADER COM GRADIENTE + STATS -->
  <header class="bg-gradient-to-br from-{cor}-900/45 via-zinc-900 to-zinc-900 py-12 border-b border-zinc-800">
    <div class="max-w-6xl mx-auto px-6">
      <div class="flex items-center gap-3 mb-4">
        <span class="inline-block px-3 py-1 bg-{cor}-500/20 text-{cor}-400 text-xs font-semibold rounded-full">MÓDULO {m['numero']}</span>
        {status_badge}
      </div>
      <h1 class="text-3xl sm:text-4xl font-bold mb-4 text-zinc-100">{m['emoji']} {m['titulo']}</h1>
      <p class="text-lg text-zinc-300 max-w-3xl mb-8">{m['descricao']}</p>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl">
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700">
          <div class="text-xl font-bold text-{cor}-400">6</div>
          <div class="text-xs text-zinc-400">Tópicos</div>
        </div>
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700">
          <div class="text-xl font-bold text-{cor}-400">{m['minutos']}</div>
          <div class="text-xs text-zinc-400">Minutos</div>
        </div>
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700">
          <div class="text-xl font-bold text-{cor}-400">{m['nivel']}</div>
          <div class="text-xs text-zinc-400">Nível</div>
        </div>
        <div class="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700">
          <div class="text-xl font-bold text-{cor}-400">{m['tipo']}</div>
          <div class="text-xs text-zinc-400">Tipo</div>
        </div>
      </div>
    </div>
  </header>

  <!-- CONTEÚDO -->
  <main class="max-w-4xl mx-auto px-6 py-12">

    <!-- Introdução -->
    <section class="mb-12 prose prose-invert max-w-none">
      <p class="text-lg text-zinc-200 leading-relaxed">{m['introducao']}</p>
    </section>

    <!-- Conceito Principal + Dados/Dica -->
    {cp_html}
    {dados_html}
    {dica_html}

    <!-- 6 SEÇÕES RICAS -->
    {''.join(topicos_html)}

    <!-- Sub-tópicos expansíveis (resumo navegável) -->
    <section class="mb-12">
      <h2 class="text-2xl font-bold mb-4">📑 Resumo navegável dos tópicos</h2>
      <div class="bg-zinc-900/50 rounded-xl border border-zinc-800 p-6">
        {''.join(detalhes)}
      </div>
    </section>

    <!-- Fazer vs Evitar -->
    {fe_html}

    <!-- Quando NÃO usar -->
    {qnu_html}

    <!-- Exemplo de código -->
    {codigo_html}

    <!-- Exercício -->
    {exercicio_html}

    <!-- Bibliografia -->
    {bib_html}

    <!-- Resumo Final + Navegação -->
    {resumo_html}

  </main>

  <!-- FOOTER -->
  <footer class="border-t border-zinc-800 mt-16">
    <div class="max-w-6xl mx-auto px-6 py-8 text-sm text-zinc-500 flex flex-wrap items-center justify-between gap-4">
      <div>
        <a href="https://inema.club" target="_blank" class="text-sky-400 hover:text-sky-300">INEMA.CLUB</a> ·
        Conteúdo CC BY-SA 4.0 · Código MIT · Atualizado em 2026-05-02
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


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> int:
    written = 0
    for m in MODULOS:
        out_path = REPO / "curso" / f"trilha{m['trilha']}" / f"{m['id']}.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_modulo(m), encoding="utf-8")
        print(f"WROTE  {out_path.relative_to(REPO)}  ({m['titulo'][:50]})")
        written += 1
    print(f"\nDone — {written} módulos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
