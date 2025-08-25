#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emit_structured_json.py

📤 Emit individual JSON files from a structured conversation export list.
"""

import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
import re


def slugify(text: str, max_length: int = 48) -> str:
    """Sanitize a string to be filename-safe."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    return text[:max_length].strip("_")


def emit_conversations(conversations: List[Dict], output_dir: Path) -> List[Path]:
    """
    Emit structured JSON conversations to disk with safe, timestamped filenames.

    Args:
        conversations (List[Dict]): Parsed conversation objects.
        output_dir (Path): Where to write JSON files.

    Returns:
        List[Path]: List of output file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths = []

    for convo in conversations:
        ts = convo.get("create_time") or convo.get("timestamp") or "0"
        try:
            # ➕ Support ISO8601 parsing
            if isinstance(ts, str) and "T" in ts:
                ts = datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
            else:
                ts = float(ts)
        except Exception:
            raise ValueError(f"Invalid timestamp: {ts} in conversation: {convo.get('title', '[no title]')}")
        
        dt = datetime.fromtimestamp(ts)
        
        
        date_str = dt.strftime("%Y-%m-%d")

        title = convo.get("title", "untitled")
        slug = slugify(title)

        filename = f"{date_str}__{slug}.json"
        file_path = output_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(convo, f, ensure_ascii=False, indent=2)

        output_paths.append(file_path)

    return output_paths
