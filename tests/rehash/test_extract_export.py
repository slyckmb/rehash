import pytest
import json
from zipfile import ZipFile, BadZipFile
from pathlib import Path
from rehash.extract_export import extract_conversations_json, extract_export

FIXTURE_DIR = Path("tests/rehash/fixtures")


def test_valid_export():
    conversations = extract_conversations_json(FIXTURE_DIR / "valid_export.zip")
    assert isinstance(conversations, list)
    assert len(conversations) > 0


def test_invalid_zip(tmp_path):
    bad_zip = tmp_path / "invalid.zip"
    bad_zip.write_text("not a zip")

    with pytest.raises(BadZipFile):
        extract_conversations_json(bad_zip)


def test_missing_conversations_json(tmp_path):
    zip_path = tmp_path / "no_convos.zip"
    with ZipFile(zip_path, "w") as zf:
        zf.writestr("random.json", "{}")

    with pytest.raises(FileNotFoundError, match="conversations.json not found"):
        extract_conversations_json(zip_path)

def test_extract_export_happy_path(tmp_path):
    from rehash.extract_export import extract_export
    import zipfile
    import json

    zip_path = tmp_path / "happy.zip"
    data = [{"title": "Test", "create_time": 1234567890, "messages": [], "source": "chatgpt"}]

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("conversations.json", json.dumps(data))

    result = extract_export(zip_path)
    assert isinstance(result, list)
    assert result[0]["title"] == "Test"

def test_extract_export_wrong_extension(tmp_path):
    from rehash.extract_export import extract_export

    txt_file = tmp_path / "not_a_zip.txt"
    txt_file.write_text("not really a zip")

    with pytest.raises(BadZipFile, match="Not a .zip file"):
        extract_export(txt_file)

def test_extract_export_not_list_json(tmp_path):
    from rehash.extract_export import extract_export
    import zipfile
    import json

    zip_path = tmp_path / "bad_data.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("conversations.json", json.dumps({"not": "a list"}))

    with pytest.raises(TypeError, match="Expected top-level list"):
        extract_export(zip_path)
