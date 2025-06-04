#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rehash.v0.3.0+fx1.py

🔧 Main entry point CLI for rehash
"""

import argparse
from rehash_json_loader import load_chatgpt_export, SCRIPT_VERSION as PARSER_VERSION

SCRIPT_VERSION = "v0.3.0+fx1"

def parse_command(args):
    print(f"🔍 rehash JSON Parser v{SCRIPT_VERSION} (loader: {PARSER_VERSION})")
    content = load_chatgpt_export(args.input)
    print("📦 Loaded content length:", len(content))

def main():
    parser = argparse.ArgumentParser(description="Rehash CLI")
    subparsers = parser.add_subparsers(dest="command")

    parse_parser = subparsers.add_parser("parse", help="Parse a ChatGPT export")
    parse_parser.add_argument("input", help="Path to ChatGPT JSON export")
    parse_parser.set_defaults(func=parse_command)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
