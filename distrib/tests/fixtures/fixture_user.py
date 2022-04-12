import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser',
        password='1234567',
        email='test@mail.mail',
        first_name='first_test',
        last_name='last_test'
    )


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client
