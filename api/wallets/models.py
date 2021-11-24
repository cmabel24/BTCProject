import uuid
import datetime
from django.contrib.auth import get_user_model
from django.db import models

# import django.dispatch
from django.utils.translation import ugettext as _

User = get_user_model()


# balance_changed = django.dispatch.Signal(
#     providing_args=["changed", "transaction", "bitcoinaddress"]
# )
# balance_changed_confirmed = django.dispatch.Signal(
#     providing_args=["changed", "transaction", "bitcoinaddress"]
# )


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
    requiredSigners = models.TextField(1)
    totalSigners = models.TextField(1)
