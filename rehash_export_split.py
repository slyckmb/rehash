#!/usr/bin/env python3
# rehash_export_split.py v0.9.4

import os
import sys
import json
import argparse
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
import re
from zoneinfo import ZoneInfo
import csv

# ──────────────────────────────
# rehash_export_split.py v0.9.4
# GPT-integrated CLI tool for extracting & formatting GPT exports
# Guardrail Format 2.2.2 Compatible
# ──────────────────────────────

REHASH_PATH = "release/v0.1.6/rehash.py"
TMPDIR = Path("tmp")

def slugify(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.strip().lower()).strip('-')

def shortid(cid: str) -> str:
    return cid[:8]

def run_subprocess(cmd):
    print(f"[debug] run_subprocess: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"[!] Subprocess failed:\n{result.stdout}")
        return None
    return result.stdout

def extract_convo_list(data_path: str, filter_text: str) -> list[tuple[str, str]]:
    cmd = ["python", REHASH_PATH, data_path, "-l", "csv"]
    if filter_text:
        safe_filter = filter_text.replace("'", "\\'")
        jmes = f"items[?contains(title, '{safe_filter}')]"
        cmd += ["--filter", jmes]

    print(f"[>] Running: {' '.join(cmd)}")
    run_subprocess(cmd)

    csv_path = Path("conversation_list.csv")
    if not csv_path.exists():
        print("[!] rehash.py did not emit conversation_list.csv")
        return []

    convos = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            if "," in line and "-" in line:
                parts = line.strip().split(",")
                cid = parts[0].strip()
                title = parts[1].strip()
                convos.append((cid, title))

    return convos

def export_convo(data_path: str, cid: str) -> Path:
    print(f"[*] Exporting {cid} via rehash.py...")
    run_subprocess(["python", REHASH_PATH, data_path, "-c", cid, "json"])
    fname = f"conversation_{cid}.json"
    return Path(fname) if Path(fname).exists() else None

def convert_and_rename(original: Path, slug: str, cid: str) -> Path:
    TMPDIR.mkdir(exist_ok=True)
    newname = TMPDIR / f"conv_{slug}_{shortid(cid)}.json"
    shutil.move(str(original), newname)
    print(f"[✓] Moved → {newname}")
    return newname

def write_json(day, slug, title, msgs, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / f"{day}__{slug}.json", "w", encoding="utf-8") as f:
        json.dump({"date": day, "title": title, "slug": slug, "messages": msgs}, f, indent=2)

def write_md(day, slug, title, msgs, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / f"{day}__{slug}.md", "w", encoding="utf-8") as f:
        f.write(f"# Chat Log: {title}\n\n")
        for m in msgs:
            ts = m["timestamp"]
            role = m["role"]
            for p in m["content"]:
                f.write(f"### [{role.upper()} @ {ts}]\n{p.strip()}\n\n")

def write_csv(day, slug, title, msgs, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    with open(outdir / f"{day}__{slug}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "role", "content"])
        for m in msgs:
            ts = m["timestamp"]
            role = m["role"]
            for p in m["content"]:
                writer.writerow([ts, role, p.strip()])

def split_and_write(file: Path, sort: str, outbase: Path, formats: set):
    with open(file, "r", encoding="utf-8") as f:
        convo = json.load(f)

    title = convo.get("title", file.stem)
    slug = slugify(title)
    tz = ZoneInfo("America/New_York")
    messages = convo.get("mapping", {})
    grouped = {}

    for m in messages.values():
        msg = m.get("message")
        if not msg:
            continue
        parts = msg.get("content", {}).get("parts", [])
        ctime = msg.get("create_time")
        if not ctime or not parts:
            continue
        try:
            dt = datetime.fromtimestamp(float(ctime), tz=ZoneInfo("UTC")).astimezone(tz)
        except Exception as e:
            print(f"[!] Skipping message with invalid timestamp: {ctime}")
            continue
        day = dt.date().isoformat()
        grouped.setdefault(day, []).append({
            "timestamp": dt.isoformat(),
            "role": msg.get("author", {}).get("role", "unknown"),
            "content": parts
        })

    for day, msgs in grouped.items():
        top = outbase / (day if sort == "date" else slug)
        if "json" in formats:
            write_json(day, slug, title, msgs, top)
        if "md" in formats:
            write_md(day, slug, title, msgs, top)
        if "csv" in formats:
            write_csv(day, slug, title, msgs, top)
        print(f"[⇨] Split: {top}/... ({', '.join(formats)})")

def parse_args():
    parser = argparse.ArgumentParser(description="Extract and split GPT conversations from rehash export.")
    parser.add_argument("--data", required=True, help="Path to .zip export file")
    parser.add_argument("--filter", help="Optional title match filter (case-insensitive)")
    parser.add_argument("--out", default="out", help="Output directory for split .json files")
    parser.add_argument("--sort", choices=["date", "title"], default="date", help="Group by date or title")
    parser.add_argument("--keep", action="store_true", help="Retain tmp/ intermediate conversation files")
    parser.add_argument("--format", default="json", help="Comma-separated output formats: json,md,csv")
    return parser.parse_args()

def main():
    args = parse_args()
    print("\n──────────── rehash_export_split v0.9.4 [GPT-integrated] ────────────")
    print(f"[CLA] --data {args.data} --filter {args.filter or '(none)'} --sort {args.sort} --out {args.out} --format {args.format}\n")

    formats = set(f.strip().lower() for f in args.format.split(","))
    outbase = Path(args.out)
    TMPDIR.mkdir(exist_ok=True)
    outbase.mkdir(parents=True, exist_ok=True)

    convos = extract_convo_list(args.data, args.filter or "")
    if not convos:
        print("[!] No conversations found.")
        sys.exit(1)

    print(f"[+] {len(convos)} conversations matched.")
    for cid, title in convos:
        slug = slugify(title)
        exported = export_convo(args.data, cid)
        if not exported:
            print(f"[!] Skipped: {cid}")
            continue
        renamed = convert_and_rename(exported, slug, cid)
        split_and_write(renamed, args.sort, outbase, formats)

    if not args.keep:
        print("[🧹] Cleaning tmp/...")
        shutil.rmtree(TMPDIR)

    print(f"[✓] Done. Output in: {outbase}")

if __name__ == "__main__":
    main()
