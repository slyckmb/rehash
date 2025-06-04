#!/bin/bash
set -euo pipefail

### 🧪 Test: Rehash JSON Parser CLI (v0.3.0+fx1)

# Script & test paths
SCRIPT="rehash.v0.3.0+fx1.py"
LOADER="rehash_json_loader.v0.3.0+fx1.py"
TESTFILE="../../docs/testdata/conversations.json"

echo "🧰 Preparing runtime filenames..."
cp "$SCRIPT" rehash.py
cp "$LOADER" rehash_json_loader.py

echo "🔧 Testing $SCRIPT with $TESTFILE"

# Check file exists
if [[ ! -f "rehash.py" ]] || [[ ! -f "rehash_json_loader.py" ]]; then
  echo "❌ Required files missing."
  exit 1
fi

if [[ ! -f "$TESTFILE" ]]; then
  echo "❌ Error: Test file not found: $TESTFILE"
  exit 1
fi

# Execute parser
echo "🚀 Executing parser..."
python3 rehash.py parse "$TESTFILE"

# Cleanup
echo "🧼 Cleaning up temp files..."
rm -f rehash.py rehash_json_loader.py

echo "✅ Test complete."
