# task_assistant/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from task_assistant.trello.poller import poll_once
from task_assistant.db.dao import _engine, SQLModel
from apscheduler.schedulers.background import BackgroundScheduler
from task_assistant.scheduler import sched      # ← KEEP this import

scheduler = BackgroundScheduler(timezone="UTC")
scheduler.add_job(poll_once, "interval", seconds=60, id="trello_poll")

# ── lifespan handler ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    SQLModel.metadata.create_all(_engine)
    scheduler.start()
    print("Startup complete")
    yield
    # shutdown
    scheduler.shutdown()
    print("Clean shutdown")

app = FastAPI(title="Stack-chan Assistant API", lifespan=lifespan)
