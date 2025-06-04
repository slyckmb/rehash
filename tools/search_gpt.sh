#!/usr/bin/env bash

# GPT CSV Extractor - Verbose Mode
# Usage: ./search_gpt.sh <keyword>

set -euo pipefail
shopt -s nullglob

DATA_DIR="./data"
REHASH_SCRIPT="release/v0.1.6/rehash.py"
OUT_DIR="./out"
KEYWORD="${1:-}"

if [[ -z "$KEYWORD" ]]; then
  echo "[!] Usage: ./search_gpt.sh <keyword>"
  exit 1
fi

LATEST_ZIP=$(ls -t "${DATA_DIR}"/*.zip | head -n 1)
[[ -z "${LATEST_ZIP}" ]] && echo "[!] No .zip exports found in ${DATA_DIR}" && exit 1

echo "[*] ZIP: $LATEST_ZIP"
echo "[*] Searching for keyword in titles: '$KEYWORD'"

# Create temp CSV
TMP_CSV=$(mktemp)
python "$REHASH_SCRIPT" "$LATEST_ZIP" -l csv --filter "items[?contains(title, '${KEYWORD}')]" > "$TMP_CSV"

# Check match count
MATCH_COUNT=$(($(wc -l < "$TMP_CSV") - 1))
if (( MATCH_COUNT <= 0 )); then
  echo "[!] No conversations matched."
  exit 0
fi

echo "[+] $MATCH_COUNT chat(s) matched keyword: $KEYWORD"
echo "[*] Extracting to: ${OUT_DIR}/"

tail -n +2 "$TMP_CSV" | while IFS=, read -r ID TITLE CREATED _; do
  ID=$(echo "$ID" | tr -d '"')
  TITLE=$(echo "$TITLE" | tr -d '"' | xargs)
  CREATED=$(echo "$CREATED" | cut -d'T' -f1 | tr -d '"')
  SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-')

  CHAT_DIR="${OUT_DIR}/${SLUG}-${CREATED}"
  mkdir -p "$CHAT_DIR"

  FNAME="chat_${SLUG}.json"
  OUT_PATH="${CHAT_DIR}/${FNAME}"
  INDEX=1
  while [[ -e "$OUT_PATH" ]]; do
    OUT_PATH="${CHAT_DIR}/chat_${SLUG}-${INDEX}.json"
    ((INDEX++))
  done

  echo "[→] Extracting: '$TITLE'"
  echo "    ID: $ID"
  echo "    Date: $CREATED"
  echo "    Path: $OUT_PATH"
  
  python "$REHASH_SCRIPT" "$LATEST_ZIP" -c "$ID" json > "$OUT_PATH"
done

echo "[✓] Extraction complete."
echo "[✓] Check ./out/ for results."
