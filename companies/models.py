from django.db import models


class Company(models.Model):
    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=100)
    about = models.TextField()

    date_founded = models.DateField()

    location = models.CharField(max_length=100)

    twitter = models.URLField()
    website = models.URLField()
    logo_url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
