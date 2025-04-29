# app/main.py

from app.controller.stackchan_controller import StackchanController
from app.client.input_provider import InputProvider
from app.client.google_client import GoogleAIClient
from app.client.voicevox_client import speak
from app.service.task_manager import TaskManager
from app.service.conversation_manager import ConversationManager
from app.client.trello_client import TrelloClient
from app.service.reminder_service import ReminderService
from dotenv import load_dotenv
import os
import time

def main():
    load_dotenv()
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    trello_api_key = os.environ.get("TRELLO_API_KEY")
    trello_token = os.environ.get("TRELLO_API_TOKEN")
    # 追加でリストIDを読み取る
    todo_list_id = os.environ.get("TRELLO_TODO_LIST_ID")
    done_list_id = os.environ.get("TRELLO_DONE_LIST_ID")
    doing_list_id = os.environ.get("TRELLO_DOING_LIST_ID")


    trello_client = TrelloClient(trello_api_key, trello_token)

    # 各種クライアント・サービス初期化
    input_provider = InputProvider()
    ai_client = GoogleAIClient(google_api_key)
    task_manager = TaskManager(trello_client)
    conversation_manager = ConversationManager(ai_client, todo_list_id, done_list_id, doing_list_id)

    # スタックチャンのコントローラを作成
    controller = StackchanController(task_manager, conversation_manager)

    reminder_service = ReminderService(task_manager, todo_list_id)
    reminder_service.start()

    print("=== スタックチャン起動完了！会話を開始します ===")

    while True:
        # ユーザー入力を取得
        user_input = input_provider.get_input()

        # 入力をコントローラに渡す
        controller.handle_input(user_input)

        # 時間経過など内部処理を進める
        controller.tick()

        # 少しsleep（高頻度で回さないため）
        time.sleep(0.5)

if __name__ == "__main__":
    main()
