from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name
