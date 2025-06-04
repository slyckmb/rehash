#!/usr/bin/env python3

import os
import sys
import csv
import json
import tempfile
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from subprocess import check_output

# CONFIG
DATA_DIR = "./data"
REHASH = "release/v0.1.6/rehash.py"
OUT_DIR = "./out"
KEYWORD = sys.argv[1] if len(sys.argv) > 1 else None
TZ = ZoneInfo("America/New_York")

if not KEYWORD:
    print("[!] Usage: python extract_gpt_by_day.py <keyword>")
    sys.exit(1)

# Find latest ZIP
zips = sorted(Path(DATA_DIR).glob("*.zip"), key=os.path.getmtime, reverse=True)
if not zips:
    print("[!] No ZIP exports found in ./data")
    sys.exit(1)

zip_path = zips[0]
print(f"[*] Using ZIP: {zip_path}")

# Run rehash list output to temp CSV
with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_csv:
    cmd = [
        "python", REHASH,
        str(zip_path),
        "-l", "csv",
        "--filter", f"items[?contains(title, '{KEYWORD}')]"
    ]
    output = check_output(cmd).decode("utf-8")
    tmp_csv.write(output)
    tmp_csv.flush()
    tmp_csv_path = tmp_csv.name

# Parse CSV with proper quoting
with open(tmp_csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

if not rows:
    print("[!] No conversations matched.")
    sys.exit(0)

print(f"[+] {len(rows)} chat(s) matched.\n")

for row in rows:
    convo_id = row.get("id", "").strip()
    title = row.get("title", "").strip() or "untitled"
    slug = "".join(c if c.isalnum() else "-" for c in title.lower()).strip("-")

    if not convo_id:
        print(f"[!] Skipping row with missing ID: {row}")
        continue

    out_path = Path(OUT_DIR) / slug
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"[→] Extracting: '{title}' ({convo_id}) → {out_path}")

    convo_json = check_output([
        "python", REHASH,
        str(zip_path),
        "-c", convo_id,
        "json"
    ]).decode("utf-8")

    convo = json.loads(convo_json)
    messages = convo.get("mapping", {})

    # Group messages by Eastern-local calendar day
    day_buckets = {}
    for msg in messages.values():
        data = msg.get("message", {})
        parts = data.get("content", {}).get("parts")
        ts = data.get("create_time")
        if not ts or not parts:
            continue
        try:
            utc_dt = datetime.fromtimestamp(float(ts), tz=ZoneInfo("UTC"))
            local_day = utc_dt.astimezone(TZ).date().isoformat()
        except Exception:
            continue

        day_buckets.setdefault(local_day, []).append({
            "author": data.get("author", {}).get("role", "unknown"),
            "timestamp": utc_dt.isoformat(),
            "content": parts
        })

    # Write to file: one JSON per local day
    for day, msgs in day_buckets.items():
        file = out_path / f"{day}.json"
        with open(file, "w") as f:
            json.dump({
                "title": title,
                "date": day,
                "messages": msgs
            }, f, indent=2)
        print(f"    [+] {day} → {file.name} ({len(msgs)} messages)")

print(f"\n[✓] All output written to: {OUT_DIR}/")

