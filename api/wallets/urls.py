from re import template
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = "Django Bitcoin"
urlpatterns = [
    path("", views.IndexView.as_view(), name="wallet_list"),
    path("<uuid:pk>/", views.TransactionListView.as_view(), name="wallet_detail"),
    path('create.html', views.CreateSeedPhrase.as_view(), name="CreateSeedPhrase"),
    # path("<int:pk>/transaction/", views.ResultsView.as_view(), name="Transactions"),
    # path("<int:question_id>/balance/", views.ResultsView.as_view(), name="Balance"),
    # path("<int:uuid>/UserHomepage", views.UserHomepage.as_view(), name="UserHomepage"),
    # url(r"^(?P<slug>[a-z0-9-_]+?)/$", views.page_details, name="details"),
    # path("sections/<int:num>", views.section, name="section"),
    
]
