from django.contrib import admin
# Register your models here.
from .models import Occasion

class OccassionAdmin(admin.ModelAdmin):
    """define the admin pages for Occassions"""
    list_display = ["id","name", "description", "created_by","created_on"]
    search_fields = ('name','created_on',)

admin.site.register(Occasion, OccassionAdmin)