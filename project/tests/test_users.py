import os
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
from django.conf import settings

if not settings.configured:
    django.setup()

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    client = APIClient()
    return client


def test_create_user(api_client, db):
    payload = dict(
        username="harry",
        name="Harry Potter",
        email="harry.potter@gmail.com",
        password="123456789"
    )

    response = api_client.post(path='/api/v1/users/', data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.get().name == "Harry Potter"


@pytest.mark.django_db
def test_token_created(api_client):
    user = dict(
        username="harry",
        name="Harry Potter",
        email="harry.potter@gmail.com",
        password="123456789"
    )
    api_client.post(path='/api/v1/users/', data=user)
    payload = dict(
        username="harry",
        password="123456789"
    )
    response = api_client.post(path='/api/v1/token', data=payload)
    assert response.status_code == status.HTTP_200_OK
