from db import db
import pytest
from sqlalchemy import text

@pytest.mark.order(5)
def test_database_connection(app):
    with app.app_context():
        result = db.session.execute(text("SELECT * FROM Users LIMIT 1;"))
        first_row = result.fetchone()
        assert first_row is not None, "Database returned no data!"
