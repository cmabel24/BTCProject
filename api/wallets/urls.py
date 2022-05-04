from re import template
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = "Django Bitcoin"
urlpatterns = [
    path("", views.IndexView.as_view(), name="wallet_list"),
    path("<int:pk>/", views.TransactionListView.as_view(), name="wallet_detail"),
    path('create/', views.CreateSeedPhrase.as_view(), name="CreateSeedPhrase"),
    path("<int:pk>/recieve/", views.RecieveView.as_view(), name="wallet_recieve"),
    path("<int:pk>/send/", views.SendView.as_view(), name="wallet_send"),
]
