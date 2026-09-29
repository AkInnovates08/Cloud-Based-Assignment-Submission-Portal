import os
os.environ["DATABASE_URL"] = "sqlite:///./test_assignment_portal.db"
os.environ["STORAGE_DIR"] = "./test_storage"
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine
import pytest

@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c
