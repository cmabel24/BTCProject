from re import template
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = "Django Bitcoin"
urlpatterns = [
    path("", views.IndexView.as_view(), name="wallet_list"),
    path("<uuid:pk>/", views.TransactionListView.as_view(), name="wallet_detail"),
    path('create.html', views.CreateSeedPhrase.as_view(), name="CreateSeedPhrase"),
]
