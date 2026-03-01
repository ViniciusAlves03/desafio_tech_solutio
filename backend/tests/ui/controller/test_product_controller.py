from app.ui.controller.product_controller import product_service

class TestProductController:

    def test_create_product(self, client, auth_headers, mocker):
        mocker.patch('app.app.redis_conn.get', return_value=None)
        mocker.patch.object(product_service, 'enqueue_create', return_value=None)

        payload = {"name": "Teclado", "price": "100.0", "brand": "Razer", "quantity": "10"}

        response = client.post('/v1/products', data=payload, headers=auth_headers)

        assert response.status_code == 202
        assert "Product creation queued" in response.get_json()["message"]

    def test_get_all_products(self, client, auth_headers, mocker, fake_product):
        mocker.patch('app.app.redis_conn.get', return_value=None)

        mock_result = {
            "items": [fake_product],
            "total": 1, "page": 1, "per_page": 10, "total_pages": 1
        }
        mocker.patch.object(product_service, 'get_all', return_value=mock_result)

        response = client.get('/v1/products?page=1&per_page=10', headers=auth_headers)

        assert response.status_code == 200
        assert response.get_json()["metadata"]["total"] == 1
        assert len(response.get_json()["items"]) == 1

    def test_get_product_by_id(self, client, auth_headers, mocker, fake_product):
        mocker.patch('app.app.redis_conn.get', return_value=None)
        mocker.patch.object(product_service, 'get_by_id', return_value=fake_product)

        response = client.get('/v1/products/1', headers=auth_headers)

        assert response.status_code == 200
        assert response.get_json()["name"] == "Teclado"

    def test_delete_product(self, client, auth_headers, mocker):
        mocker.patch('app.app.redis_conn.get', return_value=None)
        mocker.patch.object(product_service, 'enqueue_delete', return_value=None)

        response = client.delete('/v1/products/1', headers=auth_headers)

        assert response.status_code == 202

    def test_product_routes_without_token(self, client):
        assert client.get('/v1/products').status_code == 401
        assert client.post('/v1/products', data={}).status_code == 401
