import pytest
from unittest.mock import patch
from celery.result import EagerResult
from bs4 import BeautifulSoup

from mask.stores.models import Store
from mask.stores.tests.factories import StoreFactory
from mask.stores.tasks import update_mask_stock
from mask.stores.crawler import is_mask_available

@pytest.mark.django_db
def test_naver_smart_store_1(settings):
    store = StoreFactory(crawling_type='naver_smart_store_1')
    store.product_url = 'https://smartstore.naver.com/hanmaumsusan/products/4507955734'
    store.save()

    is_available = is_mask_available(store)
    assert is_available == True

    settings.CELERY_TASK_ALWAYS_EAGER = True
    task_result = update_mask_stock.delay(store.id)
    assert isinstance(task_result, EagerResult)
    assert task_result.result == f'{store} - {is_available}'
    assert store.now_in_stock == True
