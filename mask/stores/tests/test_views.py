import pytest

from django.shortcuts import reverse

from mask.stores.models import Store
from mask.stores.tests.factories import StoreFactory

pytestmark = pytest.mark.django_db


class TestStoreMainView:

    def test_get_visible_store_only(self, client):

        StoreFactory.create_batch(2, is_visible=False)
        StoreFactory.create_batch(4, is_visible=True, now_in_stock=True)
        StoreFactory.create_batch(8, is_visible=True, now_in_stock=False)

        response = client.get(reverse('home'))

        assert response.status_code == 200
        assert len(response.context.get('now_in_stock_stores')) == 4
        assert len(response.context.get('not_in_stock_stores')) == 8

    def test_sort(self, client):

        response = client.get(reverse('home'))

        assert response.status_code == 200
        assert len(response.context.get('sort_dict')) == 3
