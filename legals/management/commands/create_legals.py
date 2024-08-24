from django.core.management.base import BaseCommand, CommandError

from companies.models import Company
from legals.models import CompanyLegal

from legals.chains.termination import chain as termination_chain
from legals.chains.restrictions import chain as restrictions_chain
from legals.chains.governing_law import chain as governing_law_chain
from legals.chains.license_grants import chain as license_grants_chain


class Command(BaseCommand):
    help = "Create legals for a company."

    def add_arguments(self, parser):
        parser.add_argument("company", type=int)

    def handle(self, *args, **options):
        company_id = options["company"]

        company = Company.objects.get(pk=company_id)
        legal = CompanyLegal.objects.get(company=company)

        terms_of_service = legal.terms_of_service
        # legal.governing_law = governing_law_chain.invoke({
        #     "text": terms_of_service
        # })
        # legal.license_grants = license_grants_chain.invoke({
        #     "text": terms_of_service
        # })
        # legal.restrictions = restrictions_chain.invoke({
        #     "text": terms_of_service
        # })
        legal.termination = termination_chain.invoke({
            "text": terms_of_service
        })

        legal.save()

        self.stdout.write(
            self.style.SUCCESS('Successfully create legals for %s at %s' % (
                company, legal.date_effective,))
        )
