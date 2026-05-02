# CHANGELOG do harness FEC-EVAL

> _Formato: SemVer aplicado ao harness. Mudança em judge ou dataset gera novo sufixo (`-v2`); runs antigos com `-v1` continuam reproduzíveis. PLAN item 28._

## v1 (2026-05-02)

**Estado:** ativo, congelado para release v1.0.0.

### Datasets pinados
- `FEC-GS-RAG-v1` — 30 perguntas para P1.
- `FEC-GS-AGENT-v1` — 30 traços-canário para P2 (a popular).
- `FEC-GS-INJECTION-v1` — 20 payloads sandbox para P5 (a popular).

### Judges pinados
- `evals/v1/judges/groundedness.md` — para P1, módulos T3.
- `evals/v1/judges/agent-correctness.md` — para P2 (a criar).
- `evals/v1/judges/injection-defense.md` — para P5 (a criar).

### Modelos pinados (smoke)
- frontier: `claude-sonnet-4-6@2026-04`
- low-cost: `gpt-5-mini@2026-04`
- oss: `qwen2.5-7b-instruct@q4_K_M`

### Política

- Mudança em qualquer arquivo coberto por `HASHES.lock` exige bump da versão (v1 → v2) OU é proibida.
- Runs antigos referenciam versão exata (`evals/v1/`) e continuam reproduzíveis indefinidamente.
- Datasets podem CRESCER (adicionar exemplos) sem virar v2 SE o crescimento não quebra runs antigos. Caso contrário, novo sufixo (ex.: `FEC-GS-RAG-v1.1`).

## (planejado) v2

Disparo: mudança em metodologia do judge OU mudança breaking em dataset.

Prazo esperado: pós v2.0 do curso, ou se descoberta científica relevante exigir.
