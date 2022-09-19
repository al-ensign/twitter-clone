import os
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
from django.conf import settings

if not settings.configured:
    django.setup()

from rest_framework import status
from django.contrib.auth import get_user_model
from tweets.models import Page, Tweet, Tag


User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_pages_list(auth_client, pages):
    response = auth_client.get("/api/v1/pages")

    assert isinstance(response.data, list)
    assert len(response.data) == 10
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_page_create(user, auth_client):
    payload = {
        "title": "string",
        "description": "string",
        "owner": user.id
    }
    response = auth_client.post(
        "api/v1/pages/",
        payload,
        format="json"
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_follow_public_page(
        admin_user,
        admin_client,
        public_page
):
    payload = {
        "page_id": public_page.id
    }
    response = admin_client.patch(
        f'api/v1/pages/{public_page.id}/send_follow_request_to_page/',
        payload,
        format="json"
    )
    target = Page.objects.filter(pk=public_page.id).first()

    assert response.status_code == status.HTTP_200_OK
    assert admin_user in target.followers.all()


@pytest.mark.django_db
def test_follow_private_page(
        admin_user,
        admin_client,
        private_page
):
    payload = {
        "page_id": private_page.id
    }
    response = admin_client.patch(
        f'api/v1/pages/{private_page.id}/send_follow_request_to_page/',
        payload,
        format="json"
    )
    target = Page.objects.filter(pk=private_page.id).first()

    assert response.status_code == status.HTTP_200_OK
    assert admin_user in target.follow_requests.all()


@pytest.mark.django_db
def test_accept_follow_request(
        user,
        admin_user,
        auth_client,
        follow_request_private_page
):
    payload = {
        "user_id": admin_user.id
    }
    response = auth_client.patch(
        f'api/v1/pages/{follow_request_private_page.id}/accept_follow_request/',
        payload,
        format="json"
    )

    target = Page.objects.filter(pk=follow_request_private_page.id).first()

    assert response.status_code == status.HTTP_200_OK
    assert admin_user in target.followers.all()
    assert admin_user not in target.follow_requests.all()


@pytest.mark.django_db
def test_tweet_create(
        auth_client,
        public_page
):
    payload = {
        "text": "string",
        "owner": public_page.id
    }

    response = auth_client.post(
        f"api/v1/tweets/",
        payload,
        format="json"
    )

    target = Tweet.objects.filter(owner=public_page.id).first()

    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(target, Tweet)
    assert target.text == "string"


@pytest.mark.django_db
def test_like_tweet(
        admin_client,
        admin_user,
        tweet
):
    payload = {
        "tweet_id": tweet.id
    }
    response = admin_client.patch(
        f'api/v1/tweets/{tweet.id}/like_tweet/',
        payload,
        format="json"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unlike_tweet(
        admin_client,
        admin_user,
        liked_tweet
):
    payload = {
        "tweet_id": liked_tweet.id
    }
    response = admin_client.patch(
        f'api/v1/tweets/{liked_tweet.id}/unlike_tweet/',
        payload,
        format="json"
    )

    assert response.status_code == status.HTTP_200_OK

