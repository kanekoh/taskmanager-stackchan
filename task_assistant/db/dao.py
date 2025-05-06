# task_assistant/db/dao.py
import os
from pathlib import Path
from datetime import datetime, timedelta  
from contextlib import contextmanager; from datetime import timezone # UTC をインポート
from sqlmodel import SQLModel, Session, create_engine, select
from dotenv import load_dotenv
from .models import Task

load_dotenv() # .env ファイルを読み込む

# 環境変数 DATABASE_URL からデータベース接続文字列を取得。なければデフォルト値を使用。
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "tasks.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.resolve()}")

_engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},  # safe for FastAPI threads
)

SQLModel.metadata.create_all(_engine)

@contextmanager
def session():
    with Session(_engine) as s:
        yield s

def upsert_task(card_id: str, title: str, due, status: str):
    """Update or insert a task."""
    with Session(_engine) as s:
        task = s.get(Task, card_id) # まず ID でタスクを検索
        now = datetime.now(timezone.utc)
        if task:
            # タスクが見つかった場合：更新
            task.title = title
            task.due = due
            task.status = status
            task.updated_at = now
        else:
            # タスクが見つからなかった場合：新規作成
            task = Task(id=card_id, title=title, due=due, status=status, created_at=now, updated_at=now) # (id -> card_id に修正)
            s.add(task)
        s.commit()

def due_soon(now, before_sec, window_sec):
    lo = now - timedelta(seconds=before_sec)
    hi = now + timedelta(seconds=window_sec)
    with session() as s:
        return s.exec(
            select(Task)
            .where(Task.status == "pending")
            .where(Task.due.is_not(None))
            .where(Task.due.between(lo, hi))
            .where(Task.reminded_at.is_(None))  # リマインドされていないタスクのみ
        ).all()

def mark_reminded(task_id, when):
    with session() as s:
        t = s.get(Task, task_id)
        if t:
            t.reminded_at = when
            s.add(t); s.commit()


