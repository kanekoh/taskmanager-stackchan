from app.model.task_status import TaskStatus
from app.utils.time_parser import parse_due_time_input

class Task:
    def __init__(self, id: str, name: str, due: str = None):
        self.id = id              # TrelloのカードID
        self.name = name          # タスク名
        self.due = due            # 期限（ISO8601文字列）
        self.status = TaskStatus.TODO  # 最初はTODOとしてスタート

    def update_due_date(self, new_due: str):
        self.due = new_due
        self.status = TaskStatus.WAITING

    def mark_done(self):
        self.status = TaskStatus.DONE

    def mark_doing(self):
        self.status = TaskStatus.DOING

    def is_due_soon(self, current_time):
        """ 期限5分前か？（ローカルタイム基準） """
        if not self.due:
            return False

        due_time = datetime.fromisoformat(self.due.replace('Z', ''))  # Zを単純に除去
        due_time = due_time.replace(tzinfo=None)  # tzinfoも完全に消す

        return due_time - timedelta(minutes=5) <= current_time < due_time - timedelta(minutes=4)

    def is_due_now(self, current_time):
        """ 期限ちょうどか？（ローカルタイム基準） """
        if not self.due:
            return False

        due_time = datetime.fromisoformat(self.due.replace('Z', ''))  # Zを単純に除去
        due_time = due_time.replace(tzinfo=None)  # tzinfoも完全に消す

        return due_time <= current_time < due_time + timedelta(minutes=1)