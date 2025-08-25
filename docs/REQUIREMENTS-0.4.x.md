# Rehash v0.4.x – Functional Requirements

This document specifies the functional requirements for the **Rehash v0.4.x** release.  
It is the baseline for release readiness review and must be satisfied before v0.4.0 can be tagged.

---

## 1. Core CLI

### Requirement
- The CLI **must provide a `parse-export` subcommand**:
  ```bash
  rehash parse-export <zip> --out <dir> [--fitness-only]
  ```
- It must:
  - Accept a ChatGPT (LLM) export `.zip` file as input.
  - Extract all conversations contained within.
  - Emit one JSON file per conversation into `<dir>`.
  - Exit with a non-zero status on error.

### Status
✅ Implemented (`src/rehash/cli.py`)

---

## 2. JSON Emission

### Requirement
- Conversations must be emitted in structured JSON format with the following keys:
  - `title` (string)
  - `create_time` (ISO 8601 timestamp)
  - `mapping` (dictionary of messages with role + content)
- Each conversation must be written to a distinct file in `<out>`:
  - File naming must include the conversation’s creation timestamp and slugified title.
- The tool must create the output directory if it does not exist.

### Status
✅ Implemented (`src/rehash/emit_structured_json.py`)

---

## 3. Fitness Filtering

### Requirement
- CLI must support `--fitness-only` flag to restrict output to fitness-related conversations.
- Filtering must detect conversations by:
  - **Title keywords**:  
    `phd`, `fitness`, `workout`, `log`, `training`, `progress`
  - **Assistant message patterns**:  
    `workout log`, `training update`, `pull.*fitness`, `reconstruct.*log`, `summary of workout`
- Conversations are included if they match **either** title or message criteria.

### Status
✅ Implemented (`src/rehash/filter_fitness_logs.py`)

---

## 4. Error Handling

### Requirement
The CLI must handle and report errors gracefully:
- Missing input path → `FileNotFoundError`
- Invalid zip → `zipfile.BadZipFile`
- Malformed export data → `ValueError` or `TypeError`

The tool must:
- Print a clear ❌ error message to `stderr`.
- Exit with code `1`.

### Status
✅ Implemented (`src/rehash/cli.py`)

---

## 5. Development & QA

### Requirement
- Codebase must follow linting and typing rules:
  - `ruff` (style & import hygiene)
  - `mypy` (type checking)
- Tests must be provided with `pytest`:
  - Coverage must include CLI, extraction, emission, and filtering.
  - Coverage reports must be generatable in both terminal and HTML formats.

### Status
✅ Implemented (`tests/`, `htmlcov/`, `pyproject.toml`)

---

## 6. Packaging

### Requirement
- `rehash` must be installable via `pip`:
  - Must define project metadata in `pyproject.toml`.
  - Must declare Python requirement: `>=3.9`.
- Versioning must follow semantic versioning:
  - Current prerelease: `0.4.0a0`.

### Status
✅ Implemented (`pyproject.toml`, `src/rehash/__version__.py`)

---

## 7. Extensibility (Optional / Deferred)

### Requirement (future)
- Fitness filter should support user-supplied keywords via:
  - CLI flag (`--fitness-keywords`), or
  - Config file (`~/.rehash/config.yaml`), or
  - Environment variable (`REHASH_FITNESS_KEYWORDS`).

### Status
❌ Not yet implemented.  
🔮 Proposed for v0.5.x.

---

# ✅ Release Readiness – v0.4.0

- [x] Core CLI implemented and working.
- [x] JSON emission correct and structured.
- [x] Fitness filter functional and verified.
- [x] Error handling robust.
- [x] Tests + coverage in place.
- [x] Packaging and versioning aligned.
- [ ] Optional extensibility deferred.

**Conclusion:**  
The **0.4.x baseline requirements are satisfied**.  
The code is ready for release as **v0.4.0** once documentation and minor polish are complete.
