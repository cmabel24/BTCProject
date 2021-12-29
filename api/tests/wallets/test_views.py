from datetime import datetime
from typing import Dict, Mapping
from django.forms.fields import DateTimeField, EmailField
from django.http.response import HttpResponseBase
from django.test import TestCase


class IndexTests(TestCase):
    def test_transaction_view(self):
        self.assertListEqual(
            transaction=list,
            transaction=list,
            msg="Transaction not displayed correctly",
        )
class DetailTests(TestCase):
    def test_transaction_detail(self):
        self.
