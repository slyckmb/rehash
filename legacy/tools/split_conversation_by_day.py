#!/usr/bin/env python3
# split_conversations_by_day.py

import os
import sys
import json
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import re

# -- Utilities --

def slugify(title: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]+', '-', title.strip().lower()).strip('-')

def parse_args():
    parser = argparse.ArgumentParser(description="Split GPT conversation JSON(s) by day with timezone-aware timestamps.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=str, help="Path to a single conversation .json file")
    group.add_argument('--dir', type=str, help="Path to a directory of conversation .json files")
    group.add_argument('--all', action='store_true', help="Process all .json files in the current directory")
    parser.add_argument('--out', type=str, default='out', help="Output directory [default: ./out/]")
    return parser.parse_args()

def load_conversation(path: Path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to parse: {path} – {e}")
        return None

def ensure_output_dir(base: Path, day: str):
    target = base / day
    target.mkdir(parents=True, exist_ok=True)
    return target

def extract_daily_messages(convo, title, outdir):
    tz = ZoneInfo("America/New_York")
    messages = convo.get("mapping", {})
    slug = slugify(title)
    by_day = {}

    for obj in messages.values():
        msg = obj.get("message")
        if not msg or "create_time" not in msg or "content" not in msg:
            continue
        parts = msg["content"].get("parts", [])
        if not parts:
            continue
        dt = datetime.fromtimestamp(float(msg["create_time"]), tz=ZoneInfo("UTC")).astimezone(tz)
        day = dt.date().isoformat()
        by_day.setdefault(day, []).append({
            "timestamp": dt.isoformat(),
            "role": msg.get("author", {}).get("role", "unknown"),
            "content": parts
        })

    for day, msgs in by_day.items():
        day_dir = ensure_output_dir(outdir, day)
        fname = f"{day}__{slug}.json"
        with open(day_dir / fname, "w", encoding="utf-8") as f:
            json.dump({"date": day, "title": title, "slug": slug, "messages": msgs}, f, indent=2)

    print(f"[✓] Saved {len(by_day)} day-split file(s) for: {title}")

def process_file(file_path: Path, outdir: Path):
    convo = load_conversation(file_path)
    if not convo:
        return
    title = convo.get("title") or file_path.stem
    extract_daily_messages(convo, title, outdir)

def process_dir(dir_path: Path, outdir: Path):
    json_files = list(dir_path.glob("*.json"))
    for f in json_files:
        process_file(f, outdir)

# -- Entry Point --

def main():
    args = parse_args()
    outdir = Path(args.out)

    if args.file:
        process_file(Path(args.file), outdir)
    elif args.dir:
        process_dir(Path(args.dir), outdir)
    elif args.all:
        process_dir(Path("."), outdir)

if __name__ == "__main__":
    main()
