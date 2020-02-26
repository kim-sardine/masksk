from config import celery_app

@celery_app.task()
def get_stock_info():
    return None