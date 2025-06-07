#!/bin/bash
set -euo pipefail

### 🧪 Test: Rehash JSON Parser CLI (v0.3.0-dev)

# Script & test paths
SCRIPT="rehash.v0.3.0-dev.py"
LOADER="rehash_json_loader.v0.3.0-dev.py"
TESTFILE="../../docs/testdata/conversations.json"

echo "🧰 Preparing runtime filenames..."
cp "$SCRIPT" rehash.py
cp "$LOADER" rehash_json_loader.py

echo "🔧 Testing $SCRIPT with $TESTFILE"

# Check required files exist
for file in "$SCRIPT" "$LOADER" "$TESTFILE"; do
  [[ -f "$file" ]] || { echo "❌ Error: Missing $file"; exit 1; }
done

# Run parser
echo "🚀 Executing parser..."
python3 rehash.py parse "$TESTFILE"

# Cleanup
echo "🧹 Cleaning up runtime files..."
rm -f rehash.py rehash_json_loader.py

echo "✅ Test complete."
