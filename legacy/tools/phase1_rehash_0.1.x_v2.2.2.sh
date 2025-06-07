#!/bin/bash
set -euo pipefail

### 🔰 Guardrails Rehydrator v2.2.2
### 📦 Phase: dev/0.1.x only (no 0.2.x contamination)
### 🕐 Generated: $(date -Iseconds)
### 🌍 Assumes you are inside ~/dev/work/rehash/

REPO_NAME="rehash"
SOURCE_DIR="."        # 🧠 Stay flat — no nesting
REMOTE="origin"
GH_REPO="$REPO_NAME"

# ─────────────────────────────────────────────────────────────
# 🔒 Preflight check for missing files
REQUIRED=(
  "rehash.v0.1.0.py"
  "rehash_requirements.v0.1.6-REV2.md"
)
for file in "${REQUIRED[@]}"; do
  if [ ! -f "$SOURCE_DIR/$file" ]; then
    echo "❌ Missing: $SOURCE_DIR/$file"
    echo "🛑 Press ENTER to exit safely..."
    read -r
    exit 1
  fi
done

# ─────────────────────────────────────────────────────────────
# 🧠 Git init check
if [ -d ".git" ]; then
  echo "✅ Git repo already initialized in $(pwd)"
else
  echo "🧱 Initializing fresh Git repo..."
  git init -b main
  git commit --allow-empty -m "chore: initial base commit for squash logic"
fi

# ─────────────────────────────────────────────────────────────
# 🌱 Create dev/0.1.x branch
git checkout -b dev/0.1.x || git checkout dev/0.1.x

WAVE_01=(
  "rehash.v0.1.0.py" "rehash.v0.1.1-BUILD1.py" "rehash.v0.1.2-BUILD2.py"
  "rehash.v0.1.3-BUILD3.py" "rehash.v0.1.4-BUILD4.py" "rehash.v0.1.5-BUILD5.py"
)
WAVE_02=(
  "rehash_requirements.v0.1.4-REV1.md"
  "rehash_requirements.v0.1.6-REV2.md"
  "REHYDRATION.md"
)

# 📁 Create working folders
mkdir -p dev/v0.1.x release/v0.1.6

# ─────────── WAVE 1 ───────────
for file in "${WAVE_01[@]}"; do
  cp "$SOURCE_DIR/$file" dev/v0.1.x/
done
git add .
git commit -m "feat(wave1): core rehash engine v0.1 builds"

# ─────────── WAVE 2 ───────────
for file in "${WAVE_02[@]}"; do
  cp "$SOURCE_DIR/$file" dev/v0.1.x/
done
git add .
git commit -m "feat(wave2): requirements + rehydration baseline"

git tag v0.1.6-REV2

# ─────────────────────────────────────────────────────────────
# 📦 Build release snapshot
cp dev/v0.1.x/rehash.v0.1.5-BUILD5.py release/v0.1.6/rehash.py
cp dev/v0.1.x/rehash_requirements.v0.1.6-REV2.md release/v0.1.6/REQUIREMENTS.md
echo "- Release v0.1.6 BUILD5" > release/v0.1.6/changelog.md
git add release/
git commit -m "release(v0.1.6): snapshot release folder"

# ─────────────────────────────────────────────────────────────
# 🔀 Squash merge to main
git checkout main
git merge --squash --allow-unrelated-histories dev/0.1.x
git commit -m "release: squash dev/0.1.x → main as v0.1.6-final"

# 🚢 Publish release files to root
cp release/v0.1.6/rehash.py .
cp release/v0.1.6/REQUIREMENTS.md .
git add rehash.py REQUIREMENTS.md
git commit -m "release(v0.1.6): publish root files"
git tag v0.1.6-final

# ─────────────────────────────────────────────────────────────
# ☁️ Push to GitHub
echo "🚀 Creating GitHub repo: $GH_REPO"
gh repo create "$GH_REPO" --public --source=. --remote="$REMOTE" --push
git push "$REMOTE" main
git push "$REMOTE" dev/0.1.x
git push "$REMOTE" --tags

echo "✅ DONE: https://github.com/YOUR_USERNAME/$GH_REPO"
