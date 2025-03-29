from django.contrib import admin
# Register your models here.
from .models import Occasion,Event,Utlizers, Payment

class OccassionAdmin(admin.ModelAdmin):
    """define the admin pages for Occassions"""
    list_display = ["id","name", "description", "created_by","created_on"]
    search_fields = ('name','created_on',)


class EventAdmin(admin.ModelAdmin):
    """define the admin pages for Event"""
    list_display = ["id","name", "occasion", "expender","total_amount", "created_by"]

class UtlizersAdmin(admin.ModelAdmin):
    """define the admin pages for Utilizers"""
    list_display = ["id","event", "utlizer", "amount"]

class PaymentAdmin(admin.ModelAdmin):
    """define the admin pages for Utilizers"""
    list_display = ["id","payer", "payee", "event","amount"]

admin.site.register(Occasion, OccassionAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Utlizers, UtlizersAdmin)
admin.site.register(Payment, PaymentAdmin)
