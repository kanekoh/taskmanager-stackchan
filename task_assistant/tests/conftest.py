# tests/conftest.py
import pytest
from sqlmodel import SQLModel, create_engine, Session
from task_assistant.db import dao, models

@pytest.fixture(scope="function")
def mem_session(monkeypatch):
    # create new in-memory engine
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    # monkey-patch dao._engine so app code uses this DB
    monkeypatch.setattr(dao, "_engine", engine, raising=False)

    with Session(engine) as s:
        yield s            # tests receive a ready session
