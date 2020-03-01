from django.db import models

from mask.core.models import TimeStampedModel
from mask.stores.models import Store


class Mailing(TimeStampedModel):
    email = models.EmailField("이메일 주소", max_length=254, unique=True)
    token = models.CharField("토큰", max_length=254)

class MailingHistory(models.Model):
    mailing = models.ForeignKey(Mailing, related_name='mailing_histories', on_delete=models.CASCADE)
    stores = models.ManyToManyField(Store)
    created_at = models.DateTimeField(auto_now_add=True)
