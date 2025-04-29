from enum import Enum, auto

class TaskStatus(Enum):
    TODO = auto()                # まだ未着手
    DOING = auto()               # 実施中
    DONE = auto()                # 完了
    WAITING = auto()             # 実施予定あり（DueDateあり）
    REMINDER_PENDING = auto()    # リマインダー待ち
    REMINDER_DONE = auto()       # リマインド後の完了確認済み
