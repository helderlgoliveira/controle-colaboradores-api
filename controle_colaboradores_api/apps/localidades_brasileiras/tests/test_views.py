import json
import pytest
from model_bakery import baker

from ..models import Municipio


from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def api_client_forced_csrf():
    return APIClient(enforce_csrf_checks=True)

# TODO https://dev.to/sherlockcodes/pytest-with-django-rest-framework-from-zero-to-hero-8c4#:~:text=Now%2C%20let%27s%20proceed%20to%20test%20all%20endpoints%3A
#  https://www.django-rest-framework.org/api-guide/testing/#apiclient
#  https://stackoverflow.com/a/23091705 (test viewset)


