import pytest
import json
from app.application.service.product_service import ProductService
from app.application.domain.exception.exceptions import NotFoundError, ForbiddenError
from app.utils.messages import Messages
from app.infrastructure.database.models.product_model import Product

class TestProductService:
    @pytest.fixture
    def mock_product_repository(self, mocker):
        return mocker.Mock()

    @pytest.fixture
    def product_service(self, mock_product_repository):
        return ProductService(product_repository=mock_product_repository)

    @pytest.fixture
    def fake_product(self):
        product = Product(id=1, name="Teclado", price=100.0, brand="Razer", quantity=10, user_id=1)
        return product

    def test_get_by_id_success(self, product_service, mock_product_repository, fake_product):
        mock_product_repository.get_by_id.return_value = fake_product

        result = product_service.get_by_id(1)

        assert result.name == "Teclado"
        mock_product_repository.get_by_id.assert_called_once_with(1)

    def test_get_by_id_not_found(self, product_service, mock_product_repository):
        mock_product_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError):
            product_service.get_by_id(99)

    def test_enqueue_create(self, product_service, mocker):
        mock_redis_rpush = mocker.patch('app.application.service.product_service.redis_conn.rpush')

        data = {
            "name": "Rato", "price": 50.5, "brand": "Logitech",
            "quantity": 5, "image_base64": "base64string", "image_mime_type": "image/png"
        }

        product_service.enqueue_create(data, current_user_id=1)

        mock_redis_rpush.assert_called_once()

        args, kwargs = mock_redis_rpush.call_args
        queue_name, json_message = args

        assert queue_name == 'product_tasks'
        message_dict = json.loads(json_message)
        assert message_dict["action"] == "create"
        assert message_dict["data"]["name"] == "Rato"
        assert message_dict["data"]["user_id"] == 1

    def test_enqueue_update_forbidden(self, product_service, mock_product_repository, fake_product):
        mock_product_repository.get_by_id.return_value = fake_product

        with pytest.raises(ForbiddenError) as exc_info:
            product_service.enqueue_update(product_id=1, data={"price": 120.0}, current_user_id=2)

        assert exc_info.value.message == Messages.Product.FORBIDDEN_UPDATE

    def test_enqueue_delete_success(self, product_service, mock_product_repository, fake_product, mocker):
        mock_product_repository.get_by_id.return_value = fake_product
        mock_redis_rpush = mocker.patch('app.application.service.product_service.redis_conn.rpush')

        product_service.enqueue_delete(product_id=1, current_user_id=1)

        mock_redis_rpush.assert_called_once()
        args, kwargs = mock_redis_rpush.call_args
        message_dict = json.loads(args[1])

        assert message_dict["action"] == "delete"
        assert message_dict["product_id"] == 1
