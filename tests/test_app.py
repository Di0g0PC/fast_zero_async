from http import HTTPStatus

from fast_zero.schemas import UserPublic

# def test_read_root_deve_retornar_ok_eola_mundo(client):
#     response = client.get('/')  # ACT (ação) - chama o endpoint '/'
#     assert response.status_code == HTTPStatus.OK  # Assert
#     assert response.json() == {'message': 'Hello World'}  # Assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }  # Assert


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    # Valida os dados vindos do SQLAlchemy pelos atributos e
    # passa para o formato de pydantic
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '123',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testusername2',
        'id': user.id,
        'email': 'test@test.com',
    }


# def test_update_user_id_low(client):
#     response = client.put(
#         '/users/0',
#         json={
#             'password': '123',
#             'username': 'testusername2',
#             'email': 'test@test.com',
#         },
#     )

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'acess_token' in token


# def test_read_user_id_normal(client):
#     response = client.get('/users/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'username': 'testusername2',
#         'email': 'test@test.com',
#         'id': 1,
#     }


# def test_read_user_id_low(client):
#     response = client.get('/users/0')

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}

# def test_delete_user_id_low(client):
#     response = client.delete('/users/0')

#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}
