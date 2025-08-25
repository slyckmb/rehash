import json
from zipfile import ZipFile, BadZipFile
from pathlib import Path
from typing import Union, List, Dict, Any

def extract_export(zip_path: Union[str, Path]) -> List[Dict[str, Any]]:
    zip_path = Path(zip_path)

    if not zip_path.exists() or not zip_path.is_file():
        raise FileNotFoundError(f"Zip path does not exist: {zip_path}")
    if not zip_path.name.endswith(".zip"):
        raise BadZipFile(f"Not a .zip file: {zip_path}")

    with ZipFile(zip_path, 'r') as zf:
        try:
            with zf.open('conversations.json') as f:
                data = json.load(f)
        except KeyError:
            raise FileNotFoundError("conversations.json not found in ZIP.")

    if not isinstance(data, list):
        raise TypeError("Expected top-level list in conversations.json")

    return data

# 👇 Legacy alias for backward compatibility
extract_conversations_json = extract_export
