# task_assistant/scheduler/reminders.py
import logging, os
from datetime import datetime, UTC, timedelta

from task_assistant.db import dao

log = logging.getLogger("reminder")
BEFORE_SEC  = int(os.getenv("REMIND_BEFORE_SEC", 300))   # 5 min
BEFORE = BEFORE_SEC                                     # ← add this line
WINDOW_SEC  = int(os.getenv("REMIND_WINDOW_SEC", 60))

def check_reminders():
    """Called by APScheduler every CHECK_INTERVAL_SEC seconds."""
    now = datetime.now(UTC)
    tasks = dao.due_soon(now, BEFORE_SEC, WINDOW_SEC)
    for t in tasks:
        if t.reminded_at:
            continue
        log.info("⏰ REMINDER • %s (due %s)", t.title, t.due)
        # future: publish MQTT / Slack here
        dao.mark_reminded(t.id, now)
