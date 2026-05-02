#!/usr/bin/env bash
# render-diagrams.sh — pré-renderiza Mermaid (.mmd) em SVG dual (dark + light).
# PLAN item 30. Cada diagrama vira <id>.dark.svg e <id>.light.svg.

set -euo pipefail

SRC_DIR="assets/diagrams/src"
OUT_DIR="assets/diagrams"

if [ ! -d "$SRC_DIR" ]; then
  echo "$SRC_DIR não existe; nada a renderizar."
  exit 0
fi

# Verifica mermaid CLI
if ! command -v mmdc >/dev/null 2>&1; then
  if ! command -v npx >/dev/null 2>&1; then
    echo "ERRO: mmdc nem npx encontrados. Instale: npm install" >&2
    exit 1
  fi
  MMDC="npx -y -p @mermaid-js/mermaid-cli mmdc"
else
  MMDC="mmdc"
fi

mkdir -p "$OUT_DIR"

count=0
for src in "$SRC_DIR"/*.mmd; do
  [ -e "$src" ] || continue
  base=$(basename "$src" .mmd)

  # Dark theme
  $MMDC -i "$src" -o "$OUT_DIR/${base}.dark.svg" -t dark -b transparent --quiet
  # Light theme — força background branco para legibilidade
  $MMDC -i "$src" -o "$OUT_DIR/${base}.light.svg" -t default -b white --quiet

  echo "rendered $base (dark + light)"
  count=$((count + 1))
done

echo "OK — $count diagram(s) rendered."
