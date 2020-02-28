import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page

from mask.stores.crawler import is_mask_available
from mask.stores.models import Store

logger = logging.getLogger(__name__)

@cache_page(60)
def main_view(request):
    context = {}

    stores = Store.objects.filter(is_visible=True)
    context['stores'] = stores

    return render(request, 'stores/main.html', context)

def dummy_view(request):
    """
    특정 시간마다(1분?) 실행 예정.
    모든 상품들의 재고 여부를 확인한다.
    """
    succeed = 0
    failed = 0

    for store in Store.objects.filter(is_visible=True):
        is_available = False
        try:
            is_available = is_mask_available(store)
            print(f'{store} - {is_available}')
        except Exception as e:
            failed += 1
            logger.exception(f'[Crawling] : {store}')
            store.now_in_stock = False
        else:
            succeed += 1
            store.now_in_stock = is_available
            if is_available is True:
                store.recent_in_stock_date = timezone.now()
        store.save()

    return HttpResponse(f'{succeed + failed} / {succeed} / {failed}')
