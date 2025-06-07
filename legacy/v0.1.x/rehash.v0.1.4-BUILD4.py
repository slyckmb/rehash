#!/usr/bin/env python3
"""
rehash - ChatGPT Export Parser Tool
Version: v0.1.4-BUILD4
"""

# === Metadata ===
SCRIPT_NAME = "rehash"
SCRIPT_VERSION = "v0.1.4-BUILD4"

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
import csv
import jmespath
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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
    return format_timestamp(convo.get("create_time"))

def get_last_message_time(convo):
    return format_timestamp(convo.get("update_time"))

def detect_attachments(convo):
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
    else:
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
    if not convos:
        console.print("[yellow]No conversations to export.[/]")
        return

    fields = ["id", "title", "created_at", "model"] if mode == "trim" else [
        "id", "title", "created_at", "first_message", "last_message",
        "model", "custom", "total_messages", "attachments"
    ]

    filename = f"conversation_list.{file_type if file_type != 'tab' else 'txt'}"
    delimiter = "," if file_type == "csv" else "\t"

    try:
        with open(filename, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f, delimiter=delimiter)
            writer.writerow(fields)
            for convo in convos:
                writer.writerow([convo.get(field, "-") for field in fields])
        console.print(f"[green]Exported conversation list to:[/] {filename}")
    except Exception as e:
        console.print(f"[red]ERROR writing export file:[/] {e}")

def print_single_conversation(convo):
    if not convo or "raw" not in convo:
        console.print("[yellow]No conversation found.[/]")
        return

    panel = Panel(
        f"[bold]Title:[/] {convo['title']}\n"
        f"[bold]Model:[/] {convo['model']}\n"
        f"[bold]Custom GPT:[/] {convo['custom']}\n"
        f"[bold]Messages:[/] {convo['total_messages']}",
        title=f"[green]{convo['id']}[/green]",
        expand=False
    )
    console.print(panel)

def export_single_conversation(convo, file_type="json"):
    if not convo or "raw" not in convo:
        console.print("[yellow]No conversation to export.[/]")
        return

    filename = f"conversation_{convo['id']}.{file_type}"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            if file_type == "json":
                json.dump(convo["raw"], f, indent=2)
            elif file_type == "yaml":
                yaml.dump(convo["raw"], f, sort_keys=False, allow_unicode=True)
        console.print(f"[green]Exported conversation to:[/] {filename}")
    except Exception as e:
        console.print(f"[red]ERROR writing conversation export:[/] {e}")

def bundle_assets(convo, source_folder, export_folder):
    pass  # Placeholder for future asset packaging

# === Main Execution Flow ===

def main():
    parser = argparse.ArgumentParser(
        prog=SCRIPT_NAME,
        description=f"{SCRIPT_NAME} {SCRIPT_VERSION} - Parse and export ChatGPT conversations",
        epilog="""
USAGE RULES:

- Path argument must be the first positional (folder or zip file).
- If omitted, defaults to current directory `.`.
- Then specify -l or -c.
- Then space-separated modifiers (full, csv, tab, json, yaml).
- Do NOT combine flags and modifiers (use "-l full", NOT "-lfull").

Examples:

  rehash ./export.zip -l full csv --filter "items[?model=='gpt-4']"
  rehash ./archive/ -c abc123 json
"""
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
        "--filter",
        type=str,
        help="Apply jmespath filter to conversations when listing."
    )
    parser.add_argument(
        "modifiers",
        nargs="*",
        help="Modifiers for list/export (full, csv, tab, json, yaml)."
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
        output_file = "csv" if "csv" in modifiers else ("tab" if "tab" in modifiers else None)
        filtered_convos = filter_conversations(conversations, args.filter)
        print_convo_list(filtered_convos, mode=mode)
        if output_file:
            export_convo_list(filtered_convos, mode=mode, file_type=output_file)

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