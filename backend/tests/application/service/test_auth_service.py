import pytest
from app.application.service.auth_service import AuthService
from app.application.domain.exception.exceptions import AuthenticationError
from app.utils.messages import Messages

class TestAuthService:
    @pytest.fixture
    def auth_service(self, mock_user_repository):
        return AuthService(user_repository=mock_user_repository)

    def test_login_success(self, auth_service, mock_user_repository, fake_user, mocker):
        mock_user_repository.get_by_login_input.return_value = fake_user

        mocker.patch.object(fake_user, 'check_password', return_value=True)

        mock_create_token = mocker.patch('app.application.service.auth_service.create_access_token', return_value="token_falso_123")

        result = auth_service.login("test@email.com", "senha_correta")

        assert result["access_token"] == "token_falso_123"
        assert result["user"]["email"] == "test@email.com"
        mock_create_token.assert_called_once()

    def test_login_invalid_credentials(self, auth_service, mock_user_repository):
        mock_user_repository.get_by_login_input.return_value = None

        with pytest.raises(AuthenticationError) as exc_info:
            auth_service.login("errado@email.com", "senha")

        assert exc_info.value.message == Messages.Auth.INVALID_CREDENTIALS

    def test_logout_success(self, auth_service, mocker):
        mock_redis_set = mocker.patch('app.application.service.auth_service.redis_conn.set')

        auth_service.logout("jti_do_token_123")

        mock_redis_set.assert_called_once()
