from sqlalchemy import text

def test_users_table_exists(db):
    result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users';"))
    assert result.fetchone() is not None

