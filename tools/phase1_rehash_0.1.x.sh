#!/bin/bash
set -euo pipefail

### 🔰 Guardrails Rehydrator v2.2.0
### 📦 Phase: dev/0.1.x only (no 0.2.x contamination)
### 🕐 Generated: $(date -Iseconds)

REPO_NAME="rehash"
SOURCE_DIR="rehash"
REMOTE="origin"
GH_REPO="$REPO_NAME"

# ─────────────────────────────────────────────────────────────
# 🧠 Safety Check: Ensure no pre-existing .git from ZIP
if [ -d "$SOURCE_DIR/.git" ]; then
  echo "❌ ERROR: $SOURCE_DIR/.git exists — remove it before running."
  exit 1
fi

echo "🛠️ Rehydrating $REPO_NAME..."

mkdir -p "$REPO_NAME"
cd "$REPO_NAME"

# ─────────────────────────────────────────────────────────────
# 🔁 Init repo from scratch
git init -b main

# Create initial empty commit to enable squash later
git commit --allow-empty -m "chore: initial base commit for squash logic"

# ─────────────────────────────────────────────────────────────
# 🌱 Create dev/0.1.x branch
git checkout -b dev/0.1.x

WAVE_01=(
  "rehash.v0.1.0.py" "rehash.v0.1.1-BUILD1.py" "rehash.v0.1.2-BUILD2.py"
  "rehash.v0.1.3-BUILD3.py" "rehash.v0.1.4-BUILD4.py" "rehash.v0.1.5-BUILD5.py"
)
WAVE_02=(
  "rehash_requirements.v0.1.4-REV1.md"
  "rehash_requirements.v0.1.6-REV2.md"
  "REHYDRATION.md"
)

# Create folder structure
mkdir -p dev/v0.1.x release/v0.1.6

# ─────────── WAVE 1 ───────────
for file in "${WAVE_01[@]}"; do
  cp ../$SOURCE_DIR/$file dev/v0.1.x/
done
git add .
git commit -m "feat(wave1): core rehash engine v0.1 builds"

# ─────────── WAVE 2 ───────────
for file in "${WAVE_02[@]}"; do
  cp ../$SOURCE_DIR/$file dev/v0.1.x/
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
# 🔀 Merge to main (squash)
git checkout main
git merge --squash --allow-unrelated-histories dev/0.1.x
git commit -m "release: squash dev/0.1.x → main as v0.1.6-final"

# 🧾 Publish release files to root
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

echo "✅ Done: https://github.com/YOUR_USERNAME/$GH_REPO"
