import pytest
from django.test import RequestFactory

from mask.users.models import User
from mask.users.tests.factories import UserFactory
from mask.stores.models import Store
from mask.stores.tests.factories import StoreFactory

@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def store() -> Store:
    return StoreFactory()
