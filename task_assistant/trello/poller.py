import os, requests, time
from datetime import datetime, timezone
from dateutil.parser import isoparse
from ..db.dao import upsert_task, session
from ..db.models import Meta  # store cursor here
import logging

KEY   = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_API_TOKEN")
BOARD = os.getenv("TRELLO_BOARD_ID")
BASE  = "https://api.trello.com/1"

log = logging.getLogger("trello.poller")

def _get_cursor():
    with session() as s:
        meta = s.get(Meta, "trello_since") or Meta(key="trello_since", value="2025-01-01T00:00:00Z")
        return meta.value, meta

def _save_cursor(meta, ts):
    meta.value = ts
    with session() as s:
        s.merge(meta)
        s.commit()

def poll_once():
    since, meta = _get_cursor()
    url = f"{BASE}/boards/{BOARD}/actions"
    params = dict(key=KEY, token=TOKEN, since=since,
                  filter="createCard,updateCard,updateCard:idList,updateCard:closed")
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    log.info("Polled Trello: %d action(s) since %s", len(res.json()), since or "epoch")
    last_ts = since
    for act in reversed(res.json()):           # oldest first
        data  = act["data"]
        card  = data["card"]
        title = card["name"]
        due   = isoparse(card["due"]).astimezone(timezone.utc) if card.get("due") else None
        status= "done" if card.get("closed") else ("done" if data.get("listAfter", {}).get("name")=="Done" else "pending")
        upsert_task(card["id"], title, due, status)
        last_ts = act["date"]
    _save_cursor(meta, last_ts)
