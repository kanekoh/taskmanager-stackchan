# task_assistant/db/dao.py
from pathlib import Path
from datetime import datetime, timedelta  
from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine, select
from .models import Task

# make sure the folder exists
BASE_DIR = Path(__file__).resolve().parent.parent / "data"
BASE_DIR.mkdir(parents=True, exist_ok=True)

_engine = create_engine(
    f"sqlite:///{BASE_DIR / 'tasks.db'}",
    echo=False,
    connect_args={"check_same_thread": False},  # safe for FastAPI threads
)

SQLModel.metadata.create_all(_engine)

@contextmanager
def session():
    with Session(_engine) as s:
        yield s

def upsert_task(card_id: str, title: str, due, status: str):
    with session() as s:
        task = s.get(Task, card_id) or Task(id=card_id)
        task.title, task.due, task.status = title, due, status
        task.updated_at = datetime.utcnow()
        s.add(task)
        s.commit()

def due_soon(now, before_sec, window_sec):
    lo = now + timedelta(seconds=before_sec)
    hi = lo + timedelta(seconds=window_sec)
    with session() as s:
        return s.exec(
            select(Task)
            .where(Task.status == "pending")
            .where(Task.due.is_not(None))
            .where(Task.due.between(lo, hi))
        ).all()

def mark_reminded(task_id, when):
    with session() as s:
        t = s.get(Task, task_id)
        if t:
            t.reminded_at = when
            s.add(t); s.commit()
