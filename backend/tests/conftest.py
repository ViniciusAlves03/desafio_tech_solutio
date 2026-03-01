import sys
import os
import pytest
from unittest.mock import Mock

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "super_secret_test_key_that_is_at_least_32_bytes_long"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import create_app
from app.infrastructure.database.models.user_model import User
from app.infrastructure.database.models.product_model import Product

@pytest.fixture
def app(mocker):
    mocker.patch('app.app.db.create_all')

    app = create_app()
    app.config.update({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(app):
    from flask_jwt_extended import create_access_token
    with app.app_context():
        token = create_access_token(identity="1")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def fake_user():
    user = User(id=1, username="testuser", email="test@email.com")
    user.password_hash = "hashed_password_123"
    return user

@pytest.fixture
def fake_product():
    return Product(id=1, name="Teclado", price=100.0, brand="Razer", quantity=10, user_id=1)

@pytest.fixture
def mock_user_repository():
    return Mock()
