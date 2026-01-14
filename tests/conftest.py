import os
import pytest
from fastapi.testclient import TestClient

# CRITICAL: Set this BEFORE importing app to prevent PostgreSQL connection attempt
# The app.database module tries to connect at import time, so we need a valid DB URL
os.environ["DATABASE_URL"] = "sqlite:///:memory:"


@pytest.fixture
def client():
    """
    Provide a FastAPI TestClient for API testing.
    
    Note: We set DATABASE_URL to SQLite in-memory above to prevent the app
    from trying to connect to PostgreSQL during import. Since all tests mock
    services/repositories, the database is never actually used.
    """
    from app.main import app
    
    with TestClient(app=app, base_url="http://test") as test_client:
        yield test_client
