from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Key, Wallet


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Wallet.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Wallet
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Wallet
    template_name = "polls/results.html"


def vote(request, wallet_id):
    wallet = get_object_or_404(Wallet, pk=wallet_id)
    try:
        selected_choice = wallet.choice_set.get(pk=request.POST["key"])
    except (KeyError, Key.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "Wallet": Wallet,
                "error_message": "You didn't select an amount.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(wallet.id,)))
