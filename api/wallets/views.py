from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Key, Wallet


class IndexView(generic.ListView):
    template_name = "transaction/index.html"
    context_object_name = "latest_transaction_list"

    def get_queryset(self):
        """Return the last five transactions."""
        return Wallet.objects.order_by("-pub_date")[:5]


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
