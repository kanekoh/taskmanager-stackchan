# tests/test_dao.py
from datetime import datetime
from task_assistant.db.dao import upsert_task
from task_assistant.db.models import Task

def test_upsert_insert_then_update(mem_session):
    upsert_task("1", "Math", None, "pending")
    upsert_task("1", "Math HW", None, "done")   # update same pk

    row = mem_session.get(Task, "1")
    assert row.title == "Math HW"
    assert row.status == "done"
