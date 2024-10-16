from django.db import models


class Milestone(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    required_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField(max_length=200)

    def __str__(self):
        return self.name
