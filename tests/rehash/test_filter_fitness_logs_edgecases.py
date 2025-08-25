# tests/rehash/test_filter_fitness_logs_edgecases.py

import pytest
from rehash.filter_fitness_logs import is_fitness_conversation


def test_empty_title():
    """Conversations with no title should not match."""
    conv = {"title": "", "mapping": {}}
    assert not is_fitness_conversation(conv)


def test_message_none():
    """Mapping entry with message=None should skip safely."""
    conv = {"title": "random", "mapping": {"1": {"message": None}}}
    assert not is_fitness_conversation(conv)


def test_message_wrong_types():
    """Non-dict message values should be skipped without error."""
    for bad in ["not a dict", 12345, [1, 2, 3]]:
        conv = {"title": "random", "mapping": {"1": {"message": bad}}}
        assert not is_fitness_conversation(conv)


def test_message_empty_dict():
    """Message dict without author/content should not match."""
    conv = {"title": "random", "mapping": {"1": {"message": {}}}}
    assert not is_fitness_conversation(conv)


def test_message_non_assistant_role():
    """Message from user role should not match, even if content has keywords."""
    conv = {
        "title": "random",
        "mapping": {
            "1": {
                "message": {
                    "author": {"role": "user"},
                    "content": {"parts": ["workout log"]},
                }
            }
        },
    }
    assert not is_fitness_conversation(conv)


def test_message_dict_with_no_parts():
    """Assistant message with empty parts list should not match."""
    conv = {
        "title": "random",
        "mapping": {
            "1": {
                "message": {
                    "author": {"role": "assistant"},
                    "content": {"parts": []},
                }
            }
        },
    }
    assert not is_fitness_conversation(conv)


def test_message_dict_with_nonstring_parts():
    """Assistant message with non-string parts should be ignored."""
    conv = {
        "title": "random",
        "mapping": {
            "1": {
                "message": {
                    "author": {"role": "assistant"},
                    "content": {"parts": [{"foo": "bar"}]},
                }
            }
        },
    }
    assert not is_fitness_conversation(conv)


def test_message_dict_non_matching_text():
    """Assistant message with text but no fitness keywords should not match."""
    conv = {
        "title": "random",
        "mapping": {
            "1": {
                "message": {
                    "author": {"role": "assistant"},
                    "content": {"parts": ["hello world"]},
                }
            }
        }
    }
    assert not is_fitness_conversation(conv)
