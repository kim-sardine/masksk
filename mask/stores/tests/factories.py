from django.utils import timezone
from factory import DjangoModelFactory, Faker, fuzzy, SubFactory

from mask.stores.models import Store, StockHistory


class StoreFactory(DjangoModelFactory):

    product_title = Faker("sentence", nb_words=8)
    mall_title = Faker("sentence", nb_words=2)
    product_url = Faker("url")
    image_url = Faker("url")

    mask_type = fuzzy.FuzzyChoice(['KF99', 'KF80', '면', '기타'])
    price = fuzzy.FuzzyDecimal(800, 3000)
    size = fuzzy.FuzzyChoice(['대', '대,중', '중,소', '소'])

    crawling_type = fuzzy.FuzzyChoice(['naver_smart_store_1', 'kakao_store_1'])

    is_visible = True

    now_in_stock = False
    recent_in_stock_date = None

    class Meta:
        model = Store


class StockHistoryFactory(DjangoModelFactory):

    store = SubFactory(StoreFactory)
    created_at = Faker("date_time_this_month", tzinfo=timezone.utc)
    
    class Meta:
        model = StockHistory
