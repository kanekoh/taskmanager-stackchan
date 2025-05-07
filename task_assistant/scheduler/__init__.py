import os
from dotenv import load_dotenv, find_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from task_assistant.trello.poller import poll_once
import logging
from .reminders import check_reminders, BEFORE
              
load_dotenv(find_dotenv(), override=False)
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SEC", "60"))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("scheduler")

sched = BackgroundScheduler(timezone="UTC")
sched.add_job(poll_once, "interval", seconds=POLL_INTERVAL, id="trello_poll")
sched.add_job(check_reminders, "interval",
              seconds=int(os.getenv("CHECK_INTERVAL_SEC", 30)),
              id="task_reminder")
sched.start()
log.info("Scheduler started (interval=%s s)", POLL_INTERVAL)
