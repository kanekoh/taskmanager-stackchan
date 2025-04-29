# app/controller/stackchan_controller.py

from app.model.stackchan_mode import StackchanMode
from datetime import datetime, timezone

class StackchanController:
    def __init__(self, task_manager, conversation_manager):
        self.mode = StackchanMode.IDLE
        self.task_manager = task_manager
        self.conversation_manager = conversation_manager
        self.current_person = None
        self.pending_tasks = []
        self.current_task = None

    def handle_input(self, user_input):
        """ユーザー入力を受け取って、モードに応じた処理を行う"""
        user_input = user_input.strip()

        if self.mode == StackchanMode.IDLE:
            if user_input.startswith("/detect"):
                _, name = user_input.split(maxsplit=1)
                self.current_person = name
                self.mode = StackchanMode.GREETING

        elif self.mode == StackchanMode.FREE_TALK:
            self.conversation_manager.handle_free_talk(user_input)

        elif self.mode == StackchanMode.TASK_MANAGEMENT:
            self._handle_task_response(user_input)

    def tick(self):
        """時間経過や内部進行管理をする"""
        if self.mode == StackchanMode.GREETING:
            self._greet_and_fetch_tasks()

        elif self.mode == StackchanMode.TASK_MANAGEMENT:
            self._ask_about_task()

        # IDLE / FREE_TALKは特にtickではやることなし

    def _greet_and_fetch_tasks(self):
        from app.client.voicevox_client import speak

        speak(f"{self.current_person}さん、こんにちは！タスクを確認しますね。")
        self.pending_tasks = self.task_manager.get_tasks_for_person(self.conversation_manager.list_id)

        if not self.pending_tasks:
            speak("今日は特にやることはないみたい！")
            self.mode = StackchanMode.FREE_TALK
        else:
            self.current_task = self.pending_tasks.pop(0)
            self.mode = StackchanMode.TASK_MANAGEMENT
            self._ask_about_task()  # ★ モード切り替えたら即タスク質問！！

    def _ask_about_task(self):
        from app.client.voicevox_client import speak

        if not self.current_task:
            if self.pending_tasks:
                self.current_task = self.pending_tasks.pop(0)
            else:
                speak("また時間になったら声をかけるね！")
                self.mode = StackchanMode.FREE_TALK
                return

        speak(f"{self.current_task['name']} は終わりましたか？")

    def _handle_task_response(self, user_input):
        from app.utils.time_parser import parse_due_time_input
        from app.client.voicevox_client import speak

        answer = user_input.lower()

        if answer == "yes":
            self.current_task.mark_done()
            self.task_manager.move_task_to_done(self.current_task)
            speak("お疲れさま！タスクを完了にしました。")
            self.current_task = None

        elif answer == "doing":
            self.current_task.mark_doing()
            self.task_manager.move_task_to_doing(self.current_task)
            speak("頑張ってるね！タスクを実施中にしました。")
            self.current_task = None

        else:
            while True:
                speak("いつやる予定？")
                time_str = input("スタックチャン（予定時間を入力してね）: ").strip()

                try:
                    due_datetime = parse_due_time_input(time_str)
                    due_iso = due_datetime.isoformat()

                    self.current_task['due'] = due_iso
                    self.task_manager.update_task_due_date(self.current_task)
                    
                    speak(f"予定時間 {due_datetime.strftime('%H時%M分')} に設定しました。")
                    self.current_task = None
                    break

                except ValueError:
                    speak("うまく予定時間がわからなかったよ。もう一度教えてね！")
                    continue
