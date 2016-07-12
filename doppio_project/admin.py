from models import Pull
from django.contrib import admin

class PullAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pull, PullAdmin)