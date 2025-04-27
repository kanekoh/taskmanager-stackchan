import threading
import time
from datetime import datetime, timedelta
from app.client.voicevox_client import speak

class ReminderService:
    def __init__(self, task_manager, todo_list_id):
        self.task_manager = task_manager
        self.todo_list_id = todo_list_id

    def start(self):
        thread = threading.Thread(target=self._reminder_loop, daemon=True)
        thread.start()

    def _reminder_loop(self):
        while True:
            now = datetime.now()
            tasks = self.task_manager.get_tasks_for_person(self.todo_list_id)

            for task in tasks:
                due_raw = task.get('due')
                if due_raw:
                    # due = datetime.fromisoformat(due_raw.replace('Z', '+00:00'))
                    due = datetime.fromisoformat(due_raw.replace('Z', '')).replace(tzinfo=None)
                    print(f"[リマインダー] チェック中タスク: {task['name']} / 期限: {due}, {now}")

                    if now >= due - timedelta(minutes=5) and now < due - timedelta(minutes=4):
                        # 5分前リマインド
                        print(f"5分前リマインド: {task['name']}")
                        speak(f"もうすぐ {task['name']} の時間ですよ！")

                    if now >= due and now < due + timedelta(minutes=1):
                        # ちょうどのリマインド
                        print(f"時間ちょうどリマインド: {task['name']}")
                        speak(f"今、 {task['name']} をやる時間です！")

                    # さらにスヌーズ通知も後で追加できる！

            time.sleep(30)  # 30秒おきにチェック
