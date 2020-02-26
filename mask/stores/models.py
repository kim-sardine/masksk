from django.db import models

from mask.core.models import TimeStampedModel


class Store(TimeStampedModel):

    # 수작업
    product_title = models.CharField("상품명", max_length=300)
    mall_title = models.CharField("쇼핑몰 이름", max_length=100)

    product_url = models.URLField("상품 정보 URL", max_length=200)
    image_url = models.URLField("상품 이미지 URL", max_length=200, blank=True, null=True)

    price = models.DecimalField("낱개당 평균 가격", max_digits=13, decimal_places=3)

    crawling_type = models.CharField("크롤링 유형(id)", max_length=50)

    # 크롤링
    now_in_stock = models.BooleanField("현재 재고 있는지", default=False)
    recent_in_stock_date = models.DateTimeField("최근 재고들어온 시간", blank=True, null=True)

    def __str__(self):
        return product_title
