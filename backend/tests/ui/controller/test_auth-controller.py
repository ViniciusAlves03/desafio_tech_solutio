from app.ui.controller.auth_controller import auth_service
from app.application.domain.exception.exceptions import AuthenticationError

class TestAuthController:

    def test_login_success(self, client, mocker):
        mocker.patch.object(auth_service, 'login', return_value={
            "access_token": "token_mockado_123"
        })

        response = client.post('/v1/auth/login', json={"login": "admin@email.com", "password": "123"})

        assert response.status_code == 200
        assert response.get_json()["access_token"] == "token_mockado_123"

    def test_login_missing_fields(self, client):
        response = client.post('/v1/auth/login', json={"login": "admin@email.com"})
        assert response.status_code == 400

    def test_login_wrong_credentials(self, client, mocker):
        mocker.patch.object(auth_service, 'login', side_effect=AuthenticationError("Credenciais inválidas"))

        response = client.post('/v1/auth/login', json={"login": "errado", "password": "123"})
        assert response.status_code == 401

    def test_logout_success(self, client, auth_headers, mocker):
        mocker.patch('app.app.redis_conn.get', return_value=None)
        mocker.patch.object(auth_service, 'logout', return_value=None)

        response = client.post('/v1/auth/logout', headers=auth_headers)
        assert response.status_code == 200
