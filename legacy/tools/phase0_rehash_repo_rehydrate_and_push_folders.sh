#!/bin/bash
set -euo pipefail

### 📦 Version: v2.1.1
### 🧠 Purpose: Structured dev/release rehydration with GitHub push
### ⏱️ Timestamp: $(date -Iseconds)

REPO_NAME="rehash"
GH_REPO="rehash"
SOURCE_DIR="rehash"
REMOTE="origin"

echo "🛠️ Rehydrating $REPO_NAME..."

mkdir -p "$REPO_NAME"
cd "$REPO_NAME"
git init -b main

### === 0.1.x BRANCH + RELEASE ===

mkdir -p dev/v0.1.x release/v0.1.6
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

for file in "${WAVE_01[@]}"; do cp ../$SOURCE_DIR/$file dev/v0.1.x/; done
git add .
git commit -m "feat(wave1): core rehash engine v0.1 builds"

for file in "${WAVE_02[@]}"; do cp ../$SOURCE_DIR/$file dev/v0.1.x/; done
git add .
git commit -m "feat(wave2): requirements + rehydration baseline"

git tag v0.1.6-REV2

# === Snapshot release/v0.1.6
cp dev/v0.1.x/rehash.v0.1.5-BUILD5.py release/v0.1.6/rehash.py
cp dev/v0.1.x/rehash_requirements.v0.1.6-REV2.md release/v0.1.6/REQUIREMENTS.md
echo "- Release v0.1.6 BUILD5" > release/v0.1.6/changelog.md
git add release/
git commit -m "release(v0.1.6): snapshot release folder"

# === Merge to main
git checkout main
git merge --squash dev/0.1.x
git commit -m "release: squash dev/0.1.x → main as v0.1.6-final"
cp release/v0.1.6/rehash.py .
cp release/v0.1.6/REQUIREMENTS.md .
git add rehash.py REQUIREMENTS.md
git commit -m "release(v0.1.6): publish root files"
git tag v0.1.6-final

### === 0.2.x BRANCH + RELEASE ===

mkdir -p dev/v0.2.x release/v0.2.5-dev+fx6
git checkout -b dev/0.2.x

WAVE_03=(
  "rehash.v0.2.3-dev.py" "rehash.v0.2.4-dev.py"
  "rehash.v0.2.4-dev+fx1.py" "rehash.v0.2.4-dev+fx2.py" "rehash.v0.2.4-dev+fx3.py"
)
WAVE_04=(
  ".meta.json" "requirements.txt"
  "testdata/user.json" "testdata/conversations.json"
  "testdata/file-sample-image.png" "testdata/file-sample-doc.txt"
)
WAVE_05=(
  "rehash_requirements.v0.2.0.md" "rehash_requirements.v0.2.1.md"
  "rehash_requirements.v0.2.2-dev.md" "rehash_requirements.v0.2.3-dev.md"
  "rehash_requirements.v0.2.4-dev.md" "rehash_requirements.v0.2.5-dev.md"
  "rehash_requirements.v0.2.5-dev+fx1.md" "rehash_requirements.v0.2.5-dev+fx2.md"
)
WAVE_06=(
  "rehash.v0.2.5-dev.py" "rehash.v0.2.5-dev+fx1.py" "rehash.v0.2.5-dev+fx2.py"
  "rehash.v0.2.5-dev+fx3.py" "rehash.v0.2.5-dev+fx4.py"
  "rehash.v0.2.5-dev+fx5.py" "rehash.v0.2.5-dev+fx6.py"
)

for file in "${WAVE_03[@]}"; do cp ../$SOURCE_DIR/$file dev/v0.2.x/; done
git add .
git commit -m "feat(wave3): add 0.2.x base and fx releases"

mkdir -p dev/v0.2.x/testdata
for file in "${WAVE_04[@]}"; do cp ../$SOURCE_DIR/$file dev/v0.2.x/$file; done
git add .
git commit -m "feat(wave4): test data and meta additions"

for file in "${WAVE_05[@]}"; do cp ../$SOURCE_DIR/$file dev/v0.2.x/; done
git add .
git commit -m "feat(wave5): requirements v0.2.x"

for file in "${WAVE_06[@]}"; do cp ../$SOURCE_DIR/$file dev/v0.2.x/; done
git add .
git commit -m "feat(wave6): final fx v0.2.5-dev+fx1 → fx6"

git tag v0.2.5-dev+fx6

echo "🛑 Dev complete. Skipping release v0.2.5-dev+fx6 — still in progress."
exit 0


# # === Snapshot release/v0.2.5-dev+fx6
# cp dev/v0.2.x/rehash.v0.2.5-dev+fx6.py release/v0.2.5-dev+fx6/rehash.py
# cp dev/v0.2.x/rehash_requirements.v0.2.5-dev+fx2.md release/v0.2.5-dev+fx6/REQUIREMENTS.md
# echo "- Release v0.2.5-dev+fx6 with fx2 lockfile" > release/v0.2.5-dev+fx6/changelog.md
# git add release/
# git commit -m "release(v0.2.5-dev+fx6): snapshot release folder"

# # === Main squash merge
# git checkout main
# git merge --squash dev/0.2.x
# git commit -m "release: squash dev/0.2.x → main as v0.2.5-dev+fx6-final"
# cp release/v0.2.5-dev+fx6/rehash.py .
# cp release/v0.2.5-dev+fx6/REQUIREMENTS.md .
# git add rehash.py REQUIREMENTS.md
# git commit -m "release(v0.2.5-dev+fx6): publish root files"
# git tag v0.2.5-dev+fx6-final

# # === PUSH TO GITHUB
# echo "🚀 Creating GitHub repo: $GH_REPO"
# gh repo create "$GH_REPO" --public --source=. --remote="$REMOTE" --push
# git push --tags "$REMOTE"
# git push "$REMOTE" main
# git push "$REMOTE" dev/0.1.x
# git push "$REMOTE" dev/0.2.x

# echo "✅ All waves rehydrated and pushed to https://github.com/YOUR_USERNAME/$GH_REPO"
