from django.contrib import admin

from legals.models import CompanyLegal


class CompanyLegalAdmin(admin.ModelAdmin):
    list_display = ("company", "date_effective",)
    list_filter = ("company", "date_effective",)
    search_fields = ("company", "date_effective",)


admin.site.register(CompanyLegal, CompanyLegalAdmin)
