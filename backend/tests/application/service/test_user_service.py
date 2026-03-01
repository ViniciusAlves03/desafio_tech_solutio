import pytest
from app.application.service import UserService
from app.application.domain.exception import NotFoundError, ConflictError, ForbiddenError
from app.utils.messages import Messages

class TestUserService:
    @pytest.fixture
    def user_service(self, mock_user_repository):
        return UserService(user_repository=mock_user_repository)

    def test_get_by_id_success(self, user_service, mock_user_repository, fake_user):
        mock_user_repository.get_by_id.return_value = fake_user

        result = user_service.get_by_id(1)

        assert result.id == 1
        assert result.username == "testuser"
        mock_user_repository.get_by_id.assert_called_once_with(1)

    def test_get_by_id_not_found(self, user_service, mock_user_repository):
        mock_user_repository.get_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc_info:
            user_service.get_by_id(999)

        assert exc_info.value.message == Messages.User.NOT_FOUND_TITLE

    def test_create_user_success(self, user_service, mock_user_repository, fake_user):
        mock_user_repository.get_by_email.return_value = None
        mock_user_repository.get_by_username.return_value = None
        mock_user_repository.create.return_value = fake_user

        data = {"username": "testuser", "email": "test@email.com", "password": "senha"}

        result = user_service.create_user(data)

        assert result.email == "test@email.com"
        mock_user_repository.create.assert_called_once()

    def test_create_user_email_conflict(self, user_service, mock_user_repository, fake_user):
        mock_user_repository.get_by_email.return_value = fake_user

        data = {"username": "novo", "email": "test@email.com", "password": "senha"}

        with pytest.raises(ConflictError) as exc_info:
            user_service.create_user(data)

        assert exc_info.value.message == Messages.User.EMAIL_CONFLICT
        mock_user_repository.create.assert_not_called()

    def test_update_user_forbidden(self, user_service):
        with pytest.raises(ForbiddenError) as exc_info:
            user_service.update_user(user_id=2, current_user_id=1, data={"username": "hacker"})

        assert exc_info.value.message == Messages.User.FORBIDDEN_UPDATE
