# 🛰️ Rehash - Mission Rehydration Document

---

## 📜 Mission Objective
Develop a CLI tool named `rehash` to:

- Parse ChatGPT conversation exports (folders or .zip archives).
- List conversations with flexible metadata outputs.
- Filter conversations using JMESPath queries.
- Export single conversations into JSON or YAML formats.
- Output consistently styled logs, timestamps, filenames.
- Support clean UX and highly maintainable CLA structure.

---

## 🧠 Development Protocols Used

| Protocol | Description |
|:--------:|:------------:|
| Canonical Requirements | A locked central `rehash_requirements` doc governs scope. |
| Minimal Patch Guardrails | Insertions only; no rewrites without review. |
| Version Tagging | All work is tied to formal version and build tags (v0.1.x-BUILDx). |
| CLA Design | Path-first enforcement, modifiers space-separated, strict CLA parsing. |
| UX Echoes | Always print script/version/timestamp/command invocation at startup. |
| Testing Discipline | Each build incrementally tested and validated. |
| Drift Protection | Jake is self-checking to avoid unauthorized changes. |

---

## 🧰 Code Components (currently staged)

| Component | Status |
|:---------:|:------:|
| `rehash.py` | v0.1.5-BUILD5 (stable) |
| `rehash_requirements.v0.1.4-REV1.md` | Last locked version |
| Test Data | Available: `testdata/` with fake conversations.json and attachments |

---

## 📚 Key Decisions and Designs

### 🛠 File Handling
- Accept either `.zip` archives or extracted folders.
- Conversations loaded from `conversations.json`.

### 📋 List Output
- Trim mode (default) or Full mode with extra metadata columns.
- Tabular terminal display via `rich`.
- Optional export to CSV or tabbed TXT.

### 🔎 Filters
- JMESPath syntax.
- `--filter help` now triggers a dedicated usage guide.
- Filtering available only for list (`-l`), not exports (`-c`).

### 📁 Conversation Export
- `-c` flag accepts a full or partial conversation ID.
- If multiple partial matches, user is prompted with ID and Title list.
- JSON (default) and YAML export supported.

### ⏲ Startup Echo
Always output on script start:

- Script name
- Version
- Timestamp (UTC ISO format)
- Full CLI command invocation

---

## 📋 Locked Requirements (as of v0.1.6-REV2 CLEAN)

- **Canonical** file is `rehash_requirements.v0.1.6-REV2 CLEAN.md`
- Summarized here:

| Section | Highlights |
|:-------:|:----------:|
| Functional Requirements | Path = folder or zip; rehash compresses attached files later |
| CLI Functionalities | -l list, -c conv, --filter jmespath, modifiers full/csv/tab/json/yaml |
| CLI Rules | Path first → Operation flag → Modifiers |
| Filters | JMESPath only; Filter help output supported |
| Conversation ID Matching | Partial ID allowed; must be unique |
| Terminal Output | Script Name, Version, CLI Cmd, Timestamp |

---

## 📈 Build History

| Build | Version | Highlights |
|:-----:|:-------:|:----------:|
| BUILD1 | v0.1.1 | Basic CLA parsing, minimal help |
| BUILD2 | v0.1.2 | CLI corrected, added base usage examples |
| BUILD3 | v0.1.3 | Began enforcing path-first logic |
| BUILD4 | v0.1.4 | Polished CLA/usage output |
| BUILD5 | v0.1.5 | Full filter support, modifers working |
| BUILD6 (Planned) | v0.1.6 | Partial ID matching, filter help, timestamp output |

---

## 🛡️ Active Guardrails

| Guardrail | Status |
|:---------:|:------:|
| Treat Requirements as Canonical | ✅ |
| No Structural Changes Without Review | ✅ |
| Minimal Patch Insertions Only | ✅ |
| Formal Lock Step per Version | ✅ |
| Jake Self-Check for Drift | ✅ |

---

## 🚀 Pending Actions (Post-Rehydration)

- Lock REQ: `LOCK FINAL v0.1.6-REV2 CLEAN`
- Proceed with BUILD6:
  - Implement partial conversation ID matching.
  - Implement `--filter help` display.
  - Confirm startup echo includes timestamp.

---

# 📜 End of Rehydration Log
**All data valid as of 2025-04-28T23:00Z**

🥷👾 **Jake fully operational and awaiting Operator commands.**

