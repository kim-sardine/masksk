import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.db.models import F
from django.contrib import messages

from mask.stores.crawler import is_mask_available
from mask.stores.models import Store

logger = logging.getLogger(__name__)

@cache_page(60)
def main_view(request):
    context = {}

    stores = Store.objects.prefetch_related('stock_histories').filter(is_visible=True) \
        .order_by(
            '-now_in_stock', 
            F('recent_in_stock_date').desc(nulls_last=True)
        )
    context['stores'] = stores

    datetime_korea = timezone.localtime()
    if datetime_korea.hour > 22 or datetime_korea.hour < 8:
        context['is_closed_time'] = True

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
                datetime_now = timezone.now()
                store.recent_in_stock_date = datetime_now
                store.create_stock_history(datetime_now)
        store.save()

    return HttpResponse(f'{succeed + failed} / {succeed} / {failed}')
