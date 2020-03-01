from django.contrib import admin

from mask.mailings.models import Mailing, MailingHistory

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("email", "token", "created_at",)
