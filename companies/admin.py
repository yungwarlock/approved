from django.contrib import admin

from companies.models import Company, CompanyRequest


admin.site.register(Company)
admin.site.register(CompanyRequest)
