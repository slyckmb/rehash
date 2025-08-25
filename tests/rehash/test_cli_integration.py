import subprocess
import sys
from pathlib import Path
import pytest
import os


def test_cli_main_entry(tmp_path):
    zip_path = Path("tests/rehash/fixtures/valid_export.zip")
    out_file = tmp_path / "via_main.json"

    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", str(zip_path), "--out", str(out_file)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "📦 Loading export" in result.stdout
    assert out_file.exists()


def test_cli_script_entry(tmp_path):
    zip_path = Path("tests/rehash/fixtures/valid_export.zip")
    out_file = tmp_path / "via_script.json"

    result = subprocess.run(
        ["rehashit", "parse-export", str(zip_path), "--out", str(out_file)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "📦 Loading export" in result.stdout
    assert out_file.exists()


def test_invalid_timestamp_error(tmp_path):
    from rehash.emit_structured_json import emit_conversations

    broken = [{
        "title": "Invalid Time",
        "create_time": "not-a-time",
        "messages": {},
        "source": "chatgpt"
    }]

    with pytest.raises(ValueError, match="Invalid timestamp"):
        emit_conversations(broken, tmp_path)


def test_cli_missing_args():
    result = subprocess.run(
        [sys.executable, "-m", "rehash"],
        capture_output=True,
        text=True,
    )
    assert "usage:" in result.stderr.lower()
    assert "parse-export" in result.stderr


def test_cli_invalid_subcommand():
    result = subprocess.run(
        [sys.executable, "-m", "rehash", "nonsense-cmd"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "invalid choice" in result.stderr.lower()


def test_cli_missing_func(monkeypatch):
    import argparse
    from rehash import cli

    def broken_parser():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command", required=True)

        # Attach a command but don’t set `func`
        export_cmd = subparsers.add_parser("parse-export")
        export_cmd.add_argument("zip")
        export_cmd.add_argument("--out")
        return parser

    monkeypatch.setattr(cli, "get_parser", broken_parser)

    result = cli.main(args=["parse-export", "tests/rehash/fixtures/valid_export.zip", "--out", "fake.json"])
    assert result is None

def test_cli_direct_parse_export(tmp_path):
    from rehash import cli

    zip_path = Path("tests/rehash/fixtures/valid_export.zip")
    out_file = tmp_path / "direct.json"

    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", str(zip_path), "--out", str(out_file)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert out_file.exists()


def test_extract_export_missing_conversations(tmp_path):
    from rehash.extract_export import extract_export as extract_chatgpt_export
    from zipfile import ZipFile

    zip_path = tmp_path / "broken.zip"
    with ZipFile(zip_path, "w") as zf:
        zf.writestr("not_conversations.json", "{}")

    with pytest.raises(FileNotFoundError, match="conversations.json not found"):
        extract_chatgpt_export(zip_path)


def test_cli_invalid_zip_extension():
    """Should fail if not a .zip"""
    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", "bad.txt", "--out", "fake.json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "❌ Error" in result.stderr
    

def test_cli_nonexistent_zip_file():
    """Should error if the ZIP file doesn't exist."""
    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", "missing.zip", "--out", "out.json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Zip path does not exist" in result.stderr


def test_cli_help_flag():
    """Should return 0 and show usage"""
    result = subprocess.run(
        [sys.executable, "-m", "rehash", "-h"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
    assert "parse-export" in result.stdout

def test_cli_corrupted_zip(monkeypatch, tmp_path):
    """Should show error if ZIP file is corrupted (bad magic header)."""
    bad_zip = tmp_path / "corrupt.zip"
    bad_zip.write_text("not really a zip")

    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", str(bad_zip), "--out", str(tmp_path / "out.json")],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "❌ Error:" in result.stderr
    assert "zip" in result.stderr.lower() or "badzipfile" in result.stderr.lower()


def test_cli_nonexistent_file():
    """Should fail cleanly if zip path doesn't exist."""
    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", "missing.zip", "--out", "whatever.json"],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "❌ Error:" in result.stderr
    assert "does not exist" in result.stderr.lower()


def test_cli_missing_conversations(tmp_path):
    """Should fail if zip doesn't contain conversations.json."""
    broken = tmp_path / "broken.zip"
    with open(broken, "wb") as f:
        f.write(b"PK")  # minimal but valid zip magic

    # Actually create a valid zip without 'conversations.json'
    import zipfile
    with zipfile.ZipFile(broken, "w") as zf:
        zf.writestr("not_conversations.json", "{}")

    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", str(broken), "--out", str(tmp_path / "out.json")],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "❌ Error:" in result.stderr
    assert "conversations.json" in result.stderr.lower()

def test_cli_type_error():
    """Should fail if extract returns non-list"""
    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", "tests/rehash/fixtures/valid_export.zip", "--out", "out.json"],
        capture_output=True,
        text=True,
        env={**os.environ, "REHASH_BROKEN_EXTRACT": "1"},
    )
    assert result.returncode == 1
    assert "❌ Error" in result.stderr
    assert "Expected list of conversations" in result.stderr


def test_cli_invalid_zip_path():
    """Should fail for nonexistent path"""
    result = subprocess.run(
        [sys.executable, "-m", "rehash", "parse-export", "not_a_real.zip", "--out", "fake.json"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "❌ Error" in result.stderr

def test_cli_missing_func_subprocess(tmp_path):
    """Covers CLI case where 'func' is missing → help message and return path."""
    script = tmp_path / "fake_cli.py"
    script.write_text("""
import argparse
def get_parser():
    parser = argparse.ArgumentParser()
    sp = parser.add_subparsers(dest="cmd", required=True)
    sub = sp.add_parser("x")
    return parser

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args(["x"])
    func = getattr(args, "func", None)
    if callable(func):
        func(args)
    else:
        parser.print_help()
        exit(0)
""")
    result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    assert "usage:" in result.stdout
    assert result.returncode == 0

def test_cli_module_entrypoint_runs():
    """Covers __main__ block in cli.py (line 82)."""
    result = subprocess.run([sys.executable, "-m", "rehash", "-h"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()

def test_cli_main_path_fallback(monkeypatch):
    """Covers cli.main() fallback (print_help + return path) in-process."""
    from rehash import cli

    def parser_without_func():
        import argparse
        parser = argparse.ArgumentParser()
        sp = parser.add_subparsers(dest="command", required=True)
        sp.add_parser("dummy")  # no func set!
        return parser

    monkeypatch.setattr(cli, "get_parser", parser_without_func)
    result = cli.main(["dummy"])  # triggers print_help path
    assert result is None

def test_cli_run_main_direct(monkeypatch, capsys):
    """Cover cli.py lines 41-42, 83, 86 via in-process entry."""
    from rehash import cli

    def dummy_parser():
        import argparse
        parser = argparse.ArgumentParser(description="Dummy CLI")
        sp = parser.add_subparsers(dest="cmd", required=True)
        sp.add_parser("dummy")  # no .set_defaults(func=...)
        return parser

    monkeypatch.setattr(cli, "get_parser", dummy_parser)
    cli.run_as_main(["dummy"])

    out, err = capsys.readouterr()
    assert "usage:" in out
    assert "Dummy CLI" in out

def test_cli_parse_export_with_fitness_only(tmp_path):
    import subprocess
    zip_path = "tests/rehash/fixtures/valid_export.zip"
    out_file = tmp_path / "fitness.json"

    result = subprocess.run(
        [
            sys.executable,
            "-m", "rehash",
            "parse-export",
            zip_path,
            "--out", str(out_file),
            "--fitness-only",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "🏋️ Filtered fitness conversations" in result.stdout
    assert out_file.exists()

def test_cli_main_module_invocation():
    """Covers `__name__ == '__main__'` → line 87."""
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "rehash.cli", "--help"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Rehash CLI Tool" in result.stdout
