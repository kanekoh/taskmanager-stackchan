# tests/test_poller.py
import json, pathlib
import pytest, os
from datetime import datetime, timezone
from task_assistant.trello import poller
from task_assistant.db.models import Task
import requests

FAKE_ACTIONS = [
    {
        "date": "2025-05-01T01:00:00Z",
        "data": {
            "card": {"id": "c1", "name": "Test card", "due": None, "closed": False},
            "list": {"id": "l1", "name": "Inbox"}
        }
    }
]

class FakeResp:
    def __init__(self, json_obj):
        self._json = json_obj
        self.status_code = 200
    def json(self):
        return self._json
    def raise_for_status(self): pass

def fake_get(*_, **__):
    return FakeResp(FAKE_ACTIONS)

@pytest.mark.usefixtures("mem_session")
def test_poll_once(monkeypatch):
    monkeypatch.setenv("TRELLO_BOARD_ID", "dummy")
    monkeypatch.setenv("TRELLO_KEY", "x")
    monkeypatch.setenv("TRELLO_TOKEN", "y")
    monkeypatch.setattr(requests, "get", fake_get)

    poller.poll_once()

    from task_assistant.db.dao import session
    with session() as s:
        t = s.get(Task, "c1")
        assert t and t.title == "Test card"
