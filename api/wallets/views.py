from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from .models import Key, Wallet, Transaction
import datetime


class LoginView(generic.FormView):
    template_name = "login.html"
    context_object_name = "Login form"


class AccessAccounts(generic.ListView):
    template_name = "AccessAccounts.html"
    context_object_name = "AccessAccounts list"


class UserHomepage(generic.DetailView):
    template_name = "UserHomepage.html"
    context_object_name = "Userhomepage"


# class CreateUserView(generic.FormView):
#     template_name = "CreateUser.html"
#     context_object_name = "CreateUser form"


class IndexView(generic.ListView):
    template_name = "transaction/index.html"
    context_object_name = "latest_transaction_list"

    def get_queryset(self):
        """Return the last five transactions."""
        return Wallet.objects.order_by("updated_at")[:5]


class DepositView(generic.CreateView):
    template_name = "Deposit/deposit.html"
    context_object_name = "Deposit"

    def get_queryset(self):
        return Transaction.objects.values("Deposit")


class WithdrawView(generic.CreateView):
    template_name = "Withdraw/withdraw.html"
    context_object_name = "Withdraw"

    def get_queryset(self):
        return Transaction.objects.values("Withdraw")


class TransactionView(generic.ListView):
    template_name = "Transaction/transaction.html"
    context_object_name = "latest_transaction_list"

    def get_queryset(self):
        """Return the last five transactions."""
        return Transaction.objects.order_by("-pub_date")[:10]


class DetailView(generic.DetailView):
    model = Wallet
    template_name = "wallets/detail.html"


class ResultsView(generic.DetailView):
    model = Wallet
    template_name = "wallet/results.html"


def transaction(request, key_id):
    wallet = get_object_or_404(Wallet, pk=key_id)
    try:
        selected_choice = Key.choice_set.get(pk=request.POST["key"])
    except (Wallet.Error, Wallet.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "wallets/detail.html",
            {
                "Payment": Wallet,
                "error_message": "You didn't select an amount.",
            },
        )
    else:
        selected_choice.vote += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse("transaction:results", args=(transaction.id,))
        )


def page_details(request, slug):
    page = get_object_or_404(user=request.user).filter(slug=slug)
    today = datetime.date.today()
    is_visible = page.available_on is None or page.available_on <= today
    return TemplateResponse(
        request, "page/details.html", {"page": page, "is_visible": is_visible}
    )
