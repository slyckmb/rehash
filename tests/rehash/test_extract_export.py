import pytest
from rehash.extract_export import extract_conversations_json
from zipfile import BadZipFile
from pathlib import Path
import json

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_valid_export():
    zip_path = FIXTURE_DIR / "valid_export.zip"
    conversations = extract_conversations_json(zip_path)
    assert isinstance(conversations, list)
    assert "title" in conversations[0]


def test_invalid_zip():
    with pytest.raises(BadZipFile):
        extract_conversations_json(FIXTURE_DIR / "invalid.zip")


def test_missing_conversations_file(tmp_path):
    # Create a fake zip with no conversations.json
    zip_path = tmp_path / "missing_conversations.zip"
    from zipfile import ZipFile
    with ZipFile(zip_path, 'w') as zf:
        zf.writestr("readme.txt", "this zip has no json")

    with pytest.raises(FileNotFoundError):
        extract_conversations_json(zip_path)


def test_malformed_json(tmp_path):
    zip_path = tmp_path / "malformed_json.zip"
    from zipfile import ZipFile
    with ZipFile(zip_path, 'w') as zf:
        zf.writestr("conversations.json", "NOT JSON")

    with pytest.raises(json.JSONDecodeError):
        extract_conversations_json(zip_path)
