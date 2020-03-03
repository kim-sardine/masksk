import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import F

from mask.stores.crawler import is_mask_available
from mask.stores.models import Store

logger = logging.getLogger(__name__)


def main_view(request):
    context = {}

    stores = Store.objects.prefetch_related('stock_histories').filter(is_visible=True).order_by('product_title')

    sort_dict = [
        {
            'value': '?sort=price',
            'title': '가격순',
            'selected': '',
        },
        {
            'value': '?sort=mall_title',
            'title': '쇼핑몰 이름순',
            'selected': '',
        },
        {
            'value': '/',
            'title': '최신 재고순',
            'selected': '',
        },
    ]

    sort = request.GET.get('sort', '')
    if sort == 'price':
        stores = stores.order_by(F('price').asc(nulls_last=True))
        sort_dict[0]['selected'] = 'selected'
    elif sort == 'mall_title':
        stores = stores.order_by('mall_title')
        sort_dict[1]['selected'] = 'selected'
    else:
        stores = stores.order_by(F('recent_in_stock_date').desc(nulls_last=True))
        sort_dict[2]['selected'] = 'selected'

    context['now_in_stock_stores'] = stores.filter(now_in_stock=True)
    context['not_in_stock_stores'] = stores.filter(now_in_stock=False)
    context['sort_dict'] = sort_dict

    datetime_korea = timezone.localtime()
    if datetime_korea.hour > 22 or datetime_korea.hour < 8:
        context['is_closed_time'] = True

    return render(request, 'stores/main.html', context)
