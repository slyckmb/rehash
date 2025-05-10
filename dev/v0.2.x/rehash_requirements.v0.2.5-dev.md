# 🛠️ rehash - Requirements Document (v0.2.5-dev)

> Canonical baseline: v0.2.4-dev  
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
- **If no arguments are provided, show help and exit.**
- **If path is `.` and more than one usable file is detected, abort with warning.**

---

## 🛠 CLI Functionalities

| Flag                    | Alias | Description                                   |
|-------------------------|-------|-----------------------------------------------|
| `--diary`               | `-d`  | Show list of conversations in terminal        |
| `--chat <ID>`           | `-c`  | Export a single conversation by ID            |
| `--journal`             | `-j`  | Extract messages matching filters/date        |
| `--filter <expr>`       | `-f`  | Apply filters by title, model, etc.           |
| `--date <YYYY-MM-DD>`   |       | Filter messages by date (Eastern Time)        |
| `--output <format>`     | `-o`  | Export format: `json`, `yaml`, `csv`, `txt`   |
| `--scan`                | `-s`  | Scan archive for metadata, searchable fields, and datetime range |
| `--help`                | `-h`  | Show usage and examples                       |

---

## ⚙ CLI Usage Rules

- Path must come first. It can be a folder or a `.zip` archive.
- If omitted: `rehash` (no args) will print help and exit.
- If the path is `.` (current directory):
  - ✅ Will proceed only if **exactly one** of the following exists:
    - A single `.zip` file
    - A single `conversations.json` in `.` root
  - ⚠️ If multiple usable files or folders are found:
    - Print warning:
      “⚠️ Multiple possible inputs found in directory. Please specify a file or folder.”
    - Then exit without scanning.
- Then, supply **one operation flag only**: `--diary`, `--chat`, `--journal`, or `--scan`.
- Filters and format modifiers follow (order does not matter).
- Do not combine long/short flags (e.g., `-lfull ❌`).
- All actions echo the script name, version, UTC timestamp, and CLI args.

---

## 🛡️ Ambiguous Input Handling

| Command                  | Behavior                                                                 |
|--------------------------|--------------------------------------------------------------------------|
| `rehash`                 | ❌ Invalid — prints usage and exits                                       |
| `rehash .`               | ✅ Allowed **only if** one usable file is detected (`.zip` or `conversations.json`) |
| `rehash archive.zip`     | ✅ Preferred — exact path provided                                        |
| `rehash folder/`         | ✅ Preferred — exact folder given                                         |
| `rehash .` with >1 files | ⚠️ Fails — prompts user to choose file explicitly                         |

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

### Message Scope (requires `--journal`)
- `sender`
- `content`
- `timestamp_et`
- `conversation_title`
- `conversation_id`

---

## 🧩 Filters - Detailed Behavior

### Simplified Filter Syntax

| Syntax         | Meaning              |
|----------------|----------------------|
| `field=value`  | Exact match          |
| `field~text`   | Substring/contains   |
| `field>number` | Greater-than         |
| `field<number` | Less-than            |

Examples:
- `--filter title~fitness`
- `--filter model=gpt-4 total_messages>3`
- `--filter sender=user conversation_title~routine`

---

### Date Filtering (`--date`)

When `--journal` is active, `--date YYYY-MM-DD` filters messages by **local time** (America/New_York, DST-aware).

Example:
```bash
--journal --filter title~fitness --date 2025-04-15
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

| Export Type        | Label     | Filename Pattern                                                    |
|--------------------|-----------|----------------------------------------------------------------------|
| Diary (full list)  | `diary`   | `diary_<user>_<start>-<end>_exported-<timestamp>.json`              |
| Single Chat        | `chat`    | `chat_<slug>_<id>_<created>_to_<updated>.json`                      |
| Filtered Messages  | `journal` | `journal_<slug>_(<filtertag>)[<msgcount>]_<date>.json`              |

---

### 📓 Journal Filename Fields

| Field         | Description                                     | Example             |
|---------------|-------------------------------------------------|---------------------|
| `slug`        | Slugified title (max 40 safe chars)             | `phd_fitness`       |
| `filtertag`   | Field used in `--filter` expression              | `title`, `id`       |
| `msgcount`    | Number of exported messages                     | `65`                |
| `date`        | Date filter (in ET, `YYYY-MM-DD`)               | `2025-04-15`        |

Final format:
```
journal_<slug>_(<filtertag>)[<count>]_<date>.json
```

Example:
```
journal_phd_fitness_(title)[65]_2025-04-15.json
```

---

### 💬 Chat Filename Fields

| Field         | Description                               | Example            |
|---------------|-------------------------------------------|--------------------|
| `slug`        | Title-derived short name (≤40 chars)      | `phd_fitness`      |
| `id`          | First 8 chars of conversation UUID        | `681a8b7a`         |
| `created`     | `YYMMDD-HHMM` in ET                       | `250506-1821`      |
| `updated`     | `YYMMDD-HHMM` in ET                       | `250506-1904`      |

Final format:
```
chat_<slug>_<id>_<created>_to_<updated>.json
```

Example:
```
chat_phd_fitness_681a8b7a_250506-1821_to_250506-1904.json
```

---

## ✅ Status

This specification is **under active development** as `rehash_requirements.v0.2.5-dev.md`  
All changes follow patch protocol from `v0.2.4-dev`.  
All CLI renames, file formats, and filter behaviors are now locked as canonical unless superseded.

---

<!-- PATCH: +scan-nonconformance -->
### ⚠️ CLI Output Non-Conformance: `--scan`

The current implementation of the `--scan` mode does **not conform** to the formatting or content defined in prior requirements (see v0.2.4-dev).

#### ❌ Current Behavior
```
Archive contains 470 conversations.
Models used: ?
Example IDs: ...
```

#### ✅ Expected Behavior (per spec)
```
🗂 Archive Path: path/to/archive.zip
📅 Date Range: 2024-02-03 → 2025-05-08
💬 Conversations: 932
🧪 Searchable Fields:
  - Conversations: id, title, created_at, model, custom, total_messages, attachments
  - Messages: sender, timestamp_et, content, conversation_title
🧠 Timezone: America/New_York
✅ Custom GPTs detected
⚠️ X conversations missing title
```

This will be addressed in the `v0.2.5-dev` patch cycle.
