class ChatAPIClient:
    def send_message(self, messages: list[dict]) -> dict:
        """ユーザーのメッセージリストを送って、AIからの返答を返す"""
        raise NotImplementedError
