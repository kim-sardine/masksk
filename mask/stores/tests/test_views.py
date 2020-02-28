import pytest

from django.shortcuts import reverse

from mask.stores.models import Store
from mask.stores.tests.factories import StoreFactory

pytestmark = pytest.mark.django_db


class TestStoreMainView:

    def test_get_visible_store_only(self, client):

        StoreFactory.create_batch(2, is_visible=False)
        StoreFactory.create_batch(4, is_visible=True)

        response = client.get(reverse('home'))

        assert response.status_code == 200
        assert len(response.context.get('stores')) == 4
