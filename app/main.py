from dotenv import load_dotenv
from app.client.google_client import GoogleAIClient
from app.client.trello_client import TrelloClient
from app.client.voicevox_client import speak
from app.service.person_detector import PersonDetector
from app.service.task_manager import TaskManager
from app.service.conversation_manager import ConversationManager
from app.service.reminder_service import ReminderService
import os

load_dotenv()

speak("こんにちは！ぼくはスタックチャンだよ！")

class InputProvider:
    def get_input(self) -> str:
        raise NotImplementedError

class ConsoleInputProvider(InputProvider):
    def get_input(self) -> str:
        return input("あなた: ")


def main():
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
    TRELLO_API_TOKEN = os.environ.get("TRELLO_API_TOKEN")
    TODO_LIST_ID = os.environ.get("TODO_LIST_ID")
    DONE_LIST_ID = os.environ.get("DONE_LIST_ID")
    DOING_LIST_ID = os.environ.get("DOING_LIST_ID")

    client = GoogleAIClient(api_key=GOOGLE_API_KEY)
    input_provider = ConsoleInputProvider()
    history = []

    # 各種クライアント・サービス初期化
    trello_client = TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_API_TOKEN)
    task_manager = TaskManager(trello_client)
    person_detector = PersonDetector()
    conversation_manager = ConversationManager(task_manager, TODO_LIST_ID, DONE_LIST_ID, DOING_LIST_ID)

    # リマインダーサービス開始
    reminder_service = ReminderService(task_manager, TODO_LIST_ID)
    reminder_service.start()

    print("=== スタックチャンと会話開始！ ===")
    while True:
        user_input = input("あなた: ")

        # まず /detect コマンドを見つけたら人認識イベントを発火
        detected_person = person_detector.detect_person(user_input)
        if detected_person:
            conversation_manager.start_conversation(detected_person)
            person_detector.reset()
            continue

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("スタックチャン: またね！👋")
            speak("またね！")
            break

        # 通常の自由会話（今まで通り）
        # （ここは既存のChatAPI client.send_message() 呼び出しに接続してもOK）

        history.append({"role": "user", "content": user_input})
        response = client.send_message(history)
        bot_message = response["content"]

        print(f"スタックチャン: {bot_message}")
        history.append({"role": "model", "content": bot_message})

        print(bot_message)
        speak(bot_message)

if __name__ == "__main__":
    main()