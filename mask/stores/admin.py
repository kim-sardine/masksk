from django.contrib import admin

from mask.stores.models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("product_title", "crawling_type", "now_in_stock", "recent_in_stock_date", "is_visible", "modified_at", )
