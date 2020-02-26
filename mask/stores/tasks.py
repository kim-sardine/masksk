from config import celery_app

@celery_app.task()
def get_store_info():
    return None