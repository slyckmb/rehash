#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rehash_json_loader.v0.3.0+fx1.py

🔧 JSON ingestion + loader for ChatGPT exports
"""

SCRIPT_VERSION = "v0.3.0+fx1"

def load_chatgpt_export(filepath):
    """Load raw JSON from ChatGPT export file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()
