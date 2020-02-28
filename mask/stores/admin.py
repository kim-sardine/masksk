from django.contrib import admin

from mask.stores.models import Store


def set_is_visible(self, request, queryset):
    queryset.update(is_visible=True)
set_is_visible.short_description = '크롤링, 공개 설정'

def unset_is_visible(self, request, queryset):
    queryset.update(is_visible=False)
unset_is_visible.short_description = '크롤링, 공개 해제'

def delete_recent_in_stock_date(self, request, queryset):
    queryset.update(recent_in_stock_date=None)
delete_recent_in_stock_date.short_description = '최근 재고 시간 삭제'


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("product_title", "crawling_type", "now_in_stock", "recent_in_stock_date", "is_visible", "modified_at", )

    actions = [set_is_visible, unset_is_visible, delete_recent_in_stock_date]
