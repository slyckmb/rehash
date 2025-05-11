#!/usr/bin/env python3
# dev/v0.2.x/rehash.v0.2.6-dev.py
# Extract, list, and filter ChatGPT conversations
# Author: Operator + GPT Jake
# Created: 2024-04-28
# Updated: 2025-05-10
#
# Supported CLI:
#   --diary / -d       Show chat summary table
#   --chat / -c        Export single chat
#   --journal / -j     Export messages by date/filter
#   --scan / -s        Scan archive metadata
#   --filter / -f      Filter chats by title/id
#   --date             Message date filter (for --journal)
#   --output / -o      Output format (json/yaml/csv/tab)
#   --help / -h        Show usage

"""
rehash - ChatGPT Export Parser Tool
Version: v0.2.6-dev
"""

import os, sys, argparse, json, zipfile
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import re

# === Metadata ===
SCRIPT_NAME = "rehash"
SCRIPT_VERSION = "v0.2.6-dev"

# === UX Helpers ===
def banner():
    print(f"{'─'*45} {SCRIPT_NAME} {SCRIPT_VERSION} {'─'*45}")
    print(f"{SCRIPT_NAME} {SCRIPT_VERSION} @ {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print()

def emoji(msg):
    return f"💾 {msg}"

# === Core Loaders ===
def extract_zip(zip_path):
    temp_dir = tempfile.mkdtemp(prefix="rehash_")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    return temp_dir

def find_input_file(path):
    path = Path(path)
    if path.is_file() and path.suffix == ".zip":
        return extract_zip(path)
    if path.is_file() and path.name == "conversations.json":
        return str(path.parent)
    if path.is_dir():
        files = list(path.glob("*.zip")) + list(path.glob("conversations.json"))
        if len(files) == 1:
            return extract_zip(files[0]) if files[0].suffix == ".zip" else str(files[0].parent)
        elif len(files) > 1:
            print("⚠️  Multiple input files found. Please specify one explicitly.")
            sys.exit(1)
    print("❌ ERROR: No valid input file found.")
    sys.exit(1)

def load_conversations(folder):
    file_path = Path(folder) / "conversations.json"
    if not file_path.exists():
        print("❌ conversations.json not found in input folder.")
        sys.exit(1)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to parse conversations.json: {e}")
        sys.exit(1)

# === Filters ===
def apply_filter(convos, flt):
    if not flt: return convos
    key, op, val = None, None, None
    if "~" in flt:
        key, val = flt.split("~", 1)
        op = "contains"
    elif "=" in flt:
        key, val = flt.split("=", 1)
        op = "equals"
    else:
        print(f"❌ Invalid filter: {flt}")
        return []
    key = key.strip().lower()
    val = val.strip().lower()
    out = []
    for c in convos:
        field = str(c.get(key, "") or "").lower()
        if (op == "contains" and val in field) or (op == "equals" and val == field):
            out.append(c)
    return out

def safe_title(title):
    return re.sub(r'[^\w\-]+', '_', title.strip().lower())[:40]

# === Date Helpers ===
def format_date(ts): return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
def short_date(ts): return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")

# === Diary Mode ===
def handle_diary(convos, args):
    from rich.console import Console
    from rich.table import Table

    filtered = apply_filter(convos, args.filter)
    table = Table(title="📘 Chat Diary" + (f" — Filter: {args.filter}" if args.filter else ""))
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title")
    table.add_column("Created At", justify="right")
    table.add_column("Model", justify="center")
    for c in filtered:
        table.add_row(
            c["id"][:6],
            c.get("title", "Untitled"),
            format_date(c.get("create_time", 0)),
            c.get("model_slug", "?") or "?"
        )
    Console().print(table)
    if args.output in ("json", "yaml"):
        fname = f"diary_user_START-END_exported-{datetime.now().strftime('%Y%m%d-%H%M%S')}.{args.output}"
        with open(fname, "w", encoding="utf-8") as f:
            (json if args.output == "json" else yaml).dump(filtered, f, indent=2)
        print(emoji(f"Exported diary → {fname}"))

# === Chat Mode ===
def handle_chat(convos, args):
    matches = [c for c in convos if args.chat in c["id"]]
    if len(matches) > 1:
        print("⚠️ Multiple chats match this ID:")
        for c in matches:
            print(f"  {c['id']} — {c.get('title', '')}")
        return
    if not matches:
        print("❌ No match for chat ID.")
        return
    chat = matches[0]
    print(f"╭─ {chat['id']} ─╮")
    print(f"│ Title: {chat.get('title','?')}")
    print(f"│ Model: {chat.get('model_slug','?')}")
    print(f"│ Custom GPT: {'Yes' if chat.get('custom_gpt_id') else 'No'}")
    print(f"│ Messages: {len(chat.get('mapping',{}))}")
    print("╰" + "─" * 50 + "╯")
    if args.output in ("json", "yaml"):
        date = short_date(chat.get("create_time", 0))
        fname = f"chat_{chat['id']}_{safe_title(chat.get('title','untitled'))}_{date}.{args.output}"
        with open(fname, "w", encoding="utf-8") as f:
            (json if args.output == "json" else yaml).dump(chat, f, indent=2)
        print(emoji(f"Exported chat → {fname}"))

# === Journal Mode ===
def handle_journal(convos, args):
    from collections import defaultdict
    date_match = args.date
    filtered = apply_filter(convos, args.filter)
    for c in filtered:
        msgs = []
        mapping = c.get("mapping", {})
        for k in mapping:
            msg = mapping[k].get("message")
            if not msg or "create_time" not in mapping[k]:
                continue
            msg_ts = short_date(mapping[k]["create_time"])
            if msg_ts == date_match:
                msgs.append(msg)
        if not msgs: continue
        title = safe_title(c.get("title", "untitled"))
        fname = f"journal_{title}_{date_match}.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(msgs, f, indent=2)
        print(emoji(f"Exported {len(msgs)} messages → {fname}"))

# === Scan Mode ===
def handle_scan(convos, args):
    ids = [c["id"] for c in convos]
    titles = [c.get("title", "") for c in convos]
    dates = [c.get("create_time", 0) for c in convos if c.get("create_time")]
    print(f"📦 Archive contains {len(convos)} chats.")
    if dates:
        print(f"🗓️ Date range: {short_date(min(dates))} → {short_date(max(dates))}")
    print(f"🧠 Sample IDs: {ids[:3]}")
    print(f"📝 Sample Titles: {titles[:3]}")

# === Entry Point ===
def main():
    parser = argparse.ArgumentParser(description="rehash - ChatGPT conversation export parser")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--diary", "-d", action="store_true")
    parser.add_argument("--chat", "-c")
    parser.add_argument("--journal", "-j", action="store_true")
    parser.add_argument("--filter", "-f")
    parser.add_argument("--date")
    parser.add_argument("--output", "-o", choices=["json", "yaml", "csv", "tab"])
    parser.add_argument("--scan", "-s", action="store_true")
    parser.add_argument("--help", "-h", action="help")
    args = parser.parse_args()

    banner()

    if not any([args.diary, args.chat, args.journal, args.scan]):
        print("No operation specified. Use -d, -c, -j, or -s.")
        return

    folder = find_input_file(args.path)
    convos = load_conversations(folder)

    if args.diary:
        handle_diary(convos, args)
    elif args.chat:
        handle_chat(convos, args)
    elif args.journal and args.date:
        handle_journal(convos, args)
    elif args.scan:
        handle_scan(convos, args)

if __name__ == "__main__":
    try:
        import yaml
    except:
        yaml = None
    main()
