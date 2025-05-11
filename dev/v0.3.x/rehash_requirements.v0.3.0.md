# rehash_requirements.v0.2.6.md
Version: v0.2.6  
Status: 🟢 Canonical  
Date: 2025-05-10  
Baseline: v0.2.5-dev+fx2  
Guardrails: v2.2.2

---

## 🚩 Summary of Changes from v0.2.5-dev+fx2

- Fixes ambiguity in `--diary` column requirements (model optional).
- Ensures `--journal` gracefully skips messages without `create_time`.

---

## 🎯 CLI Modes & Options

| Flag            | Alias | Description                                          |
|-----------------|-------|------------------------------------------------------|
| `--diary`       | `-d`  | Show table of all chats (default = trim)            |
| `--chat <ID>`   | `-c`  | Export one chat (full message tree)                 |
| `--journal`     | `-j`  | Export one or more message subsets (by date/filter) |
| `--filter`      | `-f`  | Metadata filter expression (e.g. `title~fitness`)   |
| `--date`        |       | Date for filtering messages (e.g. `2025-04-15`)     |
| `--output`      | `-o`  | Export format: `json`, `yaml`, `csv`, `tab`         |
| `--scan`        | `-s`  | Display archive metadata summary                    |
| `--help`        | `-h`  | Show usage                                           |

- `path` is always positional and must be first if present
- Default path = `.` (only works if exactly one usable file is found)

---

## 🗃️ Mode: `--diary` (was `--list`)

### ✅ Summary
Outputs a summary of all conversations (now called “Chats”).

### 🧾 Behavior
- Outputs diary table to terminal in trim mode by default
- Supports modifiers: `full`, `csv`, `tab`, `json`, `yaml`
- Always outputs to terminal, and optionally to a file if `-o` specified
- Must show filters and export filenames if any

### 📋 Required Fields in Table
- Must include: ID, Title, Created At
- Model column is optional; if shown, display "?" if model is unknown

---

## 📦 Mode: `--chat <ID>` (was `--conversation`)

### ✅ Summary
Outputs one full conversation tree.

### 🧾 Behavior
- Partial ID matching allowed
- If multiple matches: show table, allow user to rerun
- Always outputs to terminal
- Exports to `chat_<id>_<title>_<date>.json` (or `.yaml`) if `-o` given

---

## ✍️ Mode: `--journal` (was `--messages`)

### ✅ Summary
Exports subset of messages from chats based on date and optional filter.

### 🧾 Behavior
- Requires `--date` (YYYY-MM-DD)
- Optional `--filter` (e.g. `title~phd`)
- Multiple chats may match; each will export a separate JSON/YAML file
- Output filenames: `journal_<title>_<date>.json`
- CLI echo: `💾 Exported 22 messages → journal_title_2025-04-15.json`

### ⚠️ Edge Case Handling
- Only messages from the specified date are exported.
- Messages with no `create_time` must be excluded or flagged gracefully.

---

## 🛰️ Mode: `--scan`

### ✅ Summary
Shows quick archive metadata.

### 📋 Required Info
- Total chat count
- Export date (if available)
- Models used
- Chat date range (earliest to latest)
- Example titles and IDs

---

## 💡 Filter Syntax (`--filter`)

Supports simplified expressions only.

| Syntax Example         | Meaning                            |
|------------------------|------------------------------------|
| `title~phd`            | Title contains “phd”               |
| `id=abc123`            | ID exact match                     |
| `title~Weekly Update`  | Title includes that phrase         |

If invalid field provided, fail gracefully and print list of valid fields.

---

## 🧠 Output Filename Rules

| Type      | Format                                                      |
|-----------|-------------------------------------------------------------|
| Diary     | `diary_<user>_<start>-<end>_exported-<timestamp>.json`      |
| Chat      | `chat_<id>_<title>_<date>.json`                             |
| Journal   | `journal_<title>_<date>.json`                               |

---

## 🧾 CLI Output UX

### All Runs
- Always echo script name + version + timestamp
- Always echo parsed CLI flags at top

### Export Modes (`-c`, `-j`, `-d` with `-o`)
- Always echo each file written with emoji:
  - `💾 Exported 65 messages → journal_fitness_2025-04-15.json`

---

## ⚠️ Ambiguous Input Handling

| Command                  | Behavior                                                                 |
|--------------------------|--------------------------------------------------------------------------|
| `rehash`                 | ❌ Invalid — prints usage and exits                                       |
| `rehash .`               | ✅ Allowed **only if** one usable file is detected (`.zip` or `json`)     |
| `rehash archive.zip`     | ✅ Preferred — exact path provided                                        |
| `rehash folder/`         | ✅ Preferred — exact folder given                                         |
| `rehash .` with >1 files | ⚠️ Fails — prompts user to choose file explicitly                         |

---

## 🛠️ Other Notes & Policies

### 💾 File Types Supported
- `.zip` — exported ChatGPT archive
- Folder containing `conversations.json`
- Single `conversations.json` file

### 🔍 Message Processing
- Message date = `create_time` converted to local time (Eastern)
- Messages with no timestamp are excluded in `--journal` mode
- Messages are flattened per chat for filtering

### 🧪 Testing Guidance
- Minimum test file must include:
  - Chat with title
  - Valid timestamps
  - At least one assistant/user exchange
- Ensure edge cases like missing models, missing message dates, long IDs

---

## 📌 UX Notes

- Avoid nested or verbose output (UX simplicity is priority)
- Use clean emoji tagging for exports: 💾, ⚠️
- File naming must be intuitive and human-readable
- Avoid ambiguous shorthand (e.g. don’t abbreviate “conversation” to “conv”)

---

## ✅ Versioning & Development Practice

- All CLI-visible features must be reflected in the requirements doc
- Script version defined **once** (DRY) and echoed at runtime
- Fixes after canonical release are marked with `+fxN`
- New features bump minor version: `v0.2.x → v0.3.0-dev`
- Patch cycles must be documented in `rehash_anomalies.v0.2.x.md`

---

## ✅ Canonical Test Invocation Examples

```
# Full diary export to terminal (trim)
rehash archive.zip -d

# Full diary to JSON
rehash archive.zip -d -o json

# Export one chat by partial ID
rehash archive.zip -c abc123 -o yaml

# Export journal by date only
rehash archive.zip -j --date 2025-04-15

# Export journal by title match + date
rehash archive.zip -j --filter title~phd --date 2025-04-15 -o json

# Scan archive metadata
rehash archive.zip -s
```

---  
**End of Canonical Requirements v0.2.6**  
Filename: `dev/v0.2.x/rehash_requirements.v0.2.6.md`  
Status: 🔒 Locked & Approved  
```
