import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta, timezone

# app.service.reminder_service から ReminderService をインポート
from app.service.reminder_service import ReminderService

class TestReminderService:
    def setup_method(self):
        self.mock_task_manager = MagicMock()
        self.reminder = ReminderService(self.mock_task_manager, "dummy_list_id")

    @patch('app.service.reminder_service.speak')
    def test_reminder_5min_before(self, mock_speak):
        now = datetime.now(timezone.utc)
        self.mock_task_manager.get_tasks_for_person.return_value = [
            {'name': 'Test Task', 'due': (now + timedelta(minutes=5)).isoformat().replace('+00:00', 'Z')}
        ]

        self.reminder.check_reminders()

        assert mock_speak.called
        mock_speak.assert_called_with('もうすぐ Test Task の時間ですよ！')

    @patch('app.service.reminder_service.speak')
    def test_reminder_exact_time(self, mock_speak):
        now = datetime.now(timezone.utc)
        self.mock_task_manager.get_tasks_for_person.return_value = [
            {'name': 'Exact Time Task', 'due': now.isoformat().replace('+00:00', 'Z')}
        ]

        self.reminder.check_reminders()

        assert mock_speak.called
        mock_speak.assert_called_with('今、 Exact Time Task をやる時間です！')

    @patch('app.service.reminder_service.speak')
    def test_reminder_ignores_past_due_tasks(self, mock_speak):
        past_time = datetime.now(timezone.utc) - timedelta(minutes=10)  # 10分前
        self.mock_task_manager.get_tasks_for_person.return_value = [
            {'name': 'Expired Task', 'due': past_time.isoformat().replace('+00:00', 'Z')}
        ]

        self.reminder.check_reminders()

        # speakは呼び出されていないことを確認
        mock_speak.assert_not_called()

if __name__ == '__main__':
    unittest.main()
