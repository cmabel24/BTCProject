#
# Django field type for a Bitcoin Address
#
import re
import hashlib
from unicodedata import name
from base58 import b58encode, b58decode
from django import forms
from django.core.exceptions import ValidationError
from wallets.models import Wallet

class CreateWalletForm(forms.ModelForm):
    """This is just a descriptor for what this class does."""
    class Meta:
        fields = ["name"]
        model = Wallet

    # xprivate_key = forms.CharField(max_length=111)


class BCAddressField(forms.CharField):
    default_error_messages = {
        "invalid": "Invalid Bitcoin address.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, value):
        if not value and not self.required:
            return None

        if not value.startswith(u"1") and not value.startswith(u"3"):
            raise ValidationError(self.error_messages["invalid"])
        value = value.strip()

        if "\n" in value:
            raise ValidationError(u"Multiple lines in the bitcoin address")

        if " " in value:
            raise ValidationError(u"Spaces in the bitcoin address")

        if re.match(r"[a-zA-Z1-9]{27,35}$", value) is None:
            raise ValidationError(self.error_messages["invalid"])
        version = get_bcaddress_version(value)
        if version is None:
            raise ValidationError(self.error_messages["invalid"])
        return value


def is_valid_btc_address(value):
    value = value.strip()
    if re.match(r"[a-zA-Z1-9]{27,35}$", value) is None:
        return False
    version = get_bcaddress_version(value)
    if version is None:
        return False
    return True


def b36encode(number, alphabet="0123456789abcdefghijklmnopqrstuvwxyz"):
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        long_value = 0
        for (i, c) in enumerate(number[::-1]):
            long_value += (256 ** i) * ord(c)
        number = long_value

    base36 = "" if number != 0 else "0"
    sign = ""
    if number < 0:
        sign = "-"
        number = -number

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def b36decode(number):
    return int(number, 36)


def get_bcaddress_version(strAddress):
    """Returns None if strAddress is invalid.    Otherwise returns integer version of address."""
    addr = b58decode(strAddress, 25)
    if addr is None:
        return None
    version = addr[0]
    checksum = addr[-4:]
    vh160 = addr[:-4]  # Version plus hash160 is what is checksummed
    h3 = hashlib.sha256(hashlib.sha256(vh160).digest()).digest()
    if h3[0:4] == checksum:
        return ord(version)
    return None
