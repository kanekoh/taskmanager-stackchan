# tests/test_reminder.py
from datetime import datetime, UTC, timedelta, timezone
from task_assistant.db.models import Task
from sqlalchemy import select
from task_assistant.scheduler.reminders import BEFORE_SEC, WINDOW_SEC
from task_assistant.db import dao # Import dao correctly

def test_due_soon_triggers_once(mem_session, monkeypatch):
    # --- Directly call dao.due_soon and dao.mark_reminded with mem_session ---
    monkeypatch.setenv("WINDOW_SEC", "600") # Ensure that WINDOW_SEC is large enough
    from task_assistant.scheduler.reminders import BEFORE_SEC, WINDOW_SEC
    now = datetime.now(UTC)
    # pad by +5 s so it's surely > now+BEFORE_SEC
    due = now - timedelta(seconds=BEFORE_SEC - 5)
    t = Task(id="x", title="Test", due=due, status="pending")
    mem_session.add(t); mem_session.commit()
    tasks = dao.due_soon(now, BEFORE_SEC, WINDOW_SEC) # Call the function using dao
    assert len(tasks) == 1
    dao.mark_reminded(t.id, now)
    mem_session.refresh(t)
    assert t.reminded_at is not None
    reminded = t.reminded_at
    # The second call to check_reminders should not change reminded_at
    tasks = dao.due_soon(now, BEFORE_SEC, WINDOW_SEC) # Call the function using dao
    assert len(tasks) == 0
    mem_session.refresh(t)
    assert t.reminded_at == reminded

