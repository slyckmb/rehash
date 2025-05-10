#!/usr/bin/env python3
# rehash.v0.2.5-dev.py
# Extract, list, and filter ChatGPT conversations
# Author: Operator + GPT Jake
# Created: 2024-04-28
# Updated: 2025-05-09
#
# Supported CLI:
#   --diary / -d           List conversations
#   --chat / -c   Export one conversation
#   --journal / -j       Extract messages by title/date
#   --scan / -s           Show archive metadata
#   --filter / -f         Apply filter expression
#   --date / -d           Date for messages
#   --output / -o         File format for exports
#   --help / -h           Show usage

"""
rehash - ChatGPT Export Parser Tool
Version: v0.2.5-dev
"""

# === Metadata ===
SCRIPT_NAME = "rehash"
SCRIPT_VERSION = "v0.2.5-dev"

# === Imports ===
import os
import sys
import json
import yaml
import argparse
import tempfile
import shutil
import zipfile
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import re

# === Utility Functions ===

def extract_zip(zip_path):
    tmpdir = tempfile.mkdtemp(prefix="rehash_")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(tmpdir)
    return tmpdir

def load_conversations(folder):
    path = os.path.join(folder, "conversations.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def filter_conversations(conversations, filter_expr):
    if not filter_expr:
        return conversations
    results = []
    if "=" in filter_expr:
        key, val = filter_expr.split("=", 1)
        for convo in conversations:
            if str(convo.get(key, "")).lower() == val.lower():
                results.append(convo)
    elif "~" in filter_expr:
        key, val = filter_expr.split("~", 1)
        for convo in conversations:
            if val.lower() in str(convo.get(key, "")).lower():
                results.append(convo)
    else:
        results = conversations
    return results

def print_convo_list(conversations, mode="trim"):
    from rich.table import Table
    from rich.console import Console
    table = Table(title="Conversations", show_lines=True)
    if mode == "trim":
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Created At")
        table.add_column("Model")
        for c in conversations:
            ts = c.get("create_time", 0)
            dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(ZoneInfo("America/New_York"))
            table.add_row(c.get("id", ""), c.get("title", ""), dt.strftime("%Y-%m-%d %H:%M:%S"), c.get("model", ""))
    else:
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Created At")
        table.add_column("First Message")
        table.add_column("Last Message")
        table.add_column("Model")
        table.add_column("Custom GPT?")
        table.add_column("Total Messages")
        table.add_column("Attachments?")
        for c in conversations:
            ts = c.get("create_time", 0)
            dt = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(ZoneInfo("America/New_York"))
            first = dt.strftime("%Y-%m-%d %H:%M:%S")
            last = datetime.fromtimestamp(c.get("update_time", ts), tz=timezone.utc).astimezone(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")
            model = c.get("model", "")
            custom = "Yes" if "custom" in model else "No"
            msg_count = len(c.get("mapping", {}))
            has_attach = any("file_ids" in m.get("message", {}).get("metadata", {}) for m in c.get("mapping", {}).values())
            table.add_row(c.get("id", ""), c.get("title", ""), dt.strftime("%Y-%m-%d %H:%M:%S"), first, last, model, custom, str(msg_count), "Yes" if has_attach else "No")
    from rich.console import Console
    Console().print(table)

def export_convo_list(conversations, mode="trim", file_type="csv"):
    if file_type == "csv":
        with open("conversation_list.csv", "w", encoding="utf-8") as f:
            f.write("id,title,created_at,model\n")
            for c in conversations:
                title = c.get("title", "").replace(",", " ")
                dt = datetime.fromtimestamp(c.get("create_time", 0), tz=timezone.utc).astimezone(ZoneInfo("America/New_York")).isoformat()
                f.write(f"{c.get('id','')},{title},{dt},{c.get('model','')}\n")
        print("Exported conversation list to: conversation_list.csv")

    elif file_type == "tab":
        with open("conversation_list.txt", "w", encoding="utf-8") as f:
            for c in conversations:
                f.write(f"{c.get('id')}\t{c.get('title')}\t{c.get('model')}\n")
        print("Exported conversation list to: conversation_list.txt")

def print_single_conversation(convo):
    from rich.panel import Panel
    from rich.console import Console
    title = convo.get("title", "Untitled")
    model = convo.get("model", "?")
    custom = "Yes" if "custom" in model else "No"
    msg_count = len(convo.get("mapping", {}))
    Console().print(Panel(f"Title: {title}\nModel: {model}\nCustom GPT: {custom}\nMessages: {msg_count}", title=convo.get("id", "?")))

def export_single_conversation(convo, file_type="json"):
    conv_id = convo.get("id", "unknown")
    if file_type == "yaml":
        with open(f"conversation_{conv_id}.yaml", "w", encoding="utf-8") as f:
            yaml.dump(convo, f, allow_unicode=True)
        print(f"Exported conversation to: conversation_{conv_id}.yaml")
    else:
        with open(f"conversation_{conv_id}.json", "w", encoding="utf-8") as f:
            json.dump(convo, f, indent=2, ensure_ascii=False)
        print(f"Exported conversation to: conversation_{conv_id}.json")

# === Main Execution Flow ===
def main():
    from rich.console import Console
    console = Console()

    parser = argparse.ArgumentParser(description="rehash - ChatGPT conversation export parser")
    parser.add_argument("path", nargs="?", default=".", help="Path to .zip or folder")
    parser.add_argument("--diary", "-d", action="store_true", help="List conversations")
    parser.add_argument("--chat", "-c", help="Export single conversation by ID (partial match allowed)")
    parser.add_argument("--journal", "-j", action="store_true", help="Export messages by title/date")
    parser.add_argument("--filter", "-f", help="Filter string (e.g. title~fitness)")
    parser.add_argument("--date", help="Date for message filtering (YYYY-MM-DD)")
    parser.add_argument("--output", "-o", choices=["json", "yaml", "csv", "tab"], help="Export format")
    parser.add_argument("--scan", "-s", action="store_true", help="Scan archive metadata")

    args = parser.parse_args()

    # Show header
    console.rule(f"[bold green]{SCRIPT_NAME} {SCRIPT_VERSION}")

    if not any([args.list, args.conversation, args.messages, args.scan]):
        console.print("No operation specified. Showing help:")
        parser.print_help()
        return

    # Handle ambiguous "."
    if args.path == ".":
        zips = [f for f in os.listdir(".") if f.endswith(".zip")]
        has_json = os.path.exists(os.path.join(".", "conversations.json"))
        if len(zips) + int(has_json) > 1:
            print("⚠️ Multiple possible inputs found in current directory. Please specify a file or folder.")
            return

    # Handle zip
    if os.path.isfile(args.path) and args.path.endswith(".zip"):
        tempdir = extract_zip(args.path)
        path = tempdir
    else:
        path = args.path

    conversations = load_conversations(path)
    if not conversations:
        print("ERROR: Unable to load conversations.")
        return

    if args.scan:
        ids = [c.get("id") for c in conversations]
        titles = [c.get("title") or "untitled" for c in conversations]
        models = sorted(set(c.get("model", "?") for c in conversations))
        print(f"Archive contains {len(conversations)} conversations.")
        print(f"Models used: {', '.join(models)}")
        print(f"Example IDs: {', '.join(ids[:3])}")
        return

    if args.list:
        filtered = filter_conversations(conversations, args.filter)
        mode = "full" if args.output in ("csv", "tab") else "trim"
        print_convo_list(filtered, mode=mode)
        if args.output in ("csv", "tab"):
            export_convo_list(filtered, mode=mode, file_type=args.output)
        return

    if args.conversation:
        matches = [c for c in conversations if c.get("id", "").startswith(args.conversation)]
        if not matches:
            print(f"❌ No conversation found with ID starting with: {args.conversation}")
            return
        elif len(matches) > 1:
            print(f"⚠️ Multiple matches found for ID: {args.conversation}")
            for c in matches:
                print(f"  {c.get('id')}: {c.get('title')}")
            return
        convo = matches[0]
        print_single_conversation(convo)
        if args.output:
            export_single_conversation(convo, file_type=args.output)
        return

    if args.messages:
        conversations = filter_conversations(conversations, args.filter)
        if not args.date:
            print("⚠️ --date is required with --journal")
            return
        try:
            date_obj = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"❌ Invalid date format: {args.date} (expected YYYY-MM-DD)")
            return
        outfiles = 0
        for convo in conversations:
            title = convo.get("title", "untitled").strip().replace(" ", "_")[:40]
            conv_id = convo.get("id", "unknown")
            messages = []
            mapping = convo.get("mapping", {})
            for node in mapping.values():
                msg = node.get("message")
                if not msg:
                    continue
                create_ts = msg.get("create_time")
                if not isinstance(create_ts, (int, float)):
                    continue
                ts_utc = datetime.fromtimestamp(create_ts, tz=timezone.utc)
                ts_et = ts_utc.astimezone(ZoneInfo("America/New_York"))
                if ts_et.date() != date_obj:
                    continue
                messages.append({
                    "message_id": msg.get("id"),
                    "sender": msg.get("author", {}).get("role"),
                    "timestamp_utc": ts_utc.isoformat(),
                    "timestamp_et": ts_et.isoformat(),
                    "content": msg.get("content", {}).get("parts", [""])[0],
                })
            if messages:
                output = {
                    "conversation_id": conv_id,
                    "conversation_title": title,
                    "date_filtered": args.date,
                    "messages": messages
                }
                safe_title = re.sub(r"[^a-zA-Z0-9_]+", "", title)
                ext = args.output or "json"
                outname = f"message_{safe_title}_{args.date}.{ext}"
                with open(outname, "w", encoding="utf-8") as f:
                    if ext == "yaml":
                        yaml.dump(output, f, allow_unicode=True)
                    else:
                        json.dump(output, f, indent=2, ensure_ascii=False)
                print(f"💾 Exported {len(messages)} messages → {outname}")
                outfiles += 1
        if outfiles == 0:
            print(f"⚠️  No messages matched {args.date} in any conversation.")

if __name__ == "__main__":
    main()
