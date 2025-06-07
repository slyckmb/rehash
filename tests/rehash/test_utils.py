# tests/tools/rehash/test_utils.py

import pytest
from rehash.utils import (
    extract_timestamp_from_filename,
    sanitize_title,
    get_stem_without_prefix
)
from pathlib import Path


def test_extract_timestamp_valid():
    filename = "chat_2025-05-04_131045_title.md"
    ts = extract_timestamp_from_filename(filename)
    assert ts == "2025-05-04T13:10:45"


def test_extract_timestamp_invalid_format():
    filename = "not_a_valid_timestamp_file.md"
    ts = extract_timestamp_from_filename(filename)
    assert ts is None


def test_extract_timestamp_bad_date():
    filename = "chat_2025-13-99_250099_something.md"
    ts = extract_timestamp_from_filename(filename)
    assert ts is None


def test_sanitize_title():
    assert sanitize_title("My GPT Log: Monday") == "my-gpt-log-monday"
    assert sanitize_title("   🚀Launch Test!   ") == "launch-test"
    assert sanitize_title("A_B_C__") == "a-b-c"


def test_get_stem_without_prefix():
    assert get_stem_without_prefix(Path("chat_2025-05-04_131045_title.md")) == "2025-05-04_131045_title"
    assert get_stem_without_prefix(Path("2025-05-04_title.md")) == "2025-05-04_title"
