#!/bin/bash
set -euo pipefail

### 🔰 Guardrails Rehydrator v2.2.3
### 📦 Phase: dev/0.2.x isolated
### 🕐 Generated: $(date -Iseconds)
### 🌍 Must be run inside: ~/dev/work/rehash/

REPO_NAME="rehash"
SOURCE_DIR="."
REMOTE="origin"
GH_REPO="$REPO_NAME"

# ─────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────
# 🌱 Create dev/0.2.x branch
git checkout -b dev/0.2.x || git checkout dev/0.2.x

WAVE_01=(
  "rehash.v0.2.3-dev.py"
  "rehash.v0.2.4-dev.py"
  "rehash.v0.2.4-dev+fx1.py"
  "rehash.v0.2.4-dev+fx2.py"
  "rehash.v0.2.4-dev+fx3.py"
  "rehash.v0.2.5-dev.py"
  "rehash.v0.2.5-dev+fx1.py"
  "rehash.v0.2.5-dev+fx2.py"
  "rehash.v0.2.5-dev+fx3.py"
  "rehash.v0.2.5-dev+fx4.py"
  "rehash.v0.2.5-dev+fx5.py"
  "rehash.v0.2.5-dev+fx6.py"
)

WAVE_02=(
  "rehash_requirements.v0.2.0.md"
  "rehash_requirements.v0.2.1.md"
  "rehash_requirements.v0.2.2-dev.md"
  "rehash_requirements.v0.2.3-dev.md"
  "rehash_requirements.v0.2.4-dev.md"
  "rehash_requirements.v0.2.5-dev.md"
  "rehash_requirements.v0.2.5-dev+fx1.md"
  "rehash_requirements.v0.2.5-dev+fx2.md"
  "rehash_REHYDRATION.v0.2.5.md"
)

# Create target folder
mkdir -p dev/v0.2.x release/v0.2.6

# ─────────── WAVE 1 ───────────
for file in "${WAVE_01[@]}"; do
  cp "$SOURCE_DIR/$file" dev/v0.2.x/
done
git add .
git commit -m "feat(wave1): core rehash engine v0.2 builds"

# ─────────── WAVE 2 ───────────
for file in "${WAVE_02[@]}"; do
  cp "$SOURCE_DIR/$file" dev/v0.2.x/
done
git add .
git commit -m "feat(wave2): requirements + fx REHYDRATION"

git tag v0.2.6-REV1

# # ─────────────────────────────────────────────────────────────
# # 📦 Build release snapshot
# cp dev/v0.2.x/rehash.v0.2.5-dev+fx6.py release/v0.2.6/rehash.py
# cp dev/v0.2.x/rehash_requirements.v0.2.5-dev+fx2.md release/v0.2.6/REQUIREMENTS.md
# echo "- Release v0.2.6 FX6" > release/v0.2.6/changelog.md
# git add release/
# git commit -m "release(v0.2.6): snapshot release folder"

# # ─────────────────────────────────────────────────────────────
# # 🔀 Merge to main (squash)
# git checkout main
# git merge --squash --allow-unrelated-histories dev/0.2.x
# git commit -m "release: squash dev/0.2.x → main as v0.2.6-final"

# # 🧾 Publish to root
# cp release/v0.2.6/rehash.py .
# cp release/v0.2.6/REQUIREMENTS.md .
# git add rehash.py REQUIREMENTS.md
# git commit -m "release(v0.2.6): publish root files"
# git tag v0.2.6-final

# # ─────────────────────────────────────────────────────────────
# # ☁️ Push to GitHub
# echo "🚀 Using existing GitHub remote: $REMOTE"
# git push "$REMOTE" main
# git push "$REMOTE" dev/0.2.x
# git push "$REMOTE" --tags

# echo "✅ DONE: https://github.com/YOUR_USERNAME/$GH_REPO"
