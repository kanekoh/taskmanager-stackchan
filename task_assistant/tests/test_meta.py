# tests/test_meta.py
from task_assistant.trello.poller import _save_cursor, _get_cursor

def test_meta_save(mem_session):
    cur, meta = _get_cursor()
    assert cur.startswith("2025")               # default

    _save_cursor(meta, "2025-05-01T00:00:00Z")
    cur2, _ = _get_cursor()
    assert cur2 == "2025-05-01T00:00:00Z"
