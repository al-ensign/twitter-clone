import pytest
from rest_framework.test import APIClient
import factory
import test_factory

from tweets.models import Page, Tweet
from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    user = User.objects.create_user(
        username="harry",
        name="Harry Potter",
        email="harry.potter@gmail.com",
        password="123456789"
    )
    return user


@pytest.fixture()
def auth_client(user, client):
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {user.token}'
    )
    return client


@pytest.fixture()
def admin_user(db):
    user = User.objects.create_superuser(
        username="ron",
        name="Ron Weasley",
        email="ron.weasley@gmail.com",
        password="123456789",
        role="admin"
    )
    return user


@pytest.fixture()
def admin_client(admin_user, client):
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {admin_user.token}'
    )
    return client


@pytest.fixture()
def private_page(user):
    return test_factory.PageFactory(
        owner=user,
        is_private=True
    )


@pytest.fixture()
def public_page(user):
    return test_factory.PageFactory(
        owner=user,
        is_private=False
    )


@pytest.fixture()
def pages():
    return test_factory.PageFactory.create_batch(10)


@pytest.fixture()
def follow_request_private_page(private_page, admin_user):
    private_page.follow_requests.add(admin_user)
    return private_page


@pytest.fixture()
def follow_request_public_page(
        public_page,
        admin_user,
        admin_client
):
    test_factory.PageFactory.create_batch(10, page=public_page)
    response = admin_client.get(f'pages/{public_page.id}/send_follow_request_to_page/')
    target = Page.objects.filter(pk=public_page.id).first()
    return target


@pytest.fixture()
def tweet(public_page):
    return test_factory.TweetFactory(
        owner=public_page
    )


@pytest.fixture()
def like_tweet(
        admin_user,
        admin_client,
        tweet
):
    response = admin_client.patch(f'/tweets/{tweet.id}/like_tweet/')
    target = Tweet.objects.filter(pk=tweet.id).first()
    return target

