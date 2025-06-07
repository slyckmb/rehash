from zipfile import ZipFile
from pathlib import Path
import json

FIXTURE_DIR = Path(__file__).parent
zip_path = FIXTURE_DIR / "valid_export.zip"

conversation_sample = [
    {
        "title": "phd fitness week 1",
        "create_time": "2025-05-06T10:30:00Z",
        "mapping": {
            "1": {"message": {"author": {"role": "user"}, "content": {"parts": ["Morning log..."]}}},
            "2": {"message": {"author": {"role": "assistant"}, "content": {"parts": ["Great job!"]}}},
        }
    }
]

with ZipFile(zip_path, 'w') as zf:
    zf.writestr("conversations.json", json.dumps(conversation_sample, indent=2))

print(f"✅ Created fixture: {zip_path}")
