#!/usr/bin/env python3

SCRIPT_VERSION = "v0.3.0-dev"

import argparse
from rehash_json_loader import load_chatgpt_export, SCRIPT_VERSION as PARSER_VERSION

def main():
    print(f"🌀 rehash.py {SCRIPT_VERSION}")
    
    parser = argparse.ArgumentParser(
        description="Rehash – Rescue and rehydrate your ChatGPT conversations."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # `parse` command
    parse_parser = subparsers.add_parser("parse", help="Parse a ChatGPT export .json file")
    parse_parser.add_argument("filepath", help="Path to exported chat JSON file")

    args = parser.parse_args()

    if args.command == "parse":
        data = load_chatgpt_export(args.filepath)
        print(f"✅ Parsed {len(data['conversations'])} conversations")

if __name__ == "__main__":
    main()
