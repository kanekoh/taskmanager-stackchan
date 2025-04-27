import requests

class TrelloClient:
    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1"

    def get_cards_from_list(self, list_id: str):
        """
        指定されたリストIDからカード一覧を取得する
        """
        url = f"{self.base_url}/lists/{list_id}/cards"
        query = {
            'key': self.api_key,
            'token': self.token,
        }
        response = requests.get(url, params=query)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return []

    def move_card(self, card_id: str, target_list_id: str):
        url = f"{self.base_url}/cards/{card_id}"
        query = {
            'key': self.api_key,
            'token': self.token,
            'idList': target_list_id,
        }
        response = requests.put(url, params=query)

        if response.status_code != 200:
            print(f"Error moving card: {response.status_code}")
            print(response.text)

    def update_card_due_date(self, card_id: str, due_date: str):
        url = f"{self.base_url}/cards/{card_id}"
        query = {
            'key': self.api_key,
            'token': self.token,
            'due': due_date,
        }
        response = requests.put(url, params=query)

        if response.status_code != 200:
            print(f"Error updating due date: {response.status_code}")
            print(response.text)
