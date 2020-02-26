from django.db import models

from mask.core.models import TimeStampedModel


class Store(TimeStampedModel):

    product_title = models.CharField(max_length=300)
    mall_title = models.CharField(max_length=100)
    price = models.DecimalField("낱개당 평균 가격", max_digits=13, decimal_places=3)
    product_url = models.URLField("상품 정보 URL", max_length=200)
    in_stock = models.BooleanField("현재 재고 여부", default=False)
    recent_in_stock_date = models.DateTimeField("최근 재고들어온 시간", blank=True, null=True)
    image_url = models.URLField("상품 이미지 URL", max_length=200, blank=True, null=True)
    crawling_type = models.CharField(max_length=50)

    def __str__(self):
        return product_title
