from app.ui.controller.user_controller import user_service

class TestUserController:

    # def test_get_all_users_route(self, client, auth_headers, mocker, fake_user):
    #     mocker.patch('app.app.redis_conn.get', return_value=None)
    #     mocker.patch.object(user_service, 'get_all', return_value=[fake_user])

    #     response = client.get('/v1/users', headers=auth_headers)

    #     assert response.status_code == 200
    #     assert len(response.get_json()) == 1

    def test_get_user_by_id(self, client, auth_headers, mocker, fake_user):
        mocker.patch('app.app.redis_conn.get', return_value=None)
        mocker.patch.object(user_service, 'get_by_id', return_value=fake_user)

        response = client.get('/v1/users/1', headers=auth_headers)

        assert response.status_code == 200
        assert response.get_json()["username"] == "testuser"

    def test_create_user_success(self, client, mocker, fake_user):
        mocker.patch.object(user_service, 'create_user', return_value=fake_user)
        payload = {"username": "novouser", "email": "novo@email.com", "password": "senha123"}

        response = client.post('/v1/users', json=payload)

        assert response.status_code == 201
        assert "Location" in response.headers

    def test_create_user_invalid_data(self, client):
        payload = {"username": "novo", "email": "novo@email.com"}
        response = client.post('/v1/users', json=payload)

        assert response.status_code == 400

    def test_update_user(self, client, auth_headers, mocker, fake_user):
        mocker.patch('app.app.redis_conn.get', return_value=None)
        mocker.patch.object(user_service, 'update_user', return_value=fake_user)

        response = client.patch('/v1/users/1', json={"username": "alterado"}, headers=auth_headers)

        assert response.status_code == 200

    def test_delete_user(self, client, auth_headers, mocker):
        mocker.patch('app.app.redis_conn.get', return_value=None)
        mocker.patch.object(user_service, 'delete_user', return_value=None)

        response = client.delete('/v1/users/1', headers=auth_headers)

        assert response.status_code == 204
