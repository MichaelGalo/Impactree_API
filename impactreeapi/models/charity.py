from django.db import models


class Charity(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "CharityCategory", on_delete=models.SET_NULL, null=True
    )
    description = models.TextField()
    impact_metric = models.CharField(max_length=255)
    impact_ratio = models.FloatField()
    website = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Charities"
