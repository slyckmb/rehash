# rehash - ChatGPT Export Parser Tool (v0.1.0)

## 🛠 Project Overview
CLI tool to parse ChatGPT exports, list conversations, and export conversations or conversation lists.  
Designed for maximum UX speed, minimal typing, dynamic filters, and human-friendly output.

---

## 🚀 Features

- **Input Source**:
  - First positional argument is the folder or `.zip` file to process.
  - If missing, assume current directory (`.`).

- **List conversations** (`-l`, `--list`):
  - Default table listing is **Trimmed metadata**.
  - `full` modifier shows **Full metadata**.
  - `csv` or `tab` modifiers additionally export the list to a file.
  - Modifiers **can be supplied in any order**.
  - Optional dynamic filtering with `--filter` (`jmespath` syntax).

- **Export conversation** (`-c`, `--conv`):
  - Always outputs selected conversation to terminal (pretty-printed using `rich`).
  - `json` or `yaml` modifiers also export the conversation to file.
  - Modifiers **can be supplied in any order**.

- **Improve terminal output readability**:
  - Use `rich` library:
    - Colors for User vs Assistant.
    - Bold conversation titles.
    - Dimming timestamps.
    - Pretty formatting with indentation.

- **Always Print Metadata**:
  - Script name: `rehash`
  - Version: `v0.1.0`
  - Current UTC datetime.

---

## 🧩 CLI Flags

| Flag | Description |
|:----:|:-----------:|
| `<path>` | First positional argument (input folder or zip). Defaults to `.` if missing. |
| `-l`, `--list` | List conversations (default: Trim mode, table to terminal) |
| `full` | Modifier: expand to Full metadata view |
| `csv` | Modifier: export list to `conversation_list.csv` |
| `tab` | Modifier: export list to `conversation_list.txt` |
| `--filter "jmespath_expr"` | Dynamic conversation list filtering |
| `-c`, `--conv <conversation_id>` | Output and export single conversation |
| `json` | Modifier: export conversation to JSON file |
| `yaml` | Modifier: export conversation to YAML file |

---

## 📋 Trim Mode Default Columns

| Column | Description |
|:------:|:-----------:|
| ID | Conversation ID |
| Title | Conversation Title |
| Created At | Datetime when conversation created |
| Model | Model slug/identifier (e.g., `gpt-4`) |

✅ Only 4 essential fields for quick scanning.

---

## 📋 Full Mode Columns

| Column | Description |
|:------:|:-----------:|
| ID | Conversation ID |
| Title | Conversation Title |
| Created At | Conversation created datetime |
| First Message Date | Datetime of first message |
| Last Message Date | Datetime of last message |
| Model | Model slug or identifier |
| Custom GPT? | Yes/No |
| Total Messages | Number of messages in the conversation |
| File Attachments? | Yes/No |

---

## 📦 Output File Naming

| Operation | Filename |
|:---------:|:--------:|
| List Export CSV | `conversation_list.csv` |
| List Export Tabbed TXT | `conversation_list.txt` |
| Conversation Export JSON | `<conversation_id>.json` |
| Conversation Export YAML | `<conversation_id>.yaml` |
| External Assets Archive | `<conversation_id>_assets.zip` |

---

## 🛡 Filters (Implemented)

- **Dynamic field filtering** using `--filter "jmespath expression"`.
- Example filter fields available:
  - `id`
  - `title`
  - `created_at`
  - `first_message`
  - `last_message`
  - `model`
  - `custom`
  - `total_messages`
  - `attachments`

Examples:

```bash
--filter "model == 'gpt-4'"
--filter "custom == 'Yes'"
--filter "total_messages > `10`"
--filter "contains(title, 'project')"
```

✅ jmespath expressions allow very powerful selection without rigid CLI flags.

---

## 📋 Usage Display Definition

When user runs `rehash --help` or invalid usage, **output must show:**

- Script title and version
- Example usages:
  - `rehash ./export.zip -l`
  - `rehash ./folder -l full csv`
  - `rehash ./export.zip -c abc123 json`
- Full list of supported flags:
  - `-l`, `--list`
  - `full`
  - `csv`
  - `tab`
  - `--filter`
  - `-c`, `--conv`
  - `json`
  - `yaml`
- Explain available **Filter Fields** clearly
- File output behavior
- "If path is missing, defaults to current folder"

---

## ✅ Validation Requirements

- Validate input folder/zip.
- Validate existence of `conversations.json`.
- Validate correct use of modifiers (only one file type allowed per export).
- Validate correct syntax for `--filter` expressions (catch bad jmespath).
- Validate conversation ID existence before export.

---

## 📜 Notes

- `rich` handles beautiful terminal output.
- `jmespath` handles smart dynamic filtering.
- CLI designed for fast muscle memory workflows.
- One `.py` file initially, modular inside for maintenance.

---
