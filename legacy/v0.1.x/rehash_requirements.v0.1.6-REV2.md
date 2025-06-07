# 🛠️ rehash - Requirements Document (v0.1.6-REV2 CLEAN)

---

## 📦 Core Functional Requirements

- Operate on a ChatGPT export archive (.zip) or extracted folder.
- Load necessary `.json` files:
  - Load `conversations.json` primarily. (Other files will be addressed later.)
  - Path can be either an extracted folder OR a .zip archive. (Auto-detect.)
- Support listing all conversations with optional filters and modifiers.
- Support exporting a single conversation by ID to JSON or YAML.
- Compress any external files linked by conversations into an archive if exporting.
- Output should always include:
  - Script name
  - Script version
  - Date/Time (UTC)
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
| `--filter "expression"` | Apply JMESPath filter to list output. |
| `-h`, `--help` | Show usage/help information. |

Modifiers (for use after the path and operation flag):

| Modifier | Meaning |
|:---|:---|
| `full` | Show full metadata columns when listing |
| `csv` | Export list to CSV file |
| `tab` | Export list to Tab-separated TXT file |
| `json` | Export conversation to JSON (default) |
| `yaml` | Export conversation to YAML |

---

## ⚙ CLI Usage Rules

- Path must come first. It can be a folder or a .zip archive. If omitted, defaults to current directory (.).
- Operation flag must follow path (`-l` or `-c`).
- Modifiers come after operation flag, space-separated.
- Flags must not be combined with modifiers (e.g., use `-l full`, not `-lfull`).
- Use `--filter help` to display full filtering field options and examples.

---

## 📋 Available Filter Fields

(For use with `--filter "jmespath"` expressions)

- id
- title
- created_at
- model
- custom
- total_messages
- attachments
- first_message
- last_message

Filtering only affects listing (`-l`), not single conversation exports (`-c`).

If you pass `--filter help`, a dedicated filter help page will be displayed, listing all filterable fields, examples, and tips.

---

## 🔎 Conversation ID Matching

- When using `-c <ID>`, partial ID matching is allowed:
  - Full ID match first.
  - Otherwise, partial prefix match if unique.
  - If multiple matches, rehash lists:
    - Conversation ID
    - Title
  - User must retry with a more specific ID.
- This improves usability with long UUID-based IDs.

---

## 🖼️ Terminal Output

- Header display every time script is run, including:
  - Script name
  - Script version
  - Full CLI command
  - UTC Date/Time stamp

Example:

```
────────────────────────────────── rehash v0.1.6 ──────────────────────────────────
Timestamp: 2025-04-28T22:41:00Z
Command Line: ./rehash testdata/ -l full csv
────────────────────────────────────────────────────────────────────────────────────
```

---

## 🧩 Filters - Detailed Behavior

If `--filter help` is passed:

- rehash must print a dedicated filter help screen like:

```
──────────────────────────── Filter Help - rehash v0.1.6 ─────────────────────────────

JMESPath Filtering Syntax:
- Conversations are under 'items[]' path.
- Examples:

  - id              → items[?id=='abc123']
  - title           → items[?contains(title, 'pasta')]
  - created_at      → items[?starts_with(created_at, '2024-03')]
  - model           → items[?model=='gpt-4']
  - custom          → items[?custom=='Yes']
  - total_messages  → items[?total_messages > `5`]
  - attachments     → items[?attachments=='Yes']

- Strings must be wrapped in double quotes.
- Numbers must be wrapped in backticks `` ` ``.

More info: https://jmespath.org/

────────────────────────────────────────────────────────────────────────────────────
```

---

## 📋 Status

| Version | Notes |
|:---|:---|
| v0.1.4-REV1 | Original locked version |
| v0.1.6-REV2 CLEAN | Path clarified, filter help, partial ID matching, timestamp output |

---

# 📜 rehash - Requirements Document (v0.1.6-REV2 CLEAN) - END

