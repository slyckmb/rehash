# rehash.v0.2.3-dev.full.py

import argparse
import os
import sys
import json
import zipfile
import tempfile
import shutil
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def extract_zip(zip_path):
    tmpdir = tempfile.mkdtemp(prefix="rehash_")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(tmpdir)
    return tmpdir

def load_conversations(folder):
    convo_path = os.path.join(folder, "conversations.json")
    if not os.path.exists(convo_path):
        return []
    with open(convo_path, "r", encoding="utf-8") as f:
        return json.load(f)

def print_banner():
    print("────────────────────────────────────────────────── rehash v0.2.3-dev ──────────────────────────────────────────────────")

def main():
    print_banner()

    parser = argparse.ArgumentParser(description="rehash v0.2.3-dev - Parse and export ChatGPT conversations")
    parser.add_argument("path", nargs="?", default=".", help="Path to exported zip or extracted folder (defaults to current directory).")
    parser.add_argument("--list", "-l", action="store_true", help="List conversations (trim mode by default).")
    parser.add_argument("--conversation", "-c", type=str, help="Export a single conversation by ID.")
    parser.add_argument("--messages", "-m", action="store_true", help="Extract messages matching title/date filters")
    parser.add_argument("--date", "-d", type=str, help="Filter messages by local date (YYYY-MM-DD, America/New_York)")
    parser.add_argument("--filter", "-f", nargs="+", help="Apply filters by metadata fields (e.g. title~foo model=gpt-4)")
    parser.add_argument("--scan", "-s", action="store_true", help="Scan archive and print metadata summary")
    parser.add_argument("--help", "-h", action="help", help="Show usage and examples")
    args = parser.parse_args()

    source_path = args.path
    if not os.path.exists(source_path):
        print(f"ERROR: Input path does not exist: {source_path}")
        return

    if os.path.isfile(source_path) and zipfile.is_zipfile(source_path):
        source_path = extract_zip(source_path)
        print(f"Extracted zip to: {source_path}")

    conversations = load_conversations(source_path)

    if args.scan:
        print(f"📦 Archive Path: {source_path}")
        if not conversations:
            print("⚠️ No conversations found.")
            return
        titles = [c.get("title") or "(untitled)" for c in conversations]
        timestamps = [c.get("create_time") for c in conversations if "create_time" in c]
        timestamps = [datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(ZoneInfo("America/New_York")) for ts in timestamps if ts]

        min_time = min(timestamps).isoformat() if timestamps else "?"
        max_time = max(timestamps).isoformat() if timestamps else "?"

        print(f"📅 Date Range (ET): {min_time} → {max_time}")
        print(f"💬 Conversations: {len(conversations)}")

        convo_fields = set()
        msg_fields = set()
        for convo in conversations:
            convo_fields.update(convo.keys())
            if "mapping" in convo:
                for entry in convo["mapping"].values():
                    msg = entry.get("message")
                    if msg:
                        msg_fields.update(msg.keys())

        print(f"🧪 Conversation Fields: {', '.join(sorted(convo_fields))}")
        print(f"🧪 Message Fields: {', '.join(sorted(msg_fields))}")
        return

    if args.messages:
        if not args.date:
            print("⚠️  --date is required with --messages")
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
                if not msg or "create_time" not in msg:
                    continue
                ts_utc = datetime.fromtimestamp(msg["create_time"], tz=timezone.utc)
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
                import re
                safe_title = re.sub(r"[^a-zA-Z0-9_]+", "", title)
                outname = f"message_{safe_title}_{args.date}.json"
                with open(outname, "w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2, ensure_ascii=False)
                print(f"💾 Exported {len(messages)} messages → {outname}")
                outfiles += 1

        if outfiles == 0:
            print(f"⚠️  No messages matched {args.date} in any conversation.")
        return

if __name__ == "__main__":
    main()
