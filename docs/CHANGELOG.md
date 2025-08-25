```markdown
# Changelog

All notable changes to **rehash** will be documented in this file.  
This project follows [Semantic Versioning](https://semver.org/).

---

## [0.4.0] – 2025-08-25
### Added
- New **CLI interface** via `rehash parse-export`
  - Parses full ChatGPT exports (`export.zip`)
  - Supports `--out <dir>` to control output destination
  - Supports `--fitness-only` to filter for fitness/training conversations
  - Reports totals: “Total conversations” vs “Fitness conversations exported”
- Extensible **fitness keyword matcher** in `filter_fitness_logs.py`
  - Configurable keyword set (workout, gym, lifting, cardio, training, etc.)
  - Defensive guards for malformed export entries
- Comprehensive **unit + integration tests**
  - 50+ tests, ~99% coverage with branch checks
  - Edge cases covered (empty messages, wrong types, missing parts, wrong role)
- Documentation
  - `README.md` with usage examples
  - `docs/REQUIREMENTS-0.4.x.md` with formal requirements
  - This changelog

### Changed
- CLI now exits with **non-zero code** on missing/corrupt export
- Refactored codebase under `src/rehash/`
  - `extract_export.py` enforces safe extraction
  - `emit_structured_json.py` outputs ISO8601 timestamps
  - `cli.py` now prints structured status and errors
- Makefile targets aligned with modern dev workflow (`make lint`, `make test`, `make coverage`, etc.)

### Removed
- Old scattered scripts replaced by unified `rehash` CLI
- Redundant test cases consolidated

---

## [0.3.x]
- Early development builds
- Basic parsing logic without filtering
- No formal CLI, limited documentation

---

## [0.2.x]
- Initial experiments with parsing ChatGPT exports
- Manual scripts only, no packaging

---

## [0.1.x]
- Project setup, stubs, and proof of concept
```
