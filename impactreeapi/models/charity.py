from django.db import models


class Charity(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "CharityCategory", on_delete=models.SET_NULL, null=True
    )
    description = models.TextField()
    impact_metric = models.CharField(max_length=255)
    impact_ratio = models.FloatField()
    website_url = models.URLField()
    image = models.ImageField(
        upload_to="charityimages",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Charities"
