#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌀 Rehash v0.3.0 — Rescue, Rediscover, Rehydrate ChatGPT Conversations
"""

import argparse
import sys
import os
from datetime import datetime

VERSION = "0.3.0"

def banner():
    print(f"""
  🌀 Rehash v{VERSION}
  ---------------------
  Revive, Rescue, Rediscover your ChatGPT history
  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """)

def parse_args():
    parser = argparse.ArgumentParser(
        description="🌀 Rehash v0.3.0 — ChatGPT Rescue Tool"
    )

    parser.add_argument("json_file", help="Path to ChatGPT JSON export")

    parser.add_argument("--diary", action="store_true",
                        help="📔 List all conversations in diary-style table")

    parser.add_argument("--chat", type=str, metavar="ID",
                        help="🧠 Show full conversation by ID")

    parser.add_argument("--journal", type=str, metavar="DATE",
                        help="📆 Export conversation(s) by date (YYYY-MM-DD)")

    parser.add_argument("--scan", action="store_true",
                        help="📊 Print dataset summary")

    parser.add_argument("--export", action="store_true",
                        help="💾 Export output to outputs/")

    parser.add_argument("--version", action="version",
                        version=f"rehash v{VERSION}",
                        help="🔖 Show version and exit")

    return parser.parse_args()

def main():
    args = parse_args()
    banner()

    if not os.path.exists(args.json_file):
        print(f"❌ File not found: {args.json_file}")
        sys.exit(1)

    # Placeholder command dispatch
    if args.diary:
        print("📔 [diary] List of all conversations — TODO")

    elif args.chat:
        print(f"🧠 [chat] Conversation ID: {args.chat} — TODO")

    elif args.journal:
        print(f"📆 [journal] Conversations on {args.journal} — TODO")

    elif args.scan:
        print("📊 [scan] Dataset summary — TODO")

    else:
        print("ℹ️ No actionable command given. Use -h for help.")

if __name__ == "__main__":
    main()
