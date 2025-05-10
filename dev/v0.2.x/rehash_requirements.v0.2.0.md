# 🛠️ rehash - Requirements Document (v0.2.0)

---

## 📦 Core Functional Requirements

- Operate on a ChatGPT export archive (`.zip`) or extracted folder.
- Load necessary `.json` files:
  - Load `conversations.json` primarily. (Other files will be addressed later.)
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
| `--filter <filter>` | Apply field-based filter to list output. |
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

---

## 📋 Available Filter Fields

(Supported in simplified and JMESPath form)

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

## 🧩 Filter Syntax (v0.2.0 update)

### Simplified Filters (preferred for CLI)

| Syntax | Meaning |
|--------|---------|
| `field=value` | Exact match |
| `field~text` | Substring/contains |
| `field>n` / `field<n` | Numeric comparison |

Examples:

```bash
--filter title=fitness
--filter title~log model~gpt custom=Yes
--filter total_messages>10
```

These are automatically translated into proper JMESPath.

### Full JMESPath (advanced users)

You may still supply raw expressions:

```bash
--filter "items[?contains(title, 'fitness')]"
--filter "items[?model=='gpt-4']"
```

If the filter string starts with `items[`, it is **not translated** and passed directly to `jmespath`.

---

## 📋 `--filter help` Behavior

If passed, `rehash` prints the following structured help block and exits:

```
──────────────────────────── Filter Help - rehash v0.2.0 ─────────────────────────────

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
- Fields are case-sensitive.
────────────────────────────────────────────────────────────────────────────────────
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
────────────────────────────────── rehash v0.2.0 ──────────────────────────────────
Timestamp: 2025-05-09T17:23:55Z
Command Line: ./rehash archive.zip -l full csv --filter title~fitness
────────────────────────────────────────────────────────────────────────────────────
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

This specification is **LOCKED** as `rehash_requirements.v0.2.0.md`.

It supersedes:

- `v0.1.4-REV1`
- `v0.1.6-REV2`

All builds from `rehash.py v0.2.0` forward must conform.

---
