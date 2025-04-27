# app/service/person_detector.py

class PersonDetector:
    def __init__(self):
        self.detected_person = None

    def detect_person(self, user_input: str):
        """
        ユーザー入力から人認識イベントを発火させる
        例: "/detect パパ" と打ったら "パパ" を認識したことにする
        """
        if user_input.startswith("/detect "):
            person_name = user_input[len("/detect "):].strip()
            if person_name:
                self.detected_person = person_name
                return person_name
        return None

    def reset(self):
        """検出済み人物をリセット"""
        self.detected_person = None
