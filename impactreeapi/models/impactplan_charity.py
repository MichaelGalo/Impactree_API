from django.db import models
from .impactplan import ImpactPlan
from .charity import Charity


class ImpactPlanCharity(models.Model):
    impact_plan = models.ForeignKey(ImpactPlan, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    allocation_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.impact_plan} - {self.charity}"

    class Meta:
        verbose_name_plural = "Impact Plan Charities"
