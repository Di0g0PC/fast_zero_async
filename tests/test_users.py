from http import HTTPStatus

from fast_zero.schemas import UserPublic

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


def test_duplicate_username(client):
    client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test1@test.com',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert
    assert response.json() == {'detail': 'Username already exists'}


def test_duplicate_email(client):
    client.post(
        '/users/',
        json={
            'username': 'testusername1',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'testusername123',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert
    assert response.json() == {'detail': 'Email already exists'}


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


def test_update_wrong_user(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '123',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}


def test_delete_wrong_user(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
