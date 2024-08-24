from django.urls import path

from web import views

urlpatterns = [
    path("", views.index),
    path("company/<str:slug>", views.company_detail),
]
