#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_export.py

📦 JSON ingestion + loader for ChatGPT exports

Loads conversations.json from within a standard ChatGPT `.zip` archive
and parses it into a validated Python list of conversations.

Author: Jake AI 🥷
"""

import zipfile
import json
from pathlib import Path
from typing import List, Dict, Any, Union

def extract_conversations_json(zip_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Extract and parse `conversations.json` from a ChatGPT export ZIP.

    Parameters:
        zip_path (str): Path to the .zip archive from ChatGPT export.

    Returns:
        List[Dict[str, Any]]: Parsed list of conversation objects.

    Raises:
        FileNotFoundError: If conversations.json not found in archive.
        zipfile.BadZipFile: If the zip is invalid.
        json.JSONDecodeError: If the JSON is malformed.
        TypeError: If the top-level JSON is not a list.
    """
    zip_path = Path(zip_path)

    if not zip_path.exists() or not zipfile.is_zipfile(zip_path):
        raise zipfile.BadZipFile(f"Invalid ZIP archive: {zip_path}")

    with zipfile.ZipFile(zip_path, 'r') as archive:
        try:
            with archive.open("conversations.json") as f:
                data = json.load(f)
        except KeyError:
            raise FileNotFoundError("conversations.json not found in ZIP.")

    if not isinstance(data, list):
        raise TypeError("Expected a list of conversations in JSON.")

    return data
