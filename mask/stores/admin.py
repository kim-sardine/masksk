from django.contrib import admin

from mask.stores.models import Store, StockHistory


def set_is_visible(self, request, queryset):
    queryset.update(is_visible=True)
set_is_visible.short_description = '크롤링, 공개 설정'

def unset_is_visible(self, request, queryset):
    queryset.update(is_visible=False)
unset_is_visible.short_description = '크롤링, 공개 해제'

def delete_stock_history(self, request, queryset):
    queryset.update(recent_in_stock_date=None)
    for store in queryset:
        store.stock_histories.all().delete()
delete_stock_history.short_description = '최근 재고 시간 및 재고 기록 삭제'



@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("product_title", "crawling_type", "now_in_stock", "is_visible", "price", "recent_in_stock_date", "modified_at", )

    actions = [set_is_visible, unset_is_visible, delete_stock_history]


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ("store", "created_at",)
