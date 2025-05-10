### 🐞 rehash Anomaly Tracker

| ID   | Description                                                                                  | Rev Detected        | Rev Fixed           | Status          |
|------|----------------------------------------------------------------------------------------------|---------------------|---------------------|------------------|
| A001 | ❌ Chat output filename does not follow `chat_<id>_<title>_<model>.json/yaml`                | v0.2.5-dev+fx6       | _(pending)_         | 🔴 Still broken  |
| A002 | ❌ Diary mode missing terminal output for file written                                       | v0.2.5-dev+fx6       | _(pending)_         | 🔴 Still broken  |
| A003 | ❌ Diary table still labeled "Conversations" instead of "Chats"                              | v0.2.5-dev+fx6       | _(pending)_         | 🔴 Still broken  |
| A004 | ❌ Scan output still uses placeholder (`Models used: ?`)                                     | v0.2.5-dev+fx6       | _(pending)_         | 🔴 Still broken  |
| A005 | ❌ CLI echo + timestamp missing at script start                                              | v0.2.5-dev+fx5       | v0.2.5-dev+fx6       | ✅ Verified fixed |
| A006 | ❌ Banner revision not updated correctly                                                     | v0.2.5-dev+fx5       | v0.2.5-dev+fx6       | ✅ Verified fixed |
| A007 | ❌ `SCRIPT_VERSION` not DRY; duplicated or hardcoded                                         | v0.2.5-dev+fx5       | v0.2.5-dev+fx6       | ✅ Verified fixed |
| A008 | ❌ `--diary` with `-o json` created no output and gave no feedback                           | v0.2.5-dev+fx5       | v0.2.5-dev+fx6       | ✅ Verified fixed |
| A009 | ❌ `--list` logic not renamed to `--diary`; crash with AttributeError                        | v0.2.5-dev+fx2       | v0.2.5-dev+fx3       | ✅ Verified fixed |
| A010 | ❌ `--journal` logic crashed on missing message timestamps (NoneType)                        | v0.2.4-dev+fx1       | v0.2.4-dev+fx2       | ✅ Verified fixed |
| A011 | ❌ Output file naming inconsistent for `journal_`, still using `message_`                    | v0.2.4-dev+fx2       | v0.2.4-dev+fx3       | ✅ Verified fixed |

---

**Legend**:
- ✅ Verified fixed
- 🔴 Still broken
- 🆕 New in latest inspection
```
