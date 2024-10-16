from django.db import models
from django.contrib.auth.models import User
from .milestone import Milestone


class ImpactPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    philanthropy_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    total_annual_allocation = models.DecimalField(max_digits=12, decimal_places=2)
    current_milestone = models.ForeignKey(
        Milestone, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"Impact Plan for {self.user.username}"
