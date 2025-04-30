from task_assistant.util.time import utcnow
def test_utcnow_has_tz():
    assert utcnow().tzinfo is not None
