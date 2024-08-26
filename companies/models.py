from django.db import models


class Company(models.Model):
    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100)
    about = models.TextField(null=True)

    date_founded = models.DateField(null=True)

    location = models.CharField(max_length=100, null=True)

    twitter = models.URLField(null=True)
    website = models.URLField(null=True)
    logo_url = models.URLField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"


class CompanyRequest(models.Model):
    reason = models.TextField()
    company_website = models.URLField()
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.company_name} by {self.name}"

    class Meta:
        verbose_name = "company request"
        verbose_name_plural = "company requests"
