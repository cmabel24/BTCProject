"Librarys to generate random items to test"
from typing import Dict, List, Type
from typing_extensions import Self
from unittest import TestProgram
from django import test
from django.contrib.auth import get_user_model, login
from django.db.models.expressions import Value
from django.forms.fields import EmailField
from django.test import TestCase
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import BaseProvider
from wallets.models import PubKey, Transaction, Wallet
import factory

User = get_user_model()

SEED = "c4b49e22a03f6ddf1be4901177fdaa2f"
fake = Faker()

# Creating a Fake User to test logging in
class UsernameProvider(BaseProvider):
    """Username provider"""

    def username(self):  # pylint: disable=no-self-use
        """Random username"""
        return fake.email().rpartition("@")[0]


factory.Faker.add_provider(UsernameProvider)
fake.add_provider(UsernameProvider)


class UserFactory(DjangoModelFactory):
    """
    Create a randomly generated base user this can be extended by:
    UserFactory.build(is_staff=True)
    """

    email = factory.Faker("email")
    username = factory.Faker("username")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    wallet = factory.Faker("wallet")
    transaction = factory.Faker("transaction")
    wallets_page = factory.Faker("wallets_page")

    class Meta:
        """Meta Data"""

    model = User

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """Add the user groups"""
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)  # pylint: disable=no-


def create_user(**kwargs):
    """This will create a user model instance, and save it. It returns the user object with
    the raw password, while saving the hashed password"""
    user = UserFactory.create(**kwargs)
    password = user.password
    user.set_password(password)
    user.save()
    user.password = password
    return user


# Create your tests here.
class WalletTestCase(TestCase):
    def setUp(self):
        Wallet.objects.create(name="Wallet")


class PubKeyTestCase(TestCase):
    def test_logging_in(self):
        PubKey.validate_unique


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_details(self):
        response = self.client.get("/wallet/details/")
        self.assertEqual(response.status_code, 404)

    def test_index(self):
        response = self.client.get("/transaction/index/")
        self.assertEqual(response.status_code, 404)


class TransactionTestCase(TestCase):
    def test_ransaction(self):
        self.failIfEqual(0, 1)


class WalletRPCTestCase(TestProgram):
    def test_walletrpc(self):
        factory.Faker("wallet")
        factory.generate(Wallet, strategy=Faker)
