import logging, os
from datetime import datetime, UTC, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from task_assistant.db import dao

log = logging.getLogger("reminder")
BEFORE_SEC  = int(os.getenv("REMIND_BEFORE_SEC", 300))
BEFORE = BEFORE_SEC
WINDOW_SEC  = int(os.getenv("REMIND_WINDOW_SEC", 60))
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
slack_client = WebClient(token=SLACK_TOKEN) if SLACK_TOKEN else None

def check_reminders():
    """Called by APScheduler every CHECK_INTERVAL_SEC seconds."""
    now = datetime.now(UTC)
    tasks = dao.due_soon(now, BEFORE_SEC, WINDOW_SEC)
    for t in tasks:
        if t.reminded_at:
            continue
        log.info("⏰ REMINDER • %s (due %s)", t.title, t.due)
        # future: publish MQTT / Slack here

        # --- Slack チャンネルへの投稿処理 ---
        # slack_client と SLACK_CHANNEL_ID の両方が設定されている場合のみ実行
        if slack_client and SLACK_CHANNEL_ID:
            try:
                message = f"⏰ Reminder: Task '{t.title}' is due soon! (Due: {t.due.strftime('%Y-%m-%d %H:%M') if t.due else 'N/A'})"
                response = slack_client.chat_postMessage(channel=SLACK_CHANNEL_ID, text=message)
                log.info("Sent reminder to Slack channel %s (Task ID: %s)", SLACK_CHANNEL_ID, t.id)
            except SlackApiError as e:
                log.error("Error sending Slack message for task %s: %s", t.id, e.response["error"])

        dao.mark_reminded(t.id, now)

