"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import include, path
from wallets import urls as page_urls
from django.conf.urls import include, url
from wallets import urls as create_urls
from wallets import urls as access_urls

urlpatterns = [
    path("wallets/", include("wallets.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    url(r"^page/", include((page_urls, "page"), namespace="page")),
    url(r"^create/", include((create_urls, "create"), namespace="createuser")),
    url(r"^access/", include((access_urls, "access"), namespace="accessuser")),
]
