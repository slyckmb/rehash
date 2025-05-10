# 🛠️ rehash - Requirements Document (v0.2.1)

---

## 📦 Core Functional Requirements

(unchanged from v0.2.0)

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

(unchanged except for minor filter clause addition)

- Modifiers must not be attached to flags (e.g., `-lfull` ❌).
- The script will **echo all CLA**, version, and UTC timestamp at start.
- If no operation flag is provided, usage/help is shown.
- `--filter help` prints all available filterable fields and examples.
- If a filter is applied and **returns no results**, rehash will show a fallback tip:

```
No conversations matched filter: title~fitness
👉 Tip: Use `--filter help` to view valid filter fields and examples.
```

---

## 📋 --filter help Behavior

(unchanged from v0.2.0 except reflected in help output and fallback messaging)

---

## 📋 Status

This specification is **LOCKED** as `rehash_requirements.v0.2.1.md`.

It supersedes:

- `v0.2.0`
- ⚠️ Only one soft request (fallback printing on no filter results) was not added in `v0.2.0` — this version addresses it.

---

# 📜 rehash - Requirements Document (v0.2.1) - END
