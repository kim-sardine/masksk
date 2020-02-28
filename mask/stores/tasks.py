import logging

from django.utils import timezone

from mask.stores.crawler import is_mask_available
from mask.stores.models import Store
from config import celery_app

logger = logging.getLogger(__name__)


@celery_app.task()
def update_mask_stock_for_all_store():

    for store in Store.objects.filter(is_visible=True):
        update_mask_stock.delay(store.id)

    return 'Go Sardine'


@celery_app.task()
def update_mask_stock(store_id):
    store = Store.objects.get(id=store_id)

    is_available = False
    try:
        is_available = is_mask_available(store)
    except Exception as e:
        logger.exception(f'[Crawling] : {store}')
        store.now_in_stock = False
    else:
        store.now_in_stock = is_available
        if is_available is True:
            store.recent_in_stock_date = timezone.now()
    store.save()
    
    return f'{store} - {is_available}'
