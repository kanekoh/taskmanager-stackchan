# app/service/task_manager.py

from app.client.trello_client import TrelloClient

class TaskManager:
    def __init__(self, trello_client: TrelloClient):
        self.client = trello_client

    def get_tasks_for_person(self, list_id: str):
        """
        指定リストIDからタスク一覧を取得する
        """
        return self.client.get_cards_from_list(list_id)

    def move_card_to_list(self, card_id: str, target_list_id: str):
        """
        指定カードを別リストに移動する
        """
        self.client.move_card(card_id, target_list_id)

    def update_due_date(self, card_id: str, due_date: str):
        """
        指定カードのDueDateを更新する
        due_dateはISO8601形式（例："2025-04-27T18:00:00.000Z"）
        """
        self.client.update_card_due_date(card_id, due_date)
