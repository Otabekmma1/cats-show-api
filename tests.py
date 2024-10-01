import os
import django
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from cats.models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CatsShow.settings')
django.setup()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def create_user():
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def create_breed():
    return Breed.objects.create(name='Siamese')

@pytest.fixture
def create_cat(create_user, create_breed):
    return Cat.objects.create(name='Kitty', breed=create_breed, age=2, color='white', owner=create_user)

@pytest.fixture
def jwt_token(client, create_user):
    response = client.post('/api/v1/token/', {
        'username': 'testuser',
        'password': '12345'
    })
    return response.data['access']

@pytest.mark.django_db
def test_get_cats(client, jwt_token, create_cat):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    response = client.get('/api/v1/cats/')
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db
def test_create_cat(client, jwt_token, create_breed):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    initial_count = Cat.objects.count()

    data = {
        'name': 'Tommy',
        'breed': create_breed.id,
        'age': 3,
        'color': 'black'
    }

    response = client.post('/api/v1/cats/', data, format='json')
    assert response.status_code == 201
    assert Cat.objects.count() == initial_count + 1

@pytest.mark.django_db
def test_update_cat(client, jwt_token, create_cat):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    data = {'name': 'Updated Kitty'}
    response = client.patch(f'/api/v1/cats/{create_cat.id}/', data, format='json')
    assert response.status_code == 200
    create_cat.refresh_from_db()
    assert create_cat.name == 'Updated Kitty'

@pytest.mark.django_db
def test_delete_cat(client, jwt_token, create_cat):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    response = client.delete(f'/api/v1/cats/{create_cat.id}/')
    assert response.status_code == 204
    assert Cat.objects.count() == 0

@pytest.mark.django_db
def test_breed_view_set(client, jwt_token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt_token}')
    response = client.get('/api/v1/breeds/')
    assert response.status_code == 200
