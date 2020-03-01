from django.contrib import admin

from mask.mailings.models import Mailing, MailingHistory

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("email", "token", "created_at",)

@admin.register(MailingHistory)
class MailingHistoryAdmin(admin.ModelAdmin):
    list_display = ("mailing", "get_stores", "created_at",)

    def get_stores(self, obj):
        return ",".join([store.product_title for store in obj.stores.all()])