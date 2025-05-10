#!/bin/bash
set -euo pipefail

### 🧠 Guardrails Phase: dev/0.2.x only
### 🔁 Continues after v2.2.0 rehydrator
### ❗ No squash, no push, no release artifacts

REPO_NAME="rehash"
SOURCE_DIR="../rehash"  # Assuming you're in rehash/ already
DEV_BRANCH="dev/0.2.x"
RELEASE_TAG="v0.2.5-dev+fx6"

# ─────────────────────────────────────────────────────────────
# 🧠 Git check: Ensure we're inside a repo
if [ ! -d .git ]; then
  echo "❌ ERROR: Not inside a Git repo. cd into your repo folder first."
  exit 1
fi

# ─────────────────────────────────────────────────────────────
# 🌱 Create dev/0.2.x branch
git checkout -b "$DEV_BRANCH" || git checkout "$DEV_BRANCH"

# ─────────── WAVE 3 ───────────
WAVE_03=(
  "rehash.v0.2.3-dev.py" "rehash.v0.2.4-dev.py"
  "rehash.v0.2.4-dev+fx1.py" "rehash.v0.2.4-dev+fx2.py" "rehash.v0.2.4-dev+fx3.py"
)
mkdir -p dev/v0.2.x
for file in "${WAVE_03[@]}"; do
  cp "$SOURCE_DIR/$file" dev/v0.2.x/
done
git add .
git commit -m "feat(wave3): base + fx rehash v0.2.3 → v0.2.4"

# ─────────── WAVE 4 ───────────
WAVE_04=(
  ".meta.json" "requirements.txt"
  "testdata/user.json" "testdata/conversations.json"
  "testdata/file-sample-image.png" "testdata/file-sample-doc.txt"
)
mkdir -p dev/v0.2.x/testdata
for file in "${WAVE_04[@]}"; do
  cp "$SOURCE_DIR/$file" "dev/v0.2.x/$file"
done
git add .
git commit -m "feat(wave4): meta and test data added"

# ─────────── WAVE 5 ───────────
WAVE_05=(
  "rehash_requirements.v0.2.0.md" "rehash_requirements.v0.2.1.md"
  "rehash_requirements.v0.2.2-dev.md" "rehash_requirements.v0.2.3-dev.md"
  "rehash_requirements.v0.2.4-dev.md" "rehash_requirements.v0.2.5-dev.md"
  "rehash_requirements.v0.2.5-dev+fx1.md" "rehash_requirements.v0.2.5-dev+fx2.md"
)
for file in "${WAVE_05[@]}"; do
  cp "$SOURCE_DIR/$file" dev/v0.2.x/
done
git add .
git commit -m "feat(wave5): requirements for 0.2.x fx series"

# ─────────── WAVE 6 ───────────
WAVE_06=(
  "rehash.v0.2.5-dev.py" "rehash.v0.2.5-dev+fx1.py" "rehash.v0.2.5-dev+fx2.py"
  "rehash.v0.2.5-dev+fx3.py" "rehash.v0.2.5-dev+fx4.py"
  "rehash.v0.2.5-dev+fx5.py" "rehash.v0.2.5-dev+fx6.py"
)
for file in "${WAVE_06[@]}"; do
  cp "$SOURCE_DIR/$file" dev/v0.2.x/
done
git add .
git commit -m "feat(wave6): full fx line 0.2.5-dev+fx1 → fx6"

# ─────────── Tag release head ───────────
git tag "$RELEASE_TAG"

echo "✅ Phase complete: dev/0.2.x hydrated + tagged as $RELEASE_TAG"
