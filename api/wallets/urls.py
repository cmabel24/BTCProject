from django.urls import path

from . import views

app_name = "Django Bitcoin"
urlpatterns = [
    path("", views.IndexView.as_view(), name="Addresses"),
    path("<int:pk>/", views.DetailView.as_view(), name="Payments"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="Transactions"),
    path("<int:question_id>/vote/", views.vote, name="Wallets"),
]
