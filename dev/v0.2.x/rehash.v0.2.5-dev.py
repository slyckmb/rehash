#!/usr/bin/env python3
# rehash.v0.2.5-dev.py
# Extract, list, and filter ChatGPT conversations
# Author: Operator + GPT Jake
# Created: 2024-04-28
# Updated: 2025-05-09

"""
rehash - ChatGPT Export Parser Tool
Version: v0.2.5-dev
"""

# === Metadata ===
SCRIPT_NAME = "rehash"
SCRIPT_VERSION = "v0.2.5-dev"

import os
import sys
import json
import csv
import shutil
import zipfile
import argparse
import datetime
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime as dt, timezone
try:
    import yaml
except ImportError:
    yaml = None

# === Utilities ===
def extract_zip(zip_path: str) -> str:
    temp_dir = Path("/tmp") / f"rehash_{os.urandom(4).hex()}"
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(temp_dir)
    print(f"Extracted zip to: {temp_dir}")
    return str(temp_dir)

def load_conversations(path: str) -> List[Dict[str, Any]]:
    conv_path = Path(path)
    if conv_path.is_dir():
        conv_file = conv_path / "conversations.json"
    elif zipfile.is_zipfile(conv_path):
        path = extract_zip(conv_path)
        conv_file = Path(path) / "conversations.json"
    else:
        conv_file = conv_path

    if not conv_file.exists():
        raise FileNotFoundError("Unable to load conversations.")
    with open(conv_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_conversations(convs: List[Dict], filters: List[str]) -> List[Dict]:
    def matches(conv: Dict) -> bool:
        for f in filters:
            key, val = f.split("~", 1)
            if key == "title":
                if val.lower() not in conv.get("title", "").lower():
                    return False
        return True

    return [c for c in convs if matches(c)]

def to_slug(text: str) -> str:
    return ''.join(c if c.isalnum() else '_' for c in text.strip())[:40]

def fmt_time(ts: float) -> str:
    return dt.fromtimestamp(ts, tz=timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')

def fmt_date(ts: float) -> str:
    return dt.fromtimestamp(ts, tz=timezone.utc).astimezone().strftime('%Y-%m-%d')

def extract_messages_by_date(convs: List[Dict], filter_str: str, date: str) -> List[Dict]:
    matches = []
    for conv in filter_conversations(convs, [filter_str]):
        for m in conv.get("mapping", {}).values():
            msg = m.get("message", {})
            ts = msg.get("create_time")
            if ts:
                ts_et = dt.fromtimestamp(ts, tz=timezone.utc).astimezone()
                if ts_et.strftime('%Y-%m-%d') == date:
                    matches.append({
                        "conversation_title": conv.get("title", "unknown"),
                        "conversation_id": conv.get("id"),
                        "sender": msg.get("author", {}).get("role", "?"),
                        "timestamp_et": ts_et.strftime('%Y-%m-%d %H:%M:%S'),
                        "content": msg.get("content", {}).get("parts", [""])[0]
                    })
    return matches

# === Output Writers ===

def export_json(obj: Any, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def export_yaml(obj: Any, filename: str):
    if not yaml:
        print("YAML export requires PyYAML. Install with `pip install pyyaml`.")
        return
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(obj, f, sort_keys=False, allow_unicode=True)

def export_csv(rows: List[Dict], filename: str):
    if not rows:
        return
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def export_txt(rows: List[Dict], filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write("\t".join(str(v) for v in row.values()) + "\n")

# === Main ===

def main():
    parser = argparse.ArgumentParser(description="rehash - ChatGPT conversation export parser")
    parser.add_argument("path", nargs="?", default=".", help="Path to .zip or folder")
    parser.add_argument("--diary", "-d", action="store_true", help="List conversations")
    parser.add_argument("--chat", "-c", help="Export single conversation by ID (partial match allowed)")
    parser.add_argument("--journal", "-j", action="store_true", help="Export messages by title/date")
    parser.add_argument("--filter", "-f", help="Filter string (e.g. title~fitness)")
    parser.add_argument("--date", "-d", help="Date for message filtering (YYYY-MM-DD)")
    parser.add_argument("--output", "-o", choices=["json", "yaml", "csv", "tab"], help="Export format")
    parser.add_argument("--scan", "-s", action="store_true", help="Scan archive metadata")
    args = parser.parse_args()

    print(f"───────────────────────────────────────────────── {SCRIPT_NAME} {SCRIPT_VERSION} ──────────────────────────────────────────────────")

    try:
        convs = load_conversations(args.path)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    if args.scan:
        print(f"Archive contains {len(convs)} conversations.")
        ids = [c["id"] for c in convs[:3]]
        print("Example IDs:", ", ".join(ids))
        return

    if args.diary:
        rows = []
        for c in convs:
            rows.append({
                "ID": c.get("id", "")[:8],
                "Title": c.get("title", ""),
                "Created At": fmt_time(c.get("create_time", 0)),
                "Model": c.get("model", "?")
            })
        if args.output == "csv":
            export_csv(rows, "diary_conversations.csv")
        elif args.output == "tab":
            export_txt(rows, "diary_conversations.txt")
        else:
            for r in rows:
                print(r)
        return

    if args.chat:
        matches = [c for c in convs if args.chat in c.get("id", "")]
        if not matches:
            print("No matching conversation found.")
            return
        if len(matches) > 1:
            print("Multiple matches:")
            for c in matches:
                print(c["id"], ":", c.get("title", ""))
            return
        c = matches[0]
        slug = to_slug(c.get("title", "chat"))
        outname = f"chat_{slug}_{c['id'][:8]}.json"
        if args.output == "yaml":
            outname = outname.replace(".json", ".yaml")
            export_yaml(c, outname)
        else:
            export_json(c, outname)
        print(f"Exported conversation to: {outname}")
        return

    if args.journal:
        if not args.date or not args.filter:
            print("Date and filter required for journal export.")
            return
        messages = extract_messages_by_date(convs, args.filter, args.date)
        if not messages:
            print("No matching messages.")
            return
        ftag = args.filter.split("~")[0]
        slug = to_slug(messages[0].get("conversation_title", "journal"))
        outname = f"journal_{slug}_({ftag})[{len(messages)}]_{args.date}.json"
        export_json(messages, outname)
        print(f"Exported {len(messages)} messages → {outname}")

if __name__ == "__main__":
    main()
