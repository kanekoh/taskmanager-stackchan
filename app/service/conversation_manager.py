# app/service/conversation_manager.py

from app.client.voicevox_client import speak

class ConversationManager:
    def __init__(self, ai_client, todo_list_id, done_list_id, doing_list_id):
        self.ai_client = ai_client
        self.list_id = todo_list_id
        self.done_list_id = done_list_id
        self.doing_list_id = doing_list_id

    def handle_free_talk(self, user_input):
        from app.client.voicevox_client import speak

        response = self.ai_client.send_message([{"role": "user", "content": user_input}])
        bot_message = response["content"]
        speak(bot_message)