#!/bin/bash
set -euo pipefail

### 🔰 Guardrails Rehydrator v2.2.3
### 📦 Phase: dev/0.1.x only
### 🕐 Generated: 2025-05-10T12:45:00-04:00
### 🌍 Assumes you are inside ~/dev/work/rehash/

REPO_NAME="rehash"
SOURCE_DIR="."         # 👈 Must match unzip target
REMOTE="origin"
GH_REPO="$REPO_NAME"

echo "🧭 Working Dir: $(pwd)"
echo "📦 Expecting: $SOURCE_DIR/rehash.v0.1.0.py"

# 🔒 Safety: Make sure no `.git` folder inside another `.git`
if [ -d "$SOURCE_DIR/.git" ]; then
  echo "⚠️  Found .git — reusing repo."
else
  echo "🛠️ Initializing repo..."
  git init -b main
  git commit --allow-empty -m "chore: initial base commit for squash logic"
fi

# 🪄 Create or switch dev branch
git checkout -B dev/0.1.x

# ───── Files for Wave 1 (builds) ─────
WAVE_01=(
  "rehash.v0.1.0.py"
  "rehash.v0.1.1-BUILD1.py"
  "rehash.v0.1.2-BUILD2.py"
  "rehash.v0.1.3-BUILD3.py"
  "rehash.v0.1.4-BUILD4.py"
  "rehash.v0.1.5-BUILD5.py"
)

# ───── Files for Wave 2 (requirements/docs) ─────
WAVE_02=(
  "rehash_requirements.v0.1.4-REV1.md"
  "rehash_requirements.v0.1.6-REV2.md"
  "REHYDRATION.md"
)

# Folder structure
mkdir -p dev/v0.1.x release/v0.1.6

# ➤ WAVE 1: Copy and commit engine builds
for f in "${WAVE_01[@]}"; do cp "$SOURCE_DIR/$f" dev/v0.1.x/; done
git add dev/v0.1.x/
git commit -m "feat(wave1): core rehash engine v0.1 builds"

# ➤ WAVE 2: Requirements + docs
for f in "${WAVE_02[@]}"; do cp "$SOURCE_DIR/$f" dev/v0.1.x/; done
git add dev/v0.1.x/
git commit -m "feat(wave2): requirements + rehydration baseline"

# Tag dev tip
git tag v0.1.6-REV2

# ➤ Build release snapshot
cp dev/v0.1.x/rehash.v0.1.5-BUILD5.py release/v0.1.6/rehash.py
cp dev/v0.1.x/rehash_requirements.v0.1.6-REV2.md release/v0.1.6/REQUIREMENTS.md
echo "- Release v0.1.6 BUILD5" > release/v0.1.6/changelog.md
git add release/
git commit -m "release(v0.1.6): snapshot release folder"

# ➤ Merge to main via squash
git checkout main
git merge --squash --allow-unrelated-histories dev/0.1.x
git commit -m "release: squash dev/0.1.x → main as v0.1.6-final"

# ➤ Publish root files
cp release/v0.1.6/rehash.py .
cp release/v0.1.6/REQUIREMENTS.md .
git add rehash.py REQUIREMENTS.md
git commit -m "release(v0.1.6): publish root files"
git tag v0.1.6-final

# ➤ Push to GitHub
echo "🚀 Creating GitHub repo: $GH_REPO"
gh repo create "$GH_REPO" --public --source=. --remote="$REMOTE" --push
git push "$REMOTE" main
git push "$REMOTE" dev/0.1.x
git push "$REMOTE" --tags

echo "✅ DONE: https://github.com/YOUR_USERNAME/$GH_REPO"
