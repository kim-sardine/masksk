import logging

from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from mask.stores.crawler import is_mask_available
from mask.stores.models import Store
from mask.mailings.models import Mailing

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
            datetime_now = timezone.now()
            store.recent_in_stock_date = datetime_now
            store.create_stock_history(datetime_now)
    store.save()
    
    return f'{store} - {is_available}'


@celery_app.task()
def send_mailing():

    # 이전 X 시간 동안 재고가 없다가, 갑자기 재고가 생긴 store 를 찾는다.
    stores = Store.get_new_now_in_stock_store()

    # 해당 store 를 모아서 email 전송
    mailings = Mailing.objects.all()
    subject = '[마스크스크] 마스크 입고 알림'

    for mailing in mailings:
        email_data = {
            'stores' : stores,
            'mailing' : mailing
        }
        message = render_to_string('email/mailing_template.html', email_data)

        _send_mailing.delay(subject, message, [mailing.email])
        mailing.create_history(stores)


@celery_app.task()
def _send_mailing(subject, message, to):
    email_message = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, to)
    email_message.content_subtype = "html"  # Main content is now text/html
    email_message.send()
