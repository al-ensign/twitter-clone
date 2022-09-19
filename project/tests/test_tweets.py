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

