from django.shortcuts import render

from companies.models import Company
from legals.models import CompanyLegal


def index(request):
    companies = Company.objects.all()

    return render(request, "index.html", {"companies": companies})


def company_detail(request, slug):
    company = Company.objects.get(slug=slug)
    legals = CompanyLegal.objects.filter(company=company)
    sorted_legals = legals.order_by("-date_effective")
    legal = sorted_legals.first()

    return render(request, "detail.html", {
        "legal": legal,
        "company": company
    })
