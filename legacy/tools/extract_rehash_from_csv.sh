#!/bin/bash

# ──────────────────────────────────────────────────────────────
# Extract & rename GPT conversations from CSV using rehash.py
# Usage: ./extract_rehash_from_csv.sh --csv file.csv --data data.zip [--out ./convos] [--filter substring]
# ──────────────────────────────────────────────────────────────

set -euo pipefail

# Defaults
OUTDIR="./convos"
FILTER=""

# ─── Parse CLI Args ────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --csv)
      CSV="$2"
      shift 2
      ;;
    --data)
      DATAPATH="$2"
      shift 2
      ;;
    --out)
      OUTDIR="$2"
      shift 2
      ;;
    --filter)
      FILTER="$2"
      shift 2
      ;;
    *)
      echo "[!] Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "${CSV:-}" ]] || [[ -z "${DATAPATH:-}" ]]; then
  echo "[!] Usage: --csv <file.csv> --data <zip|dir> [--out ./convos] [--filter substring]"
  exit 1
fi

mkdir -p "$OUTDIR"

# ─── Main Loop ────────────────────────────────────────────────
awk -F, -v IGNORECASE=1 -v filter="$FILTER" '
  filter == "" || tolower($2) ~ tolower(filter) { print $1","$2 }
' "$CSV" | while IFS=',' read -r id title; do
  shortid="${id:0:8}"
  slug=$(echo "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//;s/-$//')
  outfile="conv_${slug}_${shortid}.json"

  echo "[*] Extracting $id → $outfile"
  python release/v0.1.6/rehash.py "$DATAPATH" -c "$id" json

  if [[ -f "conversation_${id}.json" ]]; then
    mv "conversation_${id}.json" "${OUTDIR}/${outfile}"
    echo "[✓] Moved to ${OUTDIR}/${outfile}"
  else
    echo "[!] Export failed or missing for ID: $id"
  fi
done

echo "[🔁] Splitting conversations into day-grouped files..."
for f in "${OUTDIR}"/conv_*.json; do
  python split_conversations_by_day.py --file "$f" --out out/
done
echo "[✓] All conversations split by day into: ./out/"
