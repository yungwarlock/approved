from django.contrib import admin
from django.urls import path, include


handler404 = 'web.views.custom_page_not_found_view'

urlpatterns = [
    path("", include("web.urls")),
    path("admin/", admin.site.urls),
]
