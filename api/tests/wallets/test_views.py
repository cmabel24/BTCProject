from cgitb import html
from datetime import datetime
from typing import Dict, Mapping
from django.forms.fields import DateTimeField, EmailField
from django.http import HttpResponseNotFound, StreamingHttpResponse
from django.http.response import HttpResponseBase
from django.test import TestCase
from wallets.views import transaction


class DetailTests(TestCase):
    def test_transaction_detail(self):
        self.assertContains(
            StreamingHttpResponse, text=html, count=1, status_code=HttpResponseNotFound
        )
        self.failIf(expr=bool, msg="No Transaction Shown")
