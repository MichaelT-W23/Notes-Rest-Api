from app import create_app
from db import db
import pytest
from dotenv import load_dotenv

load_dotenv()

_app = None

@pytest.fixture(scope="session")
def app():
    global _app

    test_app = create_app("testing")
    _app = test_app

    with test_app.app_context():
        db.create_all()
        yield test_app


# Clear table contents, without deleting table
def clear_database():
    meta = db.metadata

    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())

    db.session.commit()


def pytest_sessionfinish():
    global _app

    if _app is not None:
        with _app.app_context():
            clear_database()
