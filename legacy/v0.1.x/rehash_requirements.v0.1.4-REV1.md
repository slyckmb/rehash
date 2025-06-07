# rehash Requirements Document  
**Version: v0.1.4-REV1 (Effective starting BUILD4)**

---

## 📜 Overview

`rehash` is a tool for parsing, listing, filtering, and exporting ChatGPT conversations from a standard OpenAI export archive (folder or zip).

Designed for:

- Fast searching
- Easy filtering (JMESPath)
- Clean conversation export (JSON / YAML)
- Easy future upgrades
- Minimal but powerful CLI

---

## 📦 Core Functional Requirements

- Operate on a ChatGPT export archive (`.zip`) or extracted export folder.
- Automatically detect if input is `.zip` or folder.
- Load **conversations.json** primarily. (Other files will be addressed later.)
- If conversations reference external files, referenced files will later be bundled into an export archive (stub for now).
- Always output script name, version, and datetime stamp on:
  - Terminal output
  - Logs
  - Export files
- Script variables:
  - `SCRIPT_NAME`
  - `SCRIPT_VERSION`
- Header display every time script is run.

---

## 🛠 CLI Functionalities

| Command | Function |
|:-------:|:--------:|
| `-l`, `--list` | List all conversations (default trimmed view) |
| `-c`, `--conv` `<id>` | Export single conversation by ID |
| `--filter` `<jmespath>` | Apply JMESPath filter during listing |

### Modifiers (Space-separated words):
- `full` → Show full metadata in list
- `csv` → Export list to CSV file
- `tab` → Export list to TAB-separated file
- `json` → Export conversation as JSON (with `-c`)
- `yaml` → Export conversation as YAML (with `-c`)

---

## ⚙ CLI Usage Rules
<!-- PATCH v0.1.4 START -->

> **New CLI Usage Standard (Effective v0.1.4-BUILD4 and beyond):**

- The **path argument must be the first positional** after the script name.
- If no path is provided, it will **default to the current directory (`.`)**.
- After the path, specify the **operation flags** (`-l` or `-c`).
- After the operation flag, **space-separated modifiers** may follow (`full`, `csv`, `tab`, `json`, `yaml`).
- **Flags must not be combined with modifiers** (e.g., use `-l full`, not `-lfull`).

### ✅ Valid Examples:

```bash
rehash ./archive/ -l full csv
rehash ./export.zip -c abc123 json
rehash ./folder/ -l tab
rehash ./folder/ -c xyz789 yaml
```

### ❌ Invalid Examples:

```bash
rehash -l full csv ./folder/   # ❌ INVALID: path must come first
rehash -lfull                  # ❌ INVALID: modifiers must be separate
```

- If the **path is invalid or missing**, the tool will error cleanly.
- If **no operation flag (`-l`/`-c`)** is provided, help will be printed.

<!-- PATCH v0.1.4 END -->

---

## 🧩 Filters

- Filters must be passed via `--filter "expression"`
- Expressions are written in [JMESPath](https://jmespath.org/) syntax
- Example:

```bash
rehash ./folder/ -l --filter "items[?model=='gpt-4']"
```

- Filtering only affects listing (`-l`), not single conversation exports (`-c`).

---

## 📊 Conversation List - Default Columns (Trim Mode)

| Field | Description |
|:-----:|:-----------:|
| ID | Unique conversation ID |
| Title | Conversation title |
| Created At | Timestamp (readable) |
| Model | Model slug/identifier |

---

## 📊 Conversation List - Full Columns (Full Mode)

| Field | Description |
|:-----:|:-----------:|
| ID | Unique conversation ID |
| Title | Conversation title |
| Created At | UTC readable timestamp |
| First Message Date | First activity timestamp |
| Last Message Date | Last activity timestamp |
| Model | Model identifier |
| Custom GPT? | Yes/No |
| Total Messages | Number of messages |
| Attachments? | Yes/No (if files are linked) |

---

## 🖼️ Terminal Output

- All lists/tables use `rich` for pretty printing.
- All conversation details use `rich Panel`.
- Colors and bold labels used for readability.

---

## 📁 File Naming Standards

| File Type | Naming |
|:---------:|:------:|
| List CSV | `conversation_list.csv` |
| List TAB | `conversation_list.txt` |
| Single JSON Export | `conversation_<id>.json` |
| Single YAML Export | `conversation_<id>.yaml` |

---

## 🔒 Other Requirements

- CLI must **error cleanly** if wrong usage.
- CLI must **print help** if no operation (`-l` or `-c`) provided.
- Code must make it easy to add more modifiers and formats in future.
- No verbose mode required (verbosity off permanently for simplicity).

---

# ✅ Status

This spec is **LOCKED for rehash v0.1.4 and BUILD 4 development.**

---
