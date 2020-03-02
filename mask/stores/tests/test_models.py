import pytest

from django.shortcuts import reverse
from django.utils import timezone

from mask.stores.models import Store
from mask.stores.tests.factories import StoreFactory, StockHistoryFactory

pytestmark = pytest.mark.django_db


class TestStockHistoryModel:

    def test_get_new_now_in_stock_store_find_first_comes_in(self, store):
        datetime_now = timezone.now()
        datetime_before_30_secs = datetime_now - timezone.timedelta(seconds=30)
        StockHistoryFactory.create(store=store, created_at=datetime_before_30_secs)

        stores = Store.get_new_now_in_stock_store()
        assert len(stores) == 0

        store.now_in_stock = True
        store.save()
        stores = Store.get_new_now_in_stock_store()
        assert len(stores) == 1

    def test_get_new_now_in_stock_store_pass_old_one(self, store):
        store.now_in_stock = True
        store.save()

        datetime_now = timezone.now()
        datetime_before_80_secs = datetime_now - timezone.timedelta(seconds=80)
        StockHistoryFactory.create(store=store, created_at=datetime_before_80_secs)

        stores = Store.get_new_now_in_stock_store()
        assert len(stores) == 0

    def test_get_new_now_in_stock_store_find_new_stock(self, store):
        store.now_in_stock = True
        store.save()

        datetime_now = timezone.now()
        datetime_before_3_hours = datetime_now - timezone.timedelta(hours=3)
        datetime_before_3_hours_1_min = datetime_now - timezone.timedelta(hours=3, minutes=1)
        StockHistoryFactory.create(store=store, created_at=datetime_before_3_hours)
        StockHistoryFactory.create(store=store, created_at=datetime_before_3_hours_1_min)

        stores = Store.get_new_now_in_stock_store()
        assert len(stores) == 0

        datetime_before_30_secondss = datetime_now - timezone.timedelta(seconds=30)
        StockHistoryFactory.create(store=store, created_at=datetime_before_30_secondss)
        stores = Store.get_new_now_in_stock_store()
        assert len(stores) == 1

        StockHistoryFactory.create(store=store, created_at=datetime_now)
        stores = Store.get_new_now_in_stock_store()
        assert len(stores) == 0

