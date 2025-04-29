from enum import Enum, auto

class StackchanMode(Enum):
    IDLE = auto()               # 誰もいない・待機中
    GREETING = auto()            # 人認識して挨拶中
    TASK_MANAGEMENT = auto()     # タスク確認・設定中
    FREE_TALK = auto()           # 通常会話モード
