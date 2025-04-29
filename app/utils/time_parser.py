# app/utils/time_parser.py

import re
from datetime import datetime, timezone, timedelta
import time

def parse_due_time_input(time_str: str) -> datetime:
    """ ユーザー入力から予定時間を柔軟に解釈する（午前午後対応） """
    is_pm = False
    is_am = False

    if "午後" in time_str:
        is_pm = True
        time_str = time_str.replace("午後", "")
    elif "午前" in time_str:
        is_am = True
        time_str = time_str.replace("午前", "")

    time_str = time_str.strip()

    # 完全に時だけ（例: 3）
    if re.match(r"^\d{1,2}$", time_str):
        hour = int(time_str)
        minute = 0

    # 時:分形式（例: 3:30）
    elif re.match(r"^\d{1,2}:\d{2}$", time_str):
        hour, minute = map(int, time_str.split(":"))

    # 時「時」だけ（例: 3時）
    elif re.match(r"^\d{1,2}時$", time_str):
        hour = int(time_str.replace("時", ""))
        minute = 0

    # 時・分「時分」表記（例: 3時30分）
    elif re.match(r"^\d{1,2}時\d{1,2}分$", time_str):
        hour = int(re.findall(r"(\d{1,2})時", time_str)[0])
        minute = int(re.findall(r"時(\d{1,2})分", time_str)[0])

    else:
        raise ValueError("入力フォーマットが認識できませんでした。")

    # 午前午後を適用
    if is_pm and hour < 12:
        hour += 12
    if is_am and hour == 12:
        hour = 0

    now = datetime.now()
    due_datetime = datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute).astimezone()
    # PCのローカルタイムゾーンのオフセット（秒単位）を取得
    offset_seconds = time.localtime().tm_gmtoff

    # オフセットをtimedeltaに変換
    local_timezone = timezone(timedelta(seconds=offset_seconds))
    # ローカルタイムゾーンに変換
    return due_datetime.replace(tzinfo=local_timezone)
