from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from mask.stores.crawler import run
from mask.stores.models import Store


def dummy_view(request):
    """
    특정 시간마다(1분?) 실행 예정.
    모든 상품들의 재고 여부를 확인한다.
    """
    for store in Store.objects.all():
        try:
            now_in_stock = run(store)
        except Exception as e:
            # TODO: 크롤링 실패 -> Error logging or DB writing
            print(store)
            print(e)
        else:
            store.now_in_stock = now_in_stock
            print(now_in_stock)
            if now_in_stock is True:
                store.recent_in_stock_date = timezone.now()
                print(store.recent_in_stock_date)
            store.save()

    return HttpResponse('done')
