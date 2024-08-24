from django.urls import path

from web import views

urlpatterns = [
    path("", views.index, name="home"),
    path("request", views.request_company, name="request_company"),
    path("company/<str:slug>", views.company_detail, name="company_detail"),
]
