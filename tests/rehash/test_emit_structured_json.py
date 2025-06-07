# tests/tools/rehash/test_emit_structured_json.py
def test_emit_conversations(tmp_path):
    from rehash.emit_structured_json import emit_conversations

    dummy_convos = [
        {
            "title": "My Chat w/ GPT",
            "timestamp": 1717452300,
            "messages": {"1": {"message": "hi!"}},
            "source": "chatgpt"
        }
    ]

    out_paths = emit_conversations(dummy_convos, tmp_path)
    assert len(out_paths) == 1
    assert out_paths[0].name.startswith("2024-06")
    assert out_paths[0].read_text(encoding="utf-8").startswith("{")
