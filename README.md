```markdown
# rehash

A command-line tool to parse and filter OpenAI ChatGPT exports into structured JSON.

---

## ✨ Features

- 📦 Parse raw `chatgpt-export.zip` files into structured per-conversation JSON
- 🧠 Preserve conversation metadata (title, participants, timestamps)
- 💪 Filter conversations by **fitness/training keywords**
- ✅ Extensible keyword patterns via `filter_fitness_logs.py`
- 🧪 99% test coverage, strict type-checking, and linter clean
- ⚡ Lightweight, zero dependencies outside the Python standard library + small helpers (`rich`, `pyyaml`, `jmespath`)

---

## 🚀 Installation

From source (recommended during dev):

```bash
git clone https://github.com/yourname/rehash.git
cd rehash
pip install -e ".[dev]"
```

This installs the `rehash` CLI into your environment.

---

## 🚀 Usage

After installing, the `rehash` command is available on your PATH.

### Parse a ChatGPT export

```bash
rehash parse-export ~/Downloads/chatgpt-export.zip --out out.json/
```

This will:
- Extract conversations from the `chatgpt-export.zip`
- Emit each conversation as a structured JSON file in `out.json/`
- Print a summary with the total number of conversations processed

---

### Parse **fitness-only** conversations

```bash
rehash parse-export ~/Downloads/chatgpt-export.zip --out fitness.json/ --fitness-only
```

This will:
- Extract conversations that **match fitness/training patterns**
- Skip all unrelated conversations
- Print a report like:

```
📦 Loading export: chatgpt-export.zip
🧠 Total conversations: 789
💪 Fitness conversations exported: 12
```

---

### Custom export location

```bash
rehash parse-export path/to/export.zip --out my-output/
```

You can specify any output directory. Files are written as JSON with safe filenames and ISO8601 timestamps.

---

### Error handling

- If the export file is missing or corrupt, `rehash` exits with an error code.
- If `--fitness-only` is used but no conversations match, it exits cleanly with `0` and an empty output directory.

---

### CLI Help

```bash
rehash --help
rehash parse-export --help
```

---

### Examples

```bash
# Parse all conversations
rehash parse-export export.zip --out out.json/

# Parse only fitness conversations
rehash parse-export export.zip --out fitness.json/ --fitness-only
```

---

## 🧪 Development

Clone the repo and install in editable mode with dev dependencies:

```bash
pip install -e ".[dev]"
```

Run tests with coverage:

```bash
pytest --cov=rehash --cov-branch --cov-report=term
```

Lint + type-check:

```bash
make lint
```

Clean build/test artifacts:

```bash
make clean
```

---

## 📄 License

MIT — see [LICENSE](LICENSE).
```
