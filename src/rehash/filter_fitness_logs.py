#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
filter_fitness_logs.py

🧠 Logic to filter ChatGPT conversations based on fitness relevance.

Heuristics include:
- Title keywords (phd, fitness, log, workout)
- Assistant message content scanning (optional)
"""

import re
from typing import List, Dict


FITNESS_TITLE_PATTERNS = [
    r"\bphd\b",
    r"\bfitness\b",
    r"\bworkout\b",
    r"\blog\b",
    r"\btraining\b",
    r"\bprogress\b",
]

FITNESS_MESSAGE_PATTERNS = [
    r"(?i)workout log",
    r"training update",
    r"pull.*fitness",
    r"reconstruct.*log",
    r"summary of workout",
]


def is_fitness_title(title: str) -> bool:
    """Returns True if title suggests it's fitness-related."""
    title = title.lower()
    return any(re.search(p, title) for p in FITNESS_TITLE_PATTERNS)


def is_fitness_conversation(conversation: Dict) -> bool:
    """
    Check if conversation appears to be fitness/workout related.

    Uses:
    - Title keyword match
    - Assistant message content match (optional)

    Args:
        conversation (Dict): A ChatGPT conversation object

    Returns:
        bool: True if fitness-related
    """
    title = conversation.get("title", "").lower()
    if is_fitness_title(title):
        return True

    for message in conversation.get("mapping", {}).values():
        if (
            isinstance(message, dict)
            and message.get("message")
            and message["message"].get("author", {}).get("role") == "assistant"
        ):
            content = message["message"].get("content", {}).get("parts", [""])[0]
            if any(re.search(p, content, re.IGNORECASE) for p in FITNESS_MESSAGE_PATTERNS):
                return True

    return False


def filter_fitness_conversations(conversations: List[Dict]) -> List[Dict]:
    """Filter only fitness-relevant conversations from export list."""
    return [conv for conv in conversations if is_fitness_conversation(conv)]
