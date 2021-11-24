import uuid
from django.contrib.auth import get_user_model
import datetime
import random
import hashlib
import base64
import pytz
from decimal import Decimal
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# from django_bitcoin.utils import *
# from django_bitcoin.utils import bitcoind
# from django_bitcoin import settings

from django.utils.translation import ugettext as _

import django.dispatch

# import jsonrpc

# from BCAddressField import is_valid_btc_address

from django.db import transaction as db_transaction
from celery import task

# from distributedlock import distributedlock, MemcachedLock, LockNotAcquiredError
from django.db.models import Avg, Max, Min, Sum


balance_changed = django.dispatch.Signal(
    providing_args=["changed", "transaction", "bitcoinaddress"]
)
balance_changed_confirmed = django.dispatch.Signal(
    providing_args=["changed", "transaction", "bitcoinaddress"]
)


@task()
def update_wallet_balance(wallet_id):
    w = Wallet.objects.get(id=wallet_id)
    Wallet.objects.filter(id=wallet_id).update(last_balance=w.total_balance_sql())


User = get_user_model()


class Key(models.Model):
    id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="keys")
    name = models.CharField(max_length=64)


class PubKey(models.Model):
    id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    key = models.ForeignKey(Key, on_delete=models.CASCADE, related_name="pub_keys")
    xpub1 = models.CharField(max_length=130, unique=True)

    {
        "name": "Copeland - Wallet",
        "addressType": "P2SH-P2WSH",
        "network": "mainnet",
        "client": {
            "type": "private",
            "url": "http://bitcoind.localhost:8080",
            "username": "cmabel",
        },
        "quorom": {
            "requiredSigners": 1,
            "totalSigners": 1,
        },
        "extendedPublicKeys": [{}],
    }


class Wallet(models.Model):
    id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField()

    def update_last_balance(self, amount):
        if (
            self.__class__.objects.filter(
                id=self.id, last_balance=self.last_balance
            ).update(last_balance=(self.last_balance + amount))
            < 1
        ):
            update_wallet_balance.apply_async((self.id,), countdown=1)

    def save(self, *args, **kwargs):
        """No need for labels."""
        self.updated_at = datetime.datetime.now()
        super(Wallet, self).save(*args, **kwargs)
        # super(Wallet, self).save(*args, **kwargs)

    keys = models.ManyToManyField(PubKey, related_name="wallet")
    name = models.TextField(unique=True)
    addressType = models.TextField(max_length=9)
    network = models.TextField(max_length=7, unique=True)
    # "Client"
    type = models.Choices("private", "public")
    url = models.URLField("http://bitcoind.localhost:8080")
    username = models.TextField(unique=True, max_length=20)
    # "qourum"
    requiredSigners = models.CharField(1)
    totalSigners = models.CharField(1)
