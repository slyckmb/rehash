# 💾 REHYDRATION — rehash Tool Dev
**Timestamp:** 2025-05-10 05:08:54  
**Context:** Restore Jake state for `rehash` CLI tool development at end of `v0.2.5-dev+fx6`

---

## 🧠 ACTIVE CONTEXT SNAPSHOT

### 🔢 Version
- Canonical Requirements: `rehash_requirements.v0.2.5-dev.md`
- Current Codebase: `rehash.v0.2.5-dev+fx6.py`
- Next expected version: `v0.2.6-dev` (clean baseline)

---

## 📂 Core Components

### 🧾 Requirements File
- Most recent: `rehash_requirements.v0.2.5-dev.md`
- Stored canonical rules, CLI UX spec, banner behaviors, filenames

### 🧠 Script Versioning
```python
SCRIPT_VERSION = "v0.2.5-dev+fx6"
```
- DRY applied
- Displayed in banner and help
- Used in filenames

### 🖥️ Main CLI Modes (as of v0.2.5)
| Flag         | Purpose                      |
|--------------|-------------------------------|
| `--diary`    | List all chats from archive   |
| `--chat ID`  | Export a single chat          |
| `--journal`  | Export filtered messages      |
| `--scan`     | Show metadata from archive    |
| `--filter`   | Metadata filter (e.g. title~) |
| `--date`     | Message filtering date        |
| `--output`   | Output format (json/yaml/tab/csv) |

---

## 💬 Outstanding Issues to Recheck in 0.2.6
| ID | Description |
|----|-------------|
| 1️⃣ | 🕒 Banner CLI timestamp and full CLI echo must always appear |
| 2️⃣ | Banner version must always reflect latest `SCRIPT_VERSION` |
| 3️⃣ | `--diary` still shows "Conversations" instead of "Chats" |
| 4️⃣ | JSON output from `--diary -o json` fails silently or doesn’t write |
| 5️⃣ | Journal filename format not updated (`journal_...`) |
| 6️⃣ | `chat_` files should include created date |
| 7️⃣ | `scan` output format doesn't follow markdown box or UX spec |

---

## 📁 Sample Archive Used for Dev
Filename: `023b5429cc33e...dae2dad5bbfc4a4aa589abea46d5b116.zip`  
Alias: `data/diary_sample.zip`

---

## 📜 Notes
- No use of `jmespath` going forward
- Terminal UX prioritized over backend complexity
- Filename format guides: `diary_...`, `chat_...`, `journal_...`
- DRY versioning in all scripts
