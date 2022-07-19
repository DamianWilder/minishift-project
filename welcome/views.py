import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from fractions import Fraction

from . import database
from .models import PageView

# Create your views here.

def index(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse(PageView.objects.count())

def calculate_chex(request):
    context = {}

    sauce_ratio = {
        "BUTTER": 6,
        "GARLIC POWDER": 2.25,
        "GARLIC SALT": 0.25,
        "ONION SALT": 0.25,
        "LEMON JUICE": 4,
        "WORCHESTERSHIRE": 4,
    }

    DRY = 10

    try:
        supply = int(request.POST.get("batch", None))

        full_batches = supply // DRY
        partial_batches = (supply % DRY) / 10

        if partial_batches and full_batches >= 4:
            full_batches += 2
        elif full_batches >= 4:
            full_batches += 1
        elif full_batches < 1:
            full_batches = 1

        response = f"Showing amounts for {full_batches} batch(es): \n"
        for k, v in sauce_ratio.items():
            sauce_ratio[k] = v * full_batches
            if sauce_ratio[k] >= 2:

                tsp = Fraction(sauce_ratio[k] % 2)
                tbsp = int(sauce_ratio[k] // 2)

                response += f"{k +':':20} {tbsp:5} Tablespoons"
                if tsp > 1:
                    response += f" and {tsp.numerator // tsp.denominator} {Fraction(tsp.numerator%tsp.denominator, tsp.denominator)} Teaspoons"
                else:
                    if tsp:
                        response += f" and {tsp} Teaspoons"
                    else:
                        pass
            else:
                response += f"{k +':':20}"
                if tsp > 1:
                    response += f"{'':1}{tsp.numerator // tsp.denominator} {Fraction(tsp.numerator%tsp.denominator, tsp.denominator)} Teaspoons"
                else:
                    response += f" {'':2}{Fraction(sauce_ratio[k])} Teaspoons"
            response += " \n"
        context["calculation"] = response.split("\n")
        return render(request, "welcome/chex_calculation.html", context)
    except:
        pass
        hostname = os.getenv('HOSTNAME', 'unknown')
        PageView.objects.create(hostname=hostname)
        return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })