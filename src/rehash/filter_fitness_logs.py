# src/rehash/filter_fitness_logs.py

import re

FITNESS_TITLE_PATTERNS = [
    r"\bphd\b",
    r"\bfitness\b",
    r"\bworkout\b",
    r"\blog\b",
    r"\btraining\b",
    r"\bprogress\b",
    r"\bperfit\b",
]

FITNESS_MESSAGE_PATTERNS = [
    r"(?i)workout log",
    r"training update",
    r"pull.*fitness",
    r"reconstruct.*log",
    r"summary of workout",
]


def is_fitness_title(title: str) -> bool:
    """Check if title matches fitness-related keywords."""
    if not title:
        return False
    return any(re.search(p, title, re.IGNORECASE) for p in FITNESS_TITLE_PATTERNS)


def is_fitness_conversation(conversation: dict) -> bool:
    """Check if a conversation is fitness-related by title or assistant messages."""
    # Title check
    if is_fitness_title(conversation.get("title", "")):
        return True

    # Message content check
    mapping = conversation.get("mapping", {})
    for msg in mapping.values():
        if not isinstance(msg, dict):
            continue
        message = msg.get("message")
        if not isinstance(message, dict):  # ✅ guard against None or wrong type
            continue
        if message.get("author", {}).get("role") != "assistant":
            continue

        parts = message.get("content", {}).get("parts", [])
        if not parts:
            continue

        # Extract first part, coerce to string safely
        content = parts[0]
        if not isinstance(content, str):
            content = str(content)

        if any(re.search(p, content, re.IGNORECASE) for p in FITNESS_MESSAGE_PATTERNS):
            return True

    return False


def filter_fitness_conversations(conversations: list[dict]) -> list[dict]:
    """Return only fitness-related conversations from list."""
    return [conv for conv in conversations if is_fitness_conversation(conv)]
