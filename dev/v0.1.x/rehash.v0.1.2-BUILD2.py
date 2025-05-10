#!/usr/bin/env python3
"""
rehash - ChatGPT Export Parser Tool
Version: v0.1.2-BUILD2
"""

# === Metadata ===
SCRIPT_NAME = "rehash"
SCRIPT_VERSION = "v0.1.2-BUILD2"

# === Imports ===
import os
import sys
import json
import yaml
import argparse
import tempfile
import shutil
import zipfile
import time
import jmespath
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# === Setup ===
console = Console()

# === Utility Functions ===

def extract_zip(zip_path):
    """Extracts a .zip file to a temp folder and returns the extracted folder path."""
    temp_dir = tempfile.mkdtemp(prefix="rehash_")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        console.print(f"[green]Extracted zip to:[/] {temp_dir}")
        return temp_dir
    except Exception as e:
        console.print(f"[red]ERROR extracting zip:[/] {e}")
        sys.exit(1)

def load_conversations(source_path):
    """Loads conversations.json and parses conversation objects."""
    conversations_file = None

    if os.path.isdir(source_path):
        possible_file = os.path.join(source_path, "conversations.json")
        if os.path.isfile(possible_file):
            conversations_file = possible_file
    elif os.path.isfile(source_path):
        if os.path.basename(source_path) == "conversations.json":
            conversations_file = source_path

    if not conversations_file or not os.path.isfile(conversations_file):
        return None

    try:
        with open(conversations_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        console.print(f"[red]ERROR loading JSON:[/] {e}")
        sys.exit(1)

    if not isinstance(data, list):
        console.print("[red]ERROR:[/] conversations.json is not a list of conversations.")
        sys.exit(1)

    enriched_convos = []
    for convo in data:
        enriched = {
            "id": convo.get("id", ""),
            "title": convo.get("title", "Untitled"),
            "created_at": format_timestamp(convo.get("create_time")),
            "first_message": get_first_message_time(convo),
            "last_message": get_last_message_time(convo),
            "model": convo.get("model_slug", "unknown"),
            "custom": "Yes" if convo.get("custom_gpt_id") else "No",
            "total_messages": count_messages(convo),
            "attachments": detect_attachments(convo),
            "raw": convo
        }
        enriched_convos.append(enriched)

    return enriched_convos

# === Helpers ===

def format_timestamp(unix_time):
    """Convert a unix timestamp to readable UTC string."""
    if not unix_time:
        return "-"
    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(unix_time))
    except Exception:
        return "-"

def count_messages(convo):
    """Count number of messages in a conversation."""
    try:
        return len([k for k in convo.get("mapping", {}).keys()])
    except Exception:
        return 0

def get_first_message_time(convo):
    """Estimate first message timestamp."""
    return format_timestamp(convo.get("create_time"))

def get_last_message_time(convo):
    """Estimate last message timestamp."""
    return format_timestamp(convo.get("update_time"))

def detect_attachments(convo):
    """Simple detector if any message content hints at a file upload."""
    try:
        mapping = convo.get("mapping", {})
        for msg in mapping.values():
            content = msg.get("message", {}).get("content", {})
            if isinstance(content, dict):
                parts = content.get("parts", [])
                for part in parts:
                    if isinstance(part, str) and "[" in part and "]" in part:
                        return "Yes"
        return "No"
    except Exception:
        return "No"

def filter_conversations(convos, filter_expr):
    """Apply jmespath filter if provided."""
    if not filter_expr:
        return convos
    try:
        results = jmespath.search(filter_expr, {"items": convos})
        if results is None:
            return []
        return results
    except Exception as e:
        console.print(f"[red]ERROR applying filter:[/] {e}")
        return convos

def print_convo_list(convos, mode="trim"):
    """Print conversation list in trim or full mode."""
    if not convos:
        console.print("[yellow]No conversations to display.[/]")
        return

    table = Table(show_lines=True)

    if mode == "full":
        columns = [
            ("ID", "id"),
            ("Title", "title"),
            ("Created At", "created_at"),
            ("First Message", "first_message"),
            ("Last Message", "last_message"),
            ("Model", "model"),
            ("Custom GPT?", "custom"),
            ("Total Messages", "total_messages"),
            ("Attachments?", "attachments")
        ]
    else:  # trim
        columns = [
            ("ID", "id"),
            ("Title", "title"),
            ("Created At", "created_at"),
            ("Model", "model")
        ]

    for col_title, _ in columns:
        table.add_column(col_title, style="cyan")

    for convo in convos:
        row = []
        for _, field in columns:
            row.append(str(convo.get(field, "-")))
        table.add_row(*row)

    console.print(table)

def export_convo_list(convos, mode="trim", file_type="csv"):
    """(Placeholder) Export list to file - Will be implemented later"""
    pass

def print_single_conversation(convo):
    """(Placeholder) Pretty print conversation - Will be implemented later"""
    pass

def export_single_conversation(convo, file_type="json"):
    """(Placeholder) Export single conversation - Will be implemented later"""
    pass

def bundle_assets(convo, source_folder, export_folder):
    """(Placeholder) Bundle external files if any - Will be implemented later"""
    pass

# === Main Execution Flow ===

def main():
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=f"{SCRIPT_NAME} {SCRIPT_VERSION} - Parse and export ChatGPT conversations",
        epilog="Example: rehash ./export.zip -l full csv --filter \"items[?model=='gpt-4']\""
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to exported zip or extracted folder (defaults to current directory)."
    )

    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List conversations (trim mode by default)."
    )
    parser.add_argument(
        "-c", "--conv",
        type=str,
        help="Export a single conversation by ID."
    )
    parser.add_argument(
        "modifiers",
        nargs="*",
        help="Modifiers for list/export (full, csv, tab, json, yaml, --filter jmespath)."
    )

    parser.add_argument(
        "--filter",
        type=str,
        help="Apply jmespath filter to conversations when listing."
    )

    args = parser.parse_args()

    console.rule(f"[bold green]{SCRIPT_NAME} {SCRIPT_VERSION}")

    if not args.list and not args.conv:
        console.print(f"[yellow]No operation specified. Showing help:[/]")
        parser.print_help()
        sys.exit(0)

    input_path = args.path
    if not os.path.exists(input_path):
        console.print(f"[red]ERROR:[/] Input path does not exist: {input_path}")
        sys.exit(1)

    temp_folder = None
    if os.path.isfile(input_path) and input_path.endswith(".zip"):
        temp_folder = extract_zip(input_path)
        data_folder = temp_folder
    else:
        data_folder = input_path

    conversations = load_conversations(data_folder)
    if conversations is None:
        console.print(f"[red]ERROR:[/] Unable to load conversations.")
        sys.exit(1)

    modifiers = [m.lower() for m in args.modifiers]

    if args.list:
        mode = "full" if "full" in modifiers else "trim"
        filtered_convos = filter_conversations(conversations, args.filter)
        print_convo_list(filtered_convos, mode=mode)

    elif args.conv:
        convo_id = args.conv
        convo = next((c for c in conversations if c["id"] == convo_id), None)
        if convo:
            file_type = "json" if "json" in modifiers else ("yaml" if "yaml" in modifiers else None)
            print_single_conversation(convo)
            if file_type:
                export_single_conversation(convo, file_type=file_type)
        else:
            console.print(f"[red]ERROR:[/] Conversation ID '{convo_id}' not found.")
            sys.exit(1)

    if temp_folder:
        shutil.rmtree(temp_folder)

    console.rule(f"[bold cyan]{SCRIPT_NAME} {SCRIPT_VERSION} - Done")

# === Entrypoint ===

if __name__ == "__main__":
    main()
