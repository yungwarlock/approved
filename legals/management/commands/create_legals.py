from django.core.management.base import BaseCommand, CommandError

from companies.models import Company
from legals.models import CompanyLegal

from legals.chains.termination import chain as termination_chain
from legals.chains.restrictions import chain as restrictions_chain
from legals.chains.governing_law import chain as governing_law_chain
from legals.chains.license_grants import chain as license_grants_chain
from legals.chains.extract_terms_and_conditions import chain as extract_terms_and_conditions_chain, fetch_url


class Command(BaseCommand):
    help = "Create legals for a company."

    def add_arguments(self, parser):
        parser.add_argument("company", type=int)

    def handle(self, *args, **options):
        company_id = options["company"]

        company = Company.objects.get(pk=company_id)

        if CompanyLegal.objects.filter(company=company).exists():
            raise CommandError(
                "CompanyLegal for %s already exists." %
                company
            )

        legal = CompanyLegal()
        legal.company = company

        terms_of_service_url = extract_terms_and_conditions_chain.invoke({
            "input": company.name
        })

        terms_of_service = fetch_url(terms_of_service_url)

        legal.governing_law = governing_law_chain.invoke({
            "text": terms_of_service
        })
        legal.license_grants = license_grants_chain.invoke({
            "text": terms_of_service
        })
        legal.restrictions = restrictions_chain.invoke({
            "text": terms_of_service
        })
        legal.termination = termination_chain.invoke({
            "text": terms_of_service
        })

        legal.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully create legals for %s at %s' % (
                company, legal.date_effective,))
        )
