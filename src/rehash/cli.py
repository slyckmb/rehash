#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py

🎯 Rehash CLI entrypoint
"""

import argparse
from pathlib import Path
from rehash.extract_export import extract_conversations_json
from rehash.emit_structured_json import emit_conversations
from rehash.filter_fitness_logs import filter_fitness_conversations

def parse_export(args):
    print(f"📦 Loading export: {args.input}")
    conversations = extract_conversations_json(args.input)
    print(f"🧠 Total conversations: {len(conversations)}")

    if args.fitness_only:
        conversations = filter_fitness_conversations(conversations)
        print(f"🏋️ Filtered fitness conversations: {len(conversations)}")

    out_paths = emit_conversations(conversations, Path(args.out))
    print(f"✅ Exported: {len(out_paths)} files ➤ {args.out}")

def main():
    parser = argparse.ArgumentParser(description="Rehash CLI Tool")
    sub = parser.add_subparsers(dest="command")

    # Subcommand: parse-export
    px = sub.add_parser("parse-export", help="Parse a ChatGPT export ZIP")
    px.add_argument("input", help="Path to export.zip")
    px.add_argument("--out", default="out/", help="Output dir [default: ./out/]")
    px.add_argument("--fitness-only", action="store_true", help="Filter for fitness convos only")
    px.set_defaults(func=parse_export)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
