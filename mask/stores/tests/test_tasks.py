import pytest
from celery.result import EagerResult

from mask.stores.tests.factories import StoreFactory
from mask.stores.tasks import update_mask_stock
from mask.stores.crawler import is_mask_available


@pytest.mark.django_db
def test_tasks(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True

    test_sets = [
        {
            'crawling_type': 'naver_smart_store_1',
            'product_url': 'https://smartstore.naver.com/hanmaumsusan/products/4255775982',
        },
        {
            'crawling_type': 'kakao_store_1',
            'product_url': 'https://store.kakao.com/maeilecommerce/products/48207905',
        },
    ]

    for test_set in test_sets:
        store = StoreFactory(
            crawling_type=test_set['crawling_type'],
            product_url=test_set['product_url']
        )
        assert store.now_in_stock == False
        assert store.recent_in_stock_date is None

        is_available = is_mask_available(store)
        assert is_available == True

        task_result = update_mask_stock.delay(store.id)
        assert isinstance(task_result, EagerResult)
        assert task_result.result == f'{store} - {is_available}'
        store.refresh_from_db()
        
        assert store.now_in_stock == True
        assert store.recent_in_stock_date is not None
