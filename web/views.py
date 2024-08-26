from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render

from sentry_sdk import capture_message

from legals.models import CompanyLegal
from companies.models import Company, CompanyRequest


def custom_page_not_found_view(*args, **kwargs):
    capture_message("Page not found!", level="error")

    # return any response here, e.g.:
    return HttpResponseNotFound("Not found")


def index(request):
    companies = Company.objects.all()

    return render(request, "index.html", {"companies": companies})


def request_company(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        company_website = request.POST.get("company_website")
        reason = request.POST.get("reason")
        name = request.POST.get("name")

        company_request = CompanyRequest(
            name=name,
            reason=reason,
            company_name=company_name,
            company_website=company_website,
        )

        messages.add_message(request, messages.INFO,
                             "Company request submitted successfully")

        return redirect("home")
    return render(request, "request_company.html")


def company_detail(request, slug):
    company = Company.objects.get(slug=slug)
    legals = CompanyLegal.objects.filter(company=company)
    sorted_legals = legals.order_by("-date_effective")
    legal = sorted_legals.first()

    return render(request, "detail.html", {
        "legal": legal,
        "company": company
    })
