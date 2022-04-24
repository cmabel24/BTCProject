import datetime
# import json
from typing import Optional
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.template.response import TemplateResponse
from django.http import HttpResponse, Http404
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL

from wallets.forms import CreateWalletForm
from wallets.models import Key, Transaction, Wallet, PubKey


# def index(request):
#     return render(request, "wallets/index.html")

class IndexView(generic.ListView):
    model = Key
    template_name = "wallets/index.html"

    def get_queryset(self):
        return Key.objects.all()

texts = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam tortor mauris, maximus semper volutpat vitae, varius placerat dui. Nunc consequat dictum est, at vestibulum est hendrerit at. Mauris suscipit neque ultrices nisl interdum accumsan. Sed euismod, ligula eget tristique semper, lecleo mi nec orci. Curabitur hendrerit, est in ",
    "Praesent euismod auctor quam, id congue tellus malesuada vitae. Ut sed lacinia quam. Sed vitae mattis metus, vel gravida ante. Praesent tincidunt nulla non sapien tincidunt, vitae semper diam faucibus. Nulla venenatis tincidunt efficitur. Integer justo nunc, egestas eget dignissim dignissim,  facilisis, dictum nunc ut, tincidunt diam.",
    "Morbi imperdiet nunc ac quam hendrerit faucibus. Morbi viverra justo est, ut bibendum lacus vehicula at. Fusce eget risus arcu. Quisque dictum porttitor nisl, eget condimentum leo mollis sed. Proin justo nisl, lacinia id erat in, suscipit ultrices nisi. Suspendisse placerat nulla at volutpat ultricies",
]


def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num - 1])
    else:
        raise Http404("No such section")
def page_details(request, slug):
    page = get_object_or_404(Wallet, username=request.user).filter(slug=slug)
    today = datetime.date.today()
    is_visible = page.available_on is None or page.available_on <= today
    return TemplateResponse(
        request, "wallets/details.html", {"page": page, "is_visible": is_visible}
    )

class IndexView(generic.ListView):
    template_name = "wallets/index.html"
    context_object_name = "wallet_list"
    model = Wallet

    def get_queryset(self):
        """Return the last five transactions."""
        return self.model.objects.all().order_by("-created_at")[:5]

class DetailView(generic.DetailView):
    """"""
    model = Transaction
    template_name = "wallets/detail.html"

class CreateSeedPhrase(generic.FormView):
    """Creates the Seed Phrase"""
    # mnemo = Mnemonic("english")
    # words = mnemo.generate(strength=128)
    # seed = mnemo.to_seed(words, passphrase="")
    # Choose strength 128, 160, 192, 224 or 256
    STRENGTH: int = 160  # Default is 128
    # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
    LANGUAGE: str = "english"  # Default is english
    # Generate new entropy hex string
    ENTROPY: str = generate_entropy(strength=STRENGTH)
    # Secret passphrase for mnemonic
    PASSPHRASE: Optional[str] = None  # "meherett"
    # Initialize Bitcoin mainnet HDWallet
    hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)
    # Get Bitcoin HDWallet from entropy
    hdwallet.from_entropy(
        entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE
    )

    # Derivation from path
    hdwallet.from_path("m/44'/0'/0'/0/0")
    # Or derivation from index
    # hdwallet.from_index(44, hardened=True)
    # hdwallet.from_index(0, hardened=True)
    # hdwallet.from_index(0, hardened=True)
    # hdwallet.from_index(0)
    # hdwallet.from_index(0)
    mnemonic_phrase = hdwallet.dumps()["mnemonic"]

    def get(self,request):
        context ={}
        context['form']= CreateWalletForm()
        context["mnemonic_phrase"] = self.mnemonic_phrase
        return render(request, "wallets/create.html", context)
    def post(self,request):
        form = CreateWalletForm(request.POST)
        if form.is_valid():
            # Write xPriv to Key model
            priv_key = Key(xprivate_key=self.hdwallet.dumps()["xprivate_key"])
            priv_key.save()

            #Write xPub and key_id to PubKey model
            pub_key = PubKey(xpublic_key=self.hdwallet.dumps()["xpublic_key"], key=priv_key)
            pub_key.save()

            #Write name, requiredSigners, totalSigners, keys to Wallet model
            data: Wallet = form.save(commit=False)
            data.requiredSigners = 1
            data.totalSigners = 1
            data.save()
            data.keys.set([pub_key])
            redirect_url = reverse("Django Bitcoin:wallet_list")
            print(redirect_url)
            return redirect(redirect_url)
    # Print all Bitcoin HDWallet information's
    #print(json.dumps(hdwallet.dumps(), indent=4, ensure_ascii=False))



# class LoginView(generic.FormView):
#     template_name = "login.html"
#     context_object_name = "Login form"


# class AccessAccounts(generic.ListView):
#     template_name = "AccessAccounts.html"
#     context_object_name = "AccessAccounts list"


# class UserHomepage(generic.DetailView):
#     template_name = "UserHomepage.html"
#     context_object_name = "UserHomepage"


# class CreateUser(generic.FormView):
#     template_name = "CreateAccount.html"
#     context_object_name = "CreateUser form"




# class IndexView(generic.ListView):
#     template_name = "transaction/index.html"
#     context_object_name = "latest_transaction_list"

#     def get_queryset(self):
#         """Return the last five transactions."""
#         return Wallet.objects.order_by("updated_at")[:5]


# class DepositView(generic.CreateView):
#     template_name = "Deposit/deposit.html"
#     context_object_name = "Deposit"

#     def get_queryset(self):
#         return Transaction.objects.values("Deposit")


# class WithdrawView(generic.CreateView):
#     template_name = "Withdraw/withdraw.html"
#     context_object_name = "Withdraw"

#     def get_queryset(self):
#         return Transaction.objects.values("Withdraw")


# class TransactionView(generic.ListView):
#     template_name = "Transaction/transaction.html"
#     context_object_name = "latest_transaction_list"

#     def get_queryset(self):
#         """Return the last five transactions."""
#         return Transaction.objects.order_by("-pub_date")[:10]


# class DetailView(generic.DetailView):
#     model = Wallet
#     template_name = "wallets/detail.html"


# class ResultsView(generic.DetailView):
#     model = Wallet
#     template_name = "wallets/results.html"


# def transaction(request, key_id):
#     wallet = get_object_or_404(Wallet, pk=key_id)
#     try:
#         selected_choice = Key.choice_set.get(pk=request.POST["key"])
#     except (Wallet.Error, Wallet.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(
#             request,
#             "wallets/detail.html",
#             {
#                 "Payment": Wallet,
#                 "error_message": "You didn't select an amount.",
#             },
#         )
#     else:
#         selected_choice.vote += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(
#             reverse("transaction:results", args=(transaction.id,))
#         )


