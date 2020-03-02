from django.db import models
from django.utils import timezone

from mask.core.models import TimeStampedModel


class Store(TimeStampedModel):
    MASK_TYPE = [
        ('N95', 'N95'),
        ('KF99', 'KF99'),
        ('KF94', 'KF94'),
        ('KF80', 'KF80'),
        ('면', '면'),
        ('천', '천'),
        ('기타', '기타'),
    ]

    # 수작업
    product_title = models.CharField("상품명", max_length=300)
    mall_title = models.CharField("쇼핑몰 이름", max_length=100)

    product_url = models.URLField("상품 정보 URL", max_length=200)
    image_url = models.URLField("상품 이미지 URL", max_length=200, blank=True, null=True)

    mask_type = models.CharField("마스크 종류", max_length=50, choices=MASK_TYPE, blank=True, null=True)
    price = models.DecimalField("낱개당 평균 가격", max_digits=13, decimal_places=3)
    size = models.CharField("마스크 사이즈", max_length=50, blank=True, null=True)

    crawling_type = models.CharField("크롤링 유형", max_length=50)

    is_visible = models.BooleanField("페이지 공개 여부", default=False)

    # 크롤링
    now_in_stock = models.BooleanField("현재 재고 있는지", default=False)
    recent_in_stock_date = models.DateTimeField("최근 재고들어온 시간", blank=True, null=True)

    def __str__(self):
        return self.product_title

    @property
    def card_class(self):
        if self.now_in_stock:
            return 'my-card-now-in-stock'
        return 'my-card-not-in-stock'

    @property
    def alert_class(self):
        if self.now_in_stock:
            return 'my-alert-now-in-stock'
        return 'my-alert-not-in-stock'

    @property
    def now_in_stock_display(self):
        if self.now_in_stock:
            return '재고 있음'
        return '재고 없음'

    @property
    def mask_type_badge_class(self):
        mask_type = self.mask_type
        if mask_type:
            if mask_type == 'N95' :
                return 'badge-primary'
            elif mask_type.startswith('KF'):
                return 'badge-success'
            elif mask_type in ['면', '천']:
                return 'badge-info'
        return 'badge-secondary'

    @property
    def price_badge_class(self):
        price = self.price
        if price:
            if price > 3000 :
                return 'badge-danger'
            elif price > 2000:
                return 'badge-warning'
            elif price > 1000:
                return 'badge-success'
        return 'badge-primary'

    def create_stock_history(self, datetime):
        StockHistory.objects.create(store=self, created_at=datetime)

    @classmethod
    def get_new_now_in_stock_store(cls):
        result = []

        stores = cls.objects.prefetch_related('stock_histories').filter(is_visible=True, now_in_stock=True)
        for store in stores:
            try:  # TODO: 함수로 묶기
                if store.stock_histories.exists():
                    time_diff = timezone.now() - store.stock_histories.first().created_at  # 방금 재고가 들어왔는지 검사
                    if time_diff.total_seconds() < 60:  # 방금 들어온 재고만 본다
                        if store.stock_histories.count() == 1:  # 처음 들어온 재고일 때 -> Hit
                            result.append(store)
                        else:  # 재고 기록이 다수일 때
                            stock_history = store.stock_histories.all()
                            time_diff = stock_history[0].created_at - stock_history[1].created_at  # 최근 두 재고 기록 비교
                            hours = time_diff.total_seconds() // 3600
                            if hours >= 2:  # 2시간 이상 재고가 없다가 재고가 들어오면 -> Hit
                                result.append(store)
            except:  # TODO: Logging
                continue
        return result

class StockHistory(models.Model):
    store = models.ForeignKey(Store, related_name='stock_histories', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.store} ({self.created_at})'
    