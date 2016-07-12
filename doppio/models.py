from django.db import models

class Pull(models.Model):
    date_of_grind = models.DateTimeField(auto_now_add=True, null=True)
    grind_level = models.FloatField(null=True, blank=True, default = 0.0)
    bean_type = models.CharField(max_length=250, null=True)
    date_of_bean_roast = models.DateTimeField(auto_now_add=True, null=True)