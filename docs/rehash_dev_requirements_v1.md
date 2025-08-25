# 🧠 Rehash Dev Requirements (v1)

> HealthFit Side Tool – Chat Rehydration + Export Flow  
> Codename: `rehash`  
> Purpose: Process ChatGPT exports into structured, usable log JSONs for downstream GPT pipeline.

---

## 📌 Purpose

Rehash is a side tool designed to automate extraction and transformation of raw ChatGPT `.json` export files into per-day, per-conversation workout JSON blobs, ready for alias patching + synthesis.

This replaces the current *manual copy/paste* + rename loop.

---

## 📂 Inputs

### 1. ChatGPT JSON Export

- 📁 `staging/chatgpt/2025-05-22_084543_chatgpt_export.zip`
- Structure:
  ```
  └── chatgpt_export.zip
      └── conversations.json
  ```

### 2. Human Metadata (optional but encouraged)

- Folder: `staging/chat/md/`
- Files: Markdown-transcribed workouts with rich language content
- Naming: `chat_YYYY-MM-DD_HHMMSS_title-web_primary.md`

---

## 🧪 Output Targets

### ✅ Extracted Daily Chat JSONs

- Output to: `staging/chat/01_raw/`
- Naming: `chat_YYYY-MM-DD_HHMMSS_[chat-title]-export.json`

Each file should:
- Contain all messages in order
- Preserve roles (`user`, `assistant`)
- Retain timestamps if available
- Include minimal required metadata (`title`, `date`, `source`)

---

## 🧰 Functional Requirements

### 1. 🎯 Zip Extractor
- [ ] Accept a zip archive of exported conversations
- [ ] Auto-extract to memory (or `.tmp/` if needed)
- [ ] Validate `conversations.json` format

### 2. 🧠 Log Picker
- [ ] Select only fitness/workout logs (optional fuzzy filter)
- [ ] Heuristic:
  - Title contains: `"phd"`, `"fitness"`, `"log"`, `"workout"`
  - OR Assistant message matches fitness context

### 3. 📅 Date Segmenter
- [ ] Auto-parse timestamp of chat
- [ ] Split into per-day files (can be multi-chat per day)

### 4. 📦 Structured Exporter
- [ ] Write per-chat JSONs to `01_raw/`
- [ ] Sanitize: remove extraneous keys
- [ ] Keep only:
  ```json
  {
    "title": "string",
    "timestamp": "iso8601",
    "messages": [ { "role": "user", "content": "..." }, ... ],
    "source": "chatgpt"
  }
  ```

---

## 🧠 Optional Enhancements

### 🪄 Human-in-the-loop CLI

```bash
rehash extract --zip staging/chatgpt/export.zip
rehash clean --filter fitness --preview
rehash emit --output staging/chat/01_raw/
```

### 🤖 GPT-aided log identifier

Use GPT to classify whether a chat contains fitness data. (Later phase.)

---

## ⛓ Integration Hooks

Rehash feeds into:

```
→ staging/chat/01_raw/…json
      ↳ gpt_generate_alias_patch.py
      ↳ render_workout_log.py
```

---

## 🔧 Tech Stack Suggestions

- ✅ `zipfile` + `tempfile` stdlib for archive ops
- ✅ `json`, `datetime`, `re` for core parsing
- 🧠 Optional: `tqdm`, `rich` for CLI display
- 🧪 Tests in `tests/tools/rehash/`

---

## 🔐 Security & Notes

- Strip PII (usernames, emails) if present
- Sanitize any tokens (ChatGPT adds unique IDs)
- Non-fitness chats should not be saved unless debug mode is active

---

## 🚦 Dev Status: Not Started

This is greenfield.
Kickoff can be CLI-first, then iterate toward lib+API-ready structure.

Start Point:
```bash
rehash extract staging/chatgpt/export.zip
```

---

## 📁 Future Structure Proposal

```
tools/rehash/
├── extract_export.py
├── filter_fitness_logs.py
├── emit_structured_json.py
├── __main__.py           # CLI entry
tests/tools/rehash/
```

---

🧠 Jake ready for side quest: **rehash-dev**
Say: `start rehash extract tool` to bootstrap the CLI 🛠️

```bash
alias_patch --rehash