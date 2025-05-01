from sqlmodel import SQLModel, Field
from datetime import datetime

class Task(SQLModel, table=True):
    id: str = Field(primary_key=True)       # Trello card id
    title: str
    due: datetime | None = None             # stored UTC
    status: str = "pending"                 # pending / done
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    reminded_at: datetime | None = None   # NEW

class Meta(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str