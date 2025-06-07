````markdown
# 🧠 dev/rehash-v1-cli TASK_TRACKER.md

🔧 _Modular CLI for ChatGPT export parsing, transformation, and emission._

---

## ✅ DONE

| ✅ Task | Description |
|--------|-------------|
| 🧱 Branching | Created `dev/rehash-v1-cli` from `v0.1.6-final` |
| 🍒 Cherry-picked key commits | CLI scaffold, loader, filters, emit logic |
| 📦 extract_export.py | Parses .zip ➤ loads conversations.json |
| 🧪 Tests for extract_export | Validated: good zip, bad zip, missing file, bad JSON |
| 🔁 utils.py | CLI via `argparse`, command dispatcher |
| 🧪 Virtualenv (`rehash`) | Python venv activated, pytest functional |
| 📤 emit_structured_json.py | Writes structured JSON with timestamp+slug |
| 🧠 Robust error handling | Timestamp fallback, float coercion, path creation |

---

## 🚧 TODO

| 🚧 Task | Priority | Notes |
|--------|----------|-------|
| 🧪 Test `emit_structured_json.py` | 🔥 high | Assert output file count + filenames |
| 🔗 Wire `emit_conversations()` to CLI | 🔥 high | Enable file output via `parse` command |
| 🧠 Refine `format_chat()` | 🟡 med | Flatten `mapping`, enrich metadata |
| 📁 Output structure convention | 🟡 med | `out/YYYY-MM-DD__slug.json` |
| ⚙️ Add CLI args: `--emit`, `--out-dir` | 🟡 med | Add `argparse` opts |
| 📈 Add test coverage tools | 🟢 low | Track via `pytest-cov` |
| 📘 Add README usage docs | 🟢 low | CLI and example runs |
| 🔁 Regression check | 🟢 low | Compare against `release/v0.1.6/rehash.py` outputs |

---

📂 File: `dev/rehash-v1-cli/TASK_TRACKER.md`
Author: 🧑‍💻 Jake (AI)
Updated: 2025-06-04
````
