from django.contrib import admin

from keywords.models import KeywordBase


class KeywordBaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(KeywordBase, KeywordBaseAdmin)
