from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ugettext as _
import datetime
import uuid
from django.db import transaction as db_transaction
from django.db.models import Avg, Max, Min, Sum
from .seo.models import SeoModel, SeoModelTranslation
User = get_user_model()


# balance_changed = django.dispatch.Signal(
#     providing_args=["changed", "transaction", "bitcoinaddress"]
# )
# balance_changed_confirmed = django.dispatch.Signal(
#     providing_args=["changed", "transaction", "bitcoinaddress"]
# )

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import pgettext_lazy

class PageQuerySet(models.QuerySet):
    def public(self):
        today = datetime.date.today()
        return self.filter(
            Q(is_visible=True),
            Q(available_on__lte=today) | Q(available_on__isnull=True),
        )

    def visible_to_user(self, user):
        has_access_to_all = user.is_active and user.has_perm("page.manage_pages")
        if has_access_to_all:
            return self.all()
        return self.public()


class Page(SeoModel):
    slug = models.SlugField(unique=True, max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=False)
    available_on = models.DateField(blank=True, null=True)

    objects = PageQuerySet.as_manager()

    class Meta:
        ordering = ("slug",)
        permissions = (
            ("manage_pages", pgettext_lazy("Permission description", "Manage pages.")),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("page:details", kwargs={"slug": self.slug})

    @property
    def is_published(self):
        today = datetime.date.today()
        return self.is_visible and (
            self.available_on is None or self.available_on <= today
        )


class PageTranslation(SeoModelTranslation):
    language_code = models.CharField(max_length=10)
    page = models.ForeignKey(
        Page, related_name="translations", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    class Meta:
        unique_together = (("language_code", "page"),)

    def __repr__(self):
        class_ = type(self)
        return "%s(pk=%r, title=%r, page_pk=%r)" % (
            class_.__name__,
            self.pk,
            self.title,
            self.page_id,
        )

    def __str__(self):
        return self.title


def update_wallet_balance(wallet_id):
    w = Wallet.objects.get(id=wallet_id)
    Wallet.objects.filter(id=wallet_id).update(last_balance=w.total_balance_sql())


class Key(models.Model):
    id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    xprivate_key = models.CharField(max_length=111)


class PubKey(models.Model):
    id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    key = models.ForeignKey(Key, on_delete=models.CASCADE, related_name="wallet_public_keys")
    xpublic_key = models.CharField(max_length=130)


class Wallet(models.Model):
    id = models.UUIDField(
        auto_created=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_last_balance(self, amount):
        if (
            self.__class__.objects.filter(
                id=self.id, last_balance=self.last_balance
            ).update(last_balance=(self.last_balance + amount))
            < 1
        ):
            update_wallet_balance.apply_async((self.id,), countdown=1)

    keys = models.ManyToManyField(PubKey, related_name="public_keys")
    name = models.TextField(unique=True)
    addressType = models.TextField(max_length=9)
    requiredSigners = models.TextField(1)
    totalSigners = models.TextField(1)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        max_digits=16, decimal_places=8, default=Decimal("0.0")
    )
    address = models.CharField(max_length=50)


class OutgoingTransaction(models.Model):
    created_at = models.DateTimeField(default=datetime.datetime.now)
    expires_at = models.DateTimeField(default=datetime.datetime.now)
    executed_at = models.DateTimeField(null=True, default=None)
    under_execution = models.BooleanField(default=False)  # execution fail
    to_bitcoinaddress = models.CharField(max_length=50, blank=True)
    amount = models.DecimalField(
        max_digits=16, decimal_places=8, default=Decimal("0.0")
    )

    txid = models.CharField(max_length=100, blank=True, null=True, default=None)

    def unicode(self):
        return (
            unicode(self.created_at)
            + ": "
            + self.to_bitcoinaddress
            + u", "
            + unicode(self.amount)
        )


class BitcoinAddress(models.Model):
    address = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    active = models.BooleanField(default=False)
    least_received = models.DecimalField(
        max_digits=16, decimal_places=8, default=Decimal(0)
    )
    least_received_confirmed = models.DecimalField(
        max_digits=16, decimal_places=8, default=Decimal(0)
    )
    label = models.CharField(max_length=50, blank=True, null=True, default=None)

    migrated_to_transactions = models.BooleanField(default=True)
