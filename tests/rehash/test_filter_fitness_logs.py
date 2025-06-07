import pytest
from rehash.filter_fitness_logs import (
    is_fitness_title,
    is_fitness_conversation,
    filter_fitness_conversations,
)

def test_is_fitness_title_match():
    assert is_fitness_title("PHD Progress Log")
    assert is_fitness_title("Workout Log")
    assert not is_fitness_title("Vacation Planning")

def test_is_fitness_conversation_title_only():
    convo = {"title": "Fitness log - week 3", "mapping": {}}
    assert is_fitness_conversation(convo)

def test_is_fitness_conversation_message_match():
    convo = {
        "title": "Chat",
        "mapping": {
            "abc": {
                "message": {
                    "author": {"role": "assistant"},
                    "content": {"parts": ["Here is your workout log summary."]},
                }
            }
        },
    }
    assert is_fitness_conversation(convo)

def test_filter_fitness_conversations_mixed():
    convos = [
        {"title": "Vacation Planning", "mapping": {}},
        {
            "title": "Chat",
            "mapping": {
                "abc": {
                    "message": {
                        "author": {"role": "assistant"},
                        "content": {"parts": ["training update for strength"]},
                    }
                }
            },
        },
    ]
    filtered = filter_fitness_conversations(convos)
    assert len(filtered) == 1
    assert "training" in filtered[0]["mapping"]["abc"]["message"]["content"]["parts"][0]
