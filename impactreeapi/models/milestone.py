from django.db import models


class Milestone(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    required_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    image_filename = models.CharField(max_length=255)

    def __str__(self):
        return self.name
