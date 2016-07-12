

from django.db import models

class Pull(models.Model):
    date_of_grind = models.DateTimeField(auto_now_add=True, null=True)
    grind_level = models.FloatField(null=True, blank=True, default=0.0)
    grind_weight = models.FloatField(null=True, blank=True, default=0.0)
    bean_type = models.CharField(max_length=250, null=True)
    bean_roast_date = models.DateTimeField(auto_now_add=True, null=True)
    shot_time_length = models.TimeField(auto_now_add=False, null=True)
    shot_pressure_profile = models.TimeField(auto_now_add=False, null=True)

    def __unicode__(self):
        return self.name