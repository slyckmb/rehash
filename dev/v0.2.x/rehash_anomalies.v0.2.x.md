# 📋 rehash Anomalies Log (v0.2.x)
_Last sync: fx6 vs. v0.2.5-dev+fx2_

| #  | Area          | Description                                                                                 | Detected In          | Fixed In | Status           |
|----|---------------|---------------------------------------------------------------------------------------------|----------------------|----------|------------------|
| 1  | CLI Echo      | No CLI Args or timestamp shown at script start                                             | v0.2.5-dev+fx4       | ❌       | ❗ Still broken   |
| 2  | Version Echo  | Banner still says `v0.2.5-dev+fx4` when fx5/fx6 active                                     | v0.2.5-dev+fx5       | ❌       | ❗ Still broken   |
| 3  | DRY Violation | Version string hardcoded in multiple places; should be DRY from one variable               | v0.2.5-dev+fx5       | ❌       | ❗ Still broken   |
| 4  | Scan Output   | Table header still says “Conversations” instead of “Chats”                                 | v0.2.5-dev+fx4       | ❌       | ❗ Still broken   |
| 5  | --diary Output| `--diary -o json` produces no export file, no terminal confirmation                         | v0.2.5-dev+fx4       | ❌       | ❗ Still broken   |
| 6  | --journal File| Output still uses `message_...` prefix, not new `journal_...`                              | v0.2.5-dev+fx3       | ❌       | ❗ Still broken   |
| 7  | Journal UX    | Journal export does not display applied filters or total message count                     | v0.2.5-dev+fx3       | ❌       | ❗ Still broken   |
| 8  | Output Naming | `diary_*` filenames not used in diary export                                               | v0.2.5-dev+fx5       | ❌       | ❗ Still broken   |
| 9  | Scan Coverage | `--scan` output does not show: username, export date, date range, file count               | v0.2.5-dev+fx4       | ❌       | ❗ Still broken   |
| 10 | Journal Filter| Journal incorrectly exports messages from convos that fail the title filter                | v0.2.5-dev+fx2       | ✅ fx3   | ✅ Verified Fixed |
| 11 | JSON Load Err | Fails to load valid test JSON with messages but no timestamps                              | v0.2.5-dev+fx6       | ❌       | ❗ New            |
| 12 | Model Field   | Table shows “Model” column always empty — either hide or show “?” placeholder              | v0.2.5-dev+fx3       | ❌       | ❗ Still broken   |
| 13 | Conversation  | Exported chat filename doesn’t include title or create date per new filename pattern       | v0.2.5-dev+fx3       | ❌       | ❗ Still broken   |
| 14 | Archive Match | If multiple JSON/ZIP found in folder, ambiguous input message not shown                    | v0.2.5-dev+fx4       | ✅ fx5   | ✅ Verified Fixed |
| 15 | --scan Header | Scan header banner doesn’t match final UX mockup                                           | v0.2.5-dev+fx4       | ❌       | ❗ Still broken   |
| 16 | Chat Summary  | Chat panel has empty `Model: ?` but no clarifying hint or UX logic                         | v0.2.5-dev+fx2       | ❌       | ❗ Still broken   |
| 17 | Chat Create   | Chat filenames do not reflect `chat_<id>_<title>_<date>.json` format                       | v0.2.5-dev+fx3       | ❌       | ❗ Still broken   |
| 18 | Filter Help   | No usage or flag guidance for `--filter` in scan or echo summary                           | v0.2.5-dev+fx2       | ❌       | ❗ Still broken   |
| 19 | CLI Aliases   | CLI aliases like `-j` / `--journal` work, but `--messages` still appears in summary logic  | v0.2.5-dev+fx4       | ❌       | ❗ Still broken   |

> Total Tracked: 19  
> ✅ Verified Fixed: 2  
> ❗ Still Broken: 17
