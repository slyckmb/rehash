# 🛠️ rehash - Requirements Document (v0.2.3-dev)

> Canonical baseline: v0.2.2-dev  
> Version status: under development  
> Guardrails: guardrails_bundle_v2.2.2.md  
> All updates from baseline follow minimal patch protocol.

---

## 📦 Core Functional Requirements

- Operate on a ChatGPT export archive (`.zip`) or extracted folder.
- Load necessary `.json` files:
  - Load `conversations.json` primarily.
  - Path can be either an extracted folder OR a .zip archive. (Auto-detect.)
- Support listing all conversations with optional filters and modifiers.
- Support exporting a single conversation by ID to JSON or YAML.
- Support message-level extraction and export on a specific date.
- Compress any external files linked by conversations into an archive if exporting.
- Output should always include:
  - Script name
  - Script version
  - Full CLI arguments
  - UTC timestamp
- Provide a scan mode to summarize archive content, searchable fields, and coverage.
- Output should be flat, non-nested, GPT-friendly JSON or text structures.
- Support simplified filter expressions (not full JMESPath).

---

## 🛠 CLI Functionalities

| Flag | Alias | Description |
|------|-------|-------------|
| `--list` | `-l` | Show list of conversations in terminal |
| `--conversation <ID>` | `-c <ID>` | Export a single conversation by ID |
| `--messages` | `-m` | Extract messages matching filters/date |
| `--filter <expr>` | `-f` | Apply filters by title, model, etc. |
| `--date <YYYY-MM-DD>` | `-d` | Filter messages by date (Eastern Time) |
| `--output <format>` | `-o` | Export format: `json`, `yaml`, `csv`, `txt` |
| `--scan` | `-s` | Scan archive for metadata, searchable fields, and datetime range |
| `--help` | `-h` | Show usage and examples |

---

## ⚙ CLI Usage Rules

- Path must come first. It can be a folder or a `.zip` archive. If omitted, defaults to current directory (`.`).
- Then, supply **one operation flag only**: `--list`, `--conversation`, `--messages`, or `--scan`.
- Filters and format modifiers follow (order does not matter).
- Do not combine long/short flags (e.g., `-lfull ❌`).
- All actions echo the script name, version, UTC timestamp, and CLI args.

---

## 📋 Available Filter Fields

### Conversation Scope (default)
- `id`
- `title`
- `created_at`
- `model`
- `custom`
- `total_messages`
- `attachments`
- `first_message`
- `last_message`

### Message Scope (requires `--messages`)
- `sender`
- `content`
- `timestamp_et`
- `conversation_title`
- `conversation_id`

---

## 🧩 Filters - Detailed Behavior

### Simplified Filter Syntax

| Syntax | Meaning |
|--------|---------|
| `field=value` | Exact match |
| `field~text` | Substring/contains |
| `field>number` | Greater-than |
| `field<number` | Less-than |

Examples:
- `--filter title~fitness`
- `--filter model=gpt-4 total_messages>3`
- `--filter sender=user conversation_title~routine`

### Date Filtering (`--date`)

When `--messages` is active, `--date YYYY-MM-DD` filters messages by **local time** (America/New_York, DST-aware).

Example:
```bash
--messages --filter title~fitness --date 2025-04-15
```

Will return all messages **on April 15** in convos titled “fitness”.

---

## 📊 Archive Scan Output (`--scan` / `-s`)

Produces a formatted terminal report showing:

- Archive source path
- Total conversations
- Earliest/latest timestamps
- Available filter fields by scope
- Presence of Custom GPTs or file attachments
- Timezone used (default: America/New_York)
- Warnings (e.g., missing titles)

Example:

```
🗂 Archive Path: archive.zip
📅 Date Range: 2024-02-03 → 2025-05-08
💬 Conversations: 932
🧪 Searchable Fields:
  - Conversations: id, title, created_at, model, custom, total_messages, attachments
  - Messages: sender, timestamp_et, content, conversation_title

🧠 Timezone: America/New_York
✅ Custom GPTs detected
⚠️ 3 conversations missing title
```

This mode is informational only and does not modify or export files.

---

## 📤 Output Naming Standards

| Action | Output File |
|--------|-------------|
| `--list` with `--output csv` | `conversation_list.csv` |
| `--list` with `--output txt` | `conversation_list.txt` |
| `--conversation` with `--output json` | `conversation_<id>.json` |
| `--conversation` with `--output yaml` | `conversation_<id>.yaml` |
| `--messages` with `--output json` | One JSON per convo: `message_<title>_<date>.json` |
| `--scan` | Terminal only (no file) |

---

## 🎯 Examples

```bash
rehash archive.zip -l
rehash archive.zip --list --filter title~fitness --output csv

rehash archive.zip -c abc123 -o yaml
rehash archive.zip --conversation xyz789 --output json

rehash archive.zip -m --filter title~routine --date 2025-04-15
rehash archive.zip --messages -f title~routine -d 2025-04-15 -o json

rehash archive.zip --scan
```

---

## ✅ Status

This specification is **under active development** as `rehash_requirements.v0.2.3-dev.md`  
All changes follow patch protocol from `v0.2.2-dev`.  
All previous patch tags (`-BUILD`, `-REV`) are retired in favor of clean semver + suffixes only.

---
