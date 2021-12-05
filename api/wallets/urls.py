from django.urls import path

from . import views

app_name = "Django Bitcoin"
urlpatterns = [
    path("", views.IndexView.as_view(), name="BitcoinAddress"),
    path("<int:pk>/wallets/", views.DetailView.as_view(), name="Wallet"),
    path("<int:pk>/transaction/", views.ResultsView.as_view(), name="Transactions"),
    #   path("<int:question_id>/balance/", views.ResultsView(), name="Balance"),
]
