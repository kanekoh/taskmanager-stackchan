# app/service/conversation_manager.py

from app.client.voicevox_client import speak

class ConversationManager:
    def __init__(self, task_manager, list_id, done_list_id, doing_list_id):
        self.task_manager = task_manager
        self.list_id = list_id
        self.done_list_id = done_list_id
        self.doing_list_id = doing_list_id

    def start_conversation(self, person_name: str):
        """
        人を認識したら呼び出す
        """
        speak(f"{person_name}さん、こんにちは！今日のタスクを確認しましょう。")

        tasks = self.task_manager.get_tasks_for_person(self.list_id)

        if not tasks:
            speak("今日はやることはないみたいです。")
            return

        for task in tasks:
            task_name = task['name']
            card_id = task['id']
            speak(f"{task_name} は終わりましたか？")

            # ユーザーからYes/Noを仮でinput()で受け取る
            answer = input("スタックチャン（入力してね） [yes/no/doing]: ").strip().lower()

            if answer == "yes":
                self.task_manager.move_card_to_list(card_id, self.done_list_id)
                speak("すごいね！完了に移動しました。")
            elif answer == "doing":
                self.task_manager.move_card_to_list(card_id, self.doing_list_id)
                speak("頑張ってるね！実施中に移動しました。")
            else:
                speak("いつやる予定ですか？たとえば、４時？")
                time_str = input("スタックチャン（予定時間を入力してね）: ").strip()
                # ここは仮で今日の日付＋時間でDueDateを設定
                from datetime import datetime
                now = datetime.now()
                due_datetime = datetime.strptime(f"{now.date()} {time_str}", "%Y-%m-%d %H時")
                due_iso = due_datetime.isoformat() + ".000Z"
                self.task_manager.update_due_date(card_id, due_iso)
                speak("予定時間を設定しました！")
