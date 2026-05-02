#!/usr/bin/env python3
"""build-quiz.py — renderiza quizzes/<modulo>.json em HTML escapado seguro.

PLAN item 34a: NUNCA usar innerHTML; sempre textContent / template escaping.
Saída: snippets HTML em quizzes/<modulo>.snippet.html para incluir nos módulos.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
QUIZ_DIR = REPO / "quizzes"


def render(quiz: dict) -> str:
    """Quiz HTML — inputs escapados, sem inline scripts. JS de checagem fica em assets/js/quiz.js (CSP-safe)."""
    e = html.escape  # alias
    qid = e(quiz["module_id"])
    parts = [f'<form class="fec-quiz" data-module="{qid}" data-questions="{len(quiz["questions"])}">']
    parts.append(f'<h3 class="text-2xl font-bold mb-4 text-primary">Quiz — {e(quiz.get("title", qid))}</h3>')

    for q in quiz["questions"]:
        qno = e(q["id"])
        parts.append(f'<fieldset class="my-6 border-l-4 border-zinc-700 pl-4" data-q="{qno}">')
        parts.append(f'<legend class="font-semibold mb-2">{e(q["question"])}</legend>')
        parts.append('<div class="space-y-2">')
        input_type = "checkbox" if q["type"] == "multiple" else "radio"
        for opt in q["options"]:
            oid = f'{qid}-{qno}-{e(opt["id"])}'
            parts.append(
                f'<label class="block cursor-pointer">'
                f'<input type="{input_type}" name="{qid}-{qno}" value="{e(opt["id"])}" id="{oid}" class="mr-2">'
                f'<span>{e(opt["text"])}</span></label>'
            )
        parts.append("</div>")
        parts.append(
            f'<div class="hidden text-sm text-zinc-500 mt-2 fec-quiz-rationale" '
            f'data-correct="{e(json.dumps(q["correct"]))}">{e(q["rationale"])}</div>'
        )
        parts.append("</fieldset>")

    parts.append('<button type="submit" class="btn btn-primary">Verificar</button>')
    parts.append('<output class="block mt-4 fec-quiz-output text-sm"></output>')
    parts.append("</form>")
    return "\n".join(parts)


def main() -> int:
    if not QUIZ_DIR.exists():
        print("quizzes/ não existe — skip.")
        return 0
    found = 0
    for jf in sorted(QUIZ_DIR.glob("*.json")):
        data = json.loads(jf.read_text(encoding="utf-8"))
        out = jf.with_suffix(".snippet.html")
        out.write_text(render(data), encoding="utf-8")
        print(f"WROTE {out.relative_to(REPO)}")
        found += 1
    if found == 0:
        print("Nenhum quiz JSON ainda.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
