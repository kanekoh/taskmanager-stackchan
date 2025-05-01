# tests/test_reminder.py
from datetime import datetime, UTC, timedelta
from contextlib import contextmanager
from task_assistant.db.models import Task
from task_assistant.scheduler.reminders import check_reminders, BEFORE_SEC

def test_due_soon_triggers_once(mem_session, monkeypatch):
    now = datetime.now(UTC)
    # pad by +5 s so it's surely > now+BEFORE_SEC
    due = now + timedelta(seconds=BEFORE_SEC + 5)

    t = Task(id="x", title="Test", due=due, status="pending")
    mem_session.add(t); mem_session.commit()

    # patch dao.session to use in-memory DB
    from task_assistant import db as _db
    @contextmanager
    def _mem_ctx(): yield mem_session
    monkeypatch.setattr(_db.dao, "session", _mem_ctx, raising=True)

    check_reminders()               # first pass
    mem_session.refresh(t)
    assert t.reminded_at is not None

    reminded = t.reminded_at
    check_reminders()               # second pass
    mem_session.refresh(t)
    assert t.reminded_at == reminded
