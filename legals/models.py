from django.db import models

from companies.models import Company


class CompanyLegal(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    terms_of_service = models.TextField()
    date_effective = models.DateField(blank=True, null=True)

    termination = models.TextField(blank=True, null=True)
    restrictions = models.TextField(blank=True, null=True)
    governing_law = models.TextField(blank=True, null=True)
    license_grants = models.TextField(blank=True, null=True)

    warranty = models.TextField(blank=True, null=True)
    liability = models.TextField(blank=True, null=True)
    disclaimer = models.TextField(blank=True, null=True)
    indemnification = models.TextField(blank=True, null=True)
    privacy_data_terms = models.TextField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company}'s Legal, {self.date_effective}"
