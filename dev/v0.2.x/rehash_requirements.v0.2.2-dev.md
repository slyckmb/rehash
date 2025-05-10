# 🛠️ rehash - Requirements Document (v0.2.2-dev)

> Canonical baseline: v0.1.6-REV2  
> Version status: under development  
> Guardrails: guardrails_bundle_v2.2.2.md  
> All updates from baseline follow minimal patch protocol.  
> Skips v0.2.0 and v0.2.1 by Operator directive.

---

## 📦 Core Functional Requirements

- Operate on a ChatGPT export archive (`.zip`) or extracted folder.
- Load necessary `.json` files:
  - Load `conversations.json` primarily.
  - Path can be either an extracted folder OR a .zip archive. (Auto-detect.)
- Support listing all conversations with optional filters and modifiers.
- Support exporting a single conversation by ID to JSON or YAML.
- Compress any external files linked by conversations into an archive if exporting.
- Output should always include:
  - Script name
  - Script version
  - Full CLI arguments
  - UTC timestamp
- Should be future-expandable:
  - Allow easy addition of file types.
  - Allow easy addition of output formats.
  - Allow easy addition of filters.

---

## 🛠 CLI Functionalities

| Flag | Description |
|:---|:---|
| `-l`, `--list` | List conversations in terminal (trim mode default). |
| `-c`, `--conv <CONV_ID>` | Export a specific conversation. |
| `--filter <filter>` | Filter conversations by metadata. Use `--filter help` for field names and syntax. |
| `-h`, `--help` | Show usage/help information. |

Modifiers (for use after the path and operation flag):

| Modifier | Meaning |
|:---|:---|
| `full` | Show full metadata columns when listing |
| `csv` | Export list to CSV file |
| `tab` | Export list to Tab-separated TXT file |
| `json` | Export conversation to JSON |
| `yaml` | Export conversation to YAML |

---

## ⚙ CLI Usage Rules

- **Path must come first.** It can be a folder or a `.zip` archive. If omitted, defaults to current directory (`.`).
- Then, supply the **operation flag** (`-l` or `-c`).
- **Modifiers** follow the op flag (e.g., `full`, `csv`), separated by spaces.
- Modifiers must not be attached to flags (e.g., `-lfull` ❌).
- The script will **echo all CLA**, version, and UTC timestamp at start.
- If no operation flag is provided, usage/help is shown.
- `--filter help` prints all available filterable fields and examples.
- If a filter is passed and returns no matches, rehash will print:

```
No conversations matched filter: [expression]  
👉 Tip: Use --filter help to view supported fields and syntax.
```

---

## 📋 Available Filter Fields

(Supports both JMESPath and simplified filter syntax — see below)

- `id`
- `title`
- `created_at`
- `model`
- `custom`
- `total_messages`
- `attachments`
- `first_message`
- `last_message`

---

## 🧩 Filters - Detailed Behavior

### Simplified Filter Syntax (added in v0.2.2-dev)

rehash now supports user-friendly filter expressions without JMESPath:

| Syntax        | Meaning                      |
|---------------|------------------------------|
| field=value   | Exact match                  |
| field~text    | Substring match (contains)   |
| field>number  | Greater-than (numeric)       |
| field<number  | Less-than (numeric)          |

Examples:

```bash
--filter title=fitness
--filter model~gpt total_messages>5
--filter title~log model=gpt-4 custom=Yes
```

These are automatically converted to JMESPath internally.  
To use raw JMESPath, supply a quoted expression starting with `items[`.

---

## 📋 --filter help Behavior

If `--filter help` is passed (or filter fails), rehash will print:

```
──────────────────────────── Filter Help - rehash v0.2.2-dev ─────────────────────────────

Supported Fields:
  id, title, created_at, model, custom,
  total_messages, attachments, first_message, last_message

Operators:
  =     → exact match
  ~     → contains/substring match
  > <   → numeric comparisons

Examples:
  --filter title=fitness
  --filter title~log model=gpt-4
  --filter total_messages>5
  --filter "items[?custom=='Yes']"   # JMESPath mode

Notes:
- Use --filter help to view this screen at any time.
- Strings are case-sensitive.
- Triggered automatically when no matches are found.

────────────────────────────────────────────────────────────────────────────────────────────
```

---

## 🔎 Conversation ID Matching

When using `-c <ID>`:

- A **full ID match** is tried first.
- If not found, then **partial prefix** is accepted *only if unique*.
- If multiple partial matches are found:
  - rehash prints a table of `ID` and `Title`
  - User is prompted to rerun with a longer ID match

---

## 🖼️ Terminal Output

Every run must start with:

- Script name
- Version
- UTC timestamp (ISO8601)
- Full CLI invocation

Example:

```
─────────────────────────────── rehash v0.2.2-dev ────────────────────────────────
Timestamp: 2025-05-09T17:52:42Z  
Command Line: ./rehash archive.zip -l full csv --filter title~fitness  
No conversations matched filter: title~fitness  
👉 Tip: Use --filter help
──────────────────────────────────────────────────────────────────────────────────
```

---

## 📝 Output Naming Standards

| Export Type | Filename Format |
|-------------|-----------------|
| List CSV | `conversation_list.csv` |
| List Tab | `conversation_list.txt` |
| Conversation JSON | `conversation_<ID>.json` |
| Conversation YAML | `conversation_<ID>.yaml` |

---

## ✅ Status

This specification is **under active development** as `rehash_requirements.v0.2.2-dev.md`.  
All changes follow patch protocol from `v0.1.6-REV2`.  
Versions `v0.2.0` and `v0.2.1` are skipped intentionally.

---
