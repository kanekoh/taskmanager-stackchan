from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from dateutil.parser import isoparse
from ..db.dao import upsert_task

router = APIRouter()

class _Card(BaseModel):
    id: str
    name: str
    due: str | None = None
    closed: bool = False

@router.post("/trello")
async def trello_hook(req: Request):
    body = await req.json()
    action = body.get("action", {})
    data   = action.get("data", {})
    card   = _Card.model_validate(data.get("card", {}))

    # we only care about create/update/column-move actions
    if not card.id:
        raise HTTPException(400, "No card data")

    status = "done" if card.closed or data.get("list", {}).get("name") == "Done" else "pending"
    due_dt = isoparse(card.due).astimezone(tz=None) if card.due else None     # store local tz naive or utc

    upsert_task(card.id, card.name, due_dt, status)
    return {"ok": True}
