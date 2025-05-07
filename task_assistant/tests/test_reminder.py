# tests/test_reminder.py
from datetime import datetime, UTC, timedelta, timezone
from task_assistant.db.models import Task
from sqlalchemy import select
from task_assistant.db import dao
from task_assistant.scheduler.reminders import BEFORE_SEC, WINDOW_SEC
from task_assistant.scheduler.reminders import check_reminders
from task_assistant.scheduler.reminders import slack_client, SLACK_CHANNEL_ID

# ここに Slack 連携のテスト関数を追加
import os
from unittest.mock import patch
import pytest
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# Slack API の呼び出しをモックする
@patch("slack_sdk.WebClient.chat_postMessage")
def test_slack_message_sent(mock_chat_postMessage, mem_session, monkeypatch):
    # --- Directly call dao.due_soon and dao.mark_reminded with mem_session ---
    monkeypatch.setenv("WINDOW_SEC", "600") # Ensure that WINDOW_SEC is large enough
    from task_assistant.scheduler.reminders import BEFORE_SEC, WINDOW_SEC
    now = datetime.now(UTC)
    # pad by +5 s so it's surely > now+BEFORE_SEC
    due = now - timedelta(seconds=BEFORE_SEC - 5)
    t = Task(id="x", title="Test Task", due=due, status="pending")
    mem_session.add(t); mem_session.commit()
    tasks = dao.due_soon(now, BEFORE_SEC, WINDOW_SEC) # Call the function using dao
    assert len(tasks) == 1

    """
    Slack メッセージが送信されることをテストする
    """
    # テストに必要なタスクを作成するなど、必要なセットアップを行う
    # 例: upsert_task("task1", "Test Task", datetime.now(), "pending")

    # テスト対象の関数を実行
    check_reminders()

    # モックが期待どおりに呼び出されたことをアサート
    mock_chat_postMessage.assert_called_once()

    # モックに渡された引数を確認
    args, kwargs = mock_chat_postMessage.call_args
    assert kwargs["channel"] == "test_channel"
    assert "Test Task" in kwargs["text"]  # テキストにタスク名が含まれているか確認

@patch("slack_sdk.WebClient.chat_postMessage")
def test_slack_api_error(mock_chat_postMessage, mem_session):
    """
    Slack API エラーが発生した場合の処理をテストする
    """
    # Slack API がエラーを返すようにモックを設定
    mock_chat_postMessage.side_effect = SlackApiError(
        message="Testing Error", response={"ok": False, "error": "testing_error"}
    )

    # エラーが発生しないことを確認 (例外が発生しないことを確認)
    try:
        check_reminders()
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

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