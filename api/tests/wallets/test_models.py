from django.test import TestCase

from wallets.models import Wallet

# Create your tests here.
class WalletTestCase(TestCase):
    def setUp(self):
        Wallet.objects.create(name="Wallet")


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
