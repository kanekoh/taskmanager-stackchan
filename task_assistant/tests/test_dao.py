# tests/test_dao.py
from datetime import datetime, timezone, timedelta
from task_assistant.db.dao import upsert_task, due_soon
from task_assistant.db.models import Task

def test_upsert_insert_then_update(mem_session):
    upsert_task("1", "Math", None, "pending")
    upsert_task("1", "Math HW", None, "done")   # update same pk

    row = mem_session.get(Task, "1")
    assert row.title == "Math HW"
    assert row.status == "done"

def test_due_soon_boundary_conditions(mem_session):
    """
    due_soon 関数の境界値テスト
    """
    now = datetime.now(timezone.utc)
    before_sec = 300 # 5分
    # 境界値のタスクを作成
    upsert_task("task_boundary_lower", "Due exactly now", now, "pending")
    task_lower = mem_session.get(Task, "task_boundary_lower")
    print(f"Task Lower Due: {task_lower.due if task_lower else None}")
    upsert_task("task_boundary_upper", "Due exactly at boundary", now + timedelta(seconds=before_sec), "pending")
    task_upper = mem_session.get(Task, "task_boundary_upper")
    print(f"Task Upper Due: {task_upper.due if task_upper else None}")
    # 境界値のすぐ外側のタスクを作成
    upsert_task("task_just_before", "Due just before now", now - timedelta(seconds=1), "pending")
    upsert_task("task_just_after", "Due just after boundary", now + timedelta(seconds=before_sec + 1), "pending")
    # due_soon を実行
    tasks = due_soon(now, before_sec, 60)
    # 検証
    task_ids = {t.id for t in tasks}
    assert len(tasks) == 2
    assert "task_boundary_lower" in task_ids
    assert "task_boundary_upper" not in task_ids
    assert "task_just_before" in task_ids
    assert "task_just_after" not in task_ids
def test_due_soon_no_due_date(mem_session):
    """
    期限 (due) が設定されていないタスクは取得されないことをテスト
    """
    now = datetime.now()
    before_sec = 300

    upsert_task("task_no_due", "Task without due date", None, "pending")

    tasks = due_soon(now, before_sec, 60)
    assert len(tasks) == 0

def test_due_soon_ignores_done_task(mem_session):
    """
    ステータスが 'done' のタスクは無視されるかテスト
    """
    now = datetime.now(timezone.utc)
    due_time = now + timedelta(seconds=150)
    before_sec = 300
    upsert_task("task4", "Done task", due_time, "done") # ステータスを done に
    tasks = due_soon(now, before_sec, 60)
    assert len(tasks) == 0

def test_due_soon_ignores_naive_task(mem_session):
    """
    Naive datetimes for `due` are ignored, because now() is utc aware.
    """
    now = datetime.now(timezone.utc)
    due_time = datetime.now() + timedelta(seconds=150)
    before_sec = 300
    upsert_task("task4", "Naive task", due_time, "pending") # ステータスを pending に
    tasks = due_soon(now, before_sec, 60)
    assert len(tasks) == 0
