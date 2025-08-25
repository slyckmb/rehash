#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cli.py

🎯 Rehash CLI entrypoint
"""

import os
import sys
import zipfile
import argparse
from pathlib import Path
from rehash.emit_structured_json import emit_conversations
from rehash.filter_fitness_logs import filter_fitness_conversations
from rehash.extract_export import extract_export as default_extract_fn

# Global hookable extractor for tests
extract_fn = default_extract_fn


def parse_export_handler(args):
    zip_path = Path(args.zip)

    # 🧪 Testing hook
    extract = (
        (lambda _: {"not": "a list"})
        if os.environ.get("REHASH_BROKEN_EXTRACT") == "1"
        else extract_fn
    )

    print(f"📦 Loading export: {zip_path}")
    conversations = extract(zip_path)

    if not isinstance(conversations, list):
        raise TypeError(f"Expected list of conversations, got {type(conversations).__name__}")
    
    print(f"🧠 Total conversations: {len(conversations)}")

    if args.fitness_only:
        conversations = filter_fitness_conversations(conversations)
        print(f"🏋️ Filtered fitness conversations: {len(conversations)}")

    out_paths = emit_conversations(conversations, Path(args.out))
    print(f"✅ Exported: {len(out_paths)} files ➤ {args.out}")


def _add_subparsers(parser: argparse.ArgumentParser) -> None:
    """Attach subcommands to the CLI parser."""
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_cmd = subparsers.add_parser("parse-export", help="Parse a ChatGPT export ZIP")
    export_cmd.add_argument("zip", type=str, help="Path to ChatGPT ZIP export")
    export_cmd.add_argument("--out", required=True, help="Where to write structured JSON")
    export_cmd.add_argument("--fitness-only", action="store_true", help="Filter to fitness logs only")
    export_cmd.set_defaults(func=parse_export_handler)


def get_parser() -> argparse.ArgumentParser:
    """Create CLI parser for entrypoint and tests."""
    parser = argparse.ArgumentParser(description="Rehash CLI Tool")
    _add_subparsers(parser)
    return parser


def main(args=None):
    parser = get_parser()
    try:
        parsed_args = parser.parse_args(args)
        func = getattr(parsed_args, "func", None)
        if callable(func):
            func(parsed_args)
        else:
            parser.print_help()
            return
    except (FileNotFoundError, zipfile.BadZipFile, ValueError, TypeError) as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


def run_as_main(args=None):
    """Entry point wrapper for in-process test coverage of __main__."""
    main(args)


if __name__ == "__main__":
    run_as_main()
