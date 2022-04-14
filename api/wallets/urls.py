from re import template
from django.urls import path
from django.conf.urls import url
from . import views

app_name = "Django Bitcoin"
urlpatterns = [
    path("", views.IndexView.as_view(), name="BitcoinAddress"),
    path("<int:pk>/wallets/", views.DetailView.as_view(), name="Wallet"),
    path("<int:pk>/transaction/", views.ResultsView.as_view(), name="Transactions"),
    path("<int:pk>/create/", views.CreateUser.as_view(), name="CreateUser"),
    path("<int:question_id>/balance/", views.ResultsView.as_view(), name="Balance"),
    path("<int:uuid>/UserHomepage", views.UserHomepage.as_view(), name="UserHomepage"),
    url(r"^(?P<slug>[a-z0-9-_]+?)/$", views.page_details, name="details"),
    path("<int:pk>/simple/", views.Simple.as_view(), name="simple"),
]
