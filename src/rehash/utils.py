#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils.py

🧠 Utilities for rehash toolchain:
- Filename parsing
- ISO timestamp extraction
- Title sanitization
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional


def extract_timestamp_from_filename(filename: str) -> Optional[str]:
    """
    Extract ISO 8601 timestamp from a filename like:
    chat_2025-05-04_131045_title.md

    Returns:
        str or None: '2025-05-04T13:10:45' or None if not matched
    """
    match = re.search(r"(\d{4}-\d{2}-\d{2})_(\d{6})", filename)
    if not match:
        return None

    date_str, time_str = match.groups()
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H%M%S")
        return dt.isoformat()
    except ValueError:
        return None


def sanitize_title(title: str) -> str:
    """
    Replace unsafe characters and normalize for filenames.

    Examples:
        "My PHD Log: Monday" → "my-phd-log-monday"
    """
    title = title.strip().lower()
    title = re.sub(r"[^a-z0-9]+", "-", title)
    return title.strip("-")


def get_stem_without_prefix(path: Path) -> str:
    """
    Remove 'chat_' prefix from a Path stem if present.
    """
    name = path.stem
    return name[5:] if name.startswith("chat_") else name
