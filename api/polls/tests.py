from django.test import TestCase

from views.py import Wallet

# Create your tests here.
class WalletTestCase(TestCase):
    def setUp(self):
        Wallet.objects.create(name="Wallet")
