#!/bin/bash
set -euo pipefail

### 🔰 Guardrails Rehydrator v2.2.4
### 📦 Phase: dev/0.2.x isolated
### 🧼 Fix: NO git add . — only targeted files

REPO_NAME="rehash"
SOURCE_DIR="."
REMOTE="origin"
GH_REPO="$REPO_NAME"

echo "🧭 Working Dir: $(pwd)"
echo "📦 Expecting: $SOURCE_DIR/rehash.v0.2.3-dev.py"
ls "$SOURCE_DIR/rehash.v0.2.3-dev.py" || { echo "❌ Missing file: rehash.v0.2.3-dev.py"; exit 1; }

if [ ! -d ".git" ]; then
  echo "🛠️ Initializing fresh Git repo..."
  git init -b main
  git commit --allow-empty -m "chore: init base commit for squash logic"
else
  echo "✅ Git repo already initialized"
fi

# ─────────────── 🌱 Create dev/0.2.x branch ───────────────
git checkout -b dev/0.2.x || git checkout dev/0.2.x
mkdir -p dev/v0.2.x release/v0.2.6

# ─────────── WAVE 1 ───────────
WAVE_01=(
  rehash.v0.2.3-dev.py
  rehash.v0.2.4-dev.py
  rehash.v0.2.4-dev+fx1.py
  rehash.v0.2.4-dev+fx2.py
  rehash.v0.2.4-dev+fx3.py
  rehash.v0.2.5-dev.py
  rehash.v0.2.5-dev+fx1.py
  rehash.v0.2.5-dev+fx2.py
  rehash.v0.2.5-dev+fx3.py
  rehash.v0.2.5-dev+fx4.py
  rehash.v0.2.5-dev+fx5.py
  rehash.v0.2.5-dev+fx6.py
)

for file in "${WAVE_01[@]}"; do
  cp "$SOURCE_DIR/$file" "dev/v0.2.x/"
  git add "dev/v0.2.x/$file"
done
git commit -m "feat(wave1): core rehash engine v0.2 builds"

# ─────────── WAVE 2 ───────────
WAVE_02=(
  rehash_requirements.v0.2.0.md
  rehash_requirements.v0.2.1.md
  rehash_requirements.v0.2.2-dev.md
  rehash_requirements.v0.2.3-dev.md
  rehash_requirements.v0.2.4-dev.md
  rehash_requirements.v0.2.5-dev.md
  rehash_requirements.v0.2.5-dev+fx1.md
  rehash_requirements.v0.2.5-dev+fx2.md
  rehash_REHYDRATION.v0.2.5.md
)

for file in "${WAVE_02[@]}"; do
  cp "$SOURCE_DIR/$file" "dev/v0.2.x/"
  git add "dev/v0.2.x/$file"
done
git commit -m "feat(wave2): requirements + fx REHYDRATION"

# 🔖 Tag
git tag v0.2.6-REV1
echo "✅ Phase 2 complete. Tag created: v0.2.6-REV1"
