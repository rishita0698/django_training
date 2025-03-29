from django.db import models
from users.models import CustomUser

# Create your models here.
class Occasion(models.Model):
    """Model for occasion"""
    name = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="occasion")
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Event(models.Model):
    """Model for Event"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    occasion = models.ForeignKey(Occasion, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="created_event")
    expender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="paid_event")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Utlizers(models.Model):
    """Model for Utlizers"""
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    utlizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "utilized_event")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} for {self.event.name}"
    

class Payment(models.Model):
    """Model for payment"""
    id = models.AutoField(primary_key=True)
    payer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "payment_made")
    payee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "payments_received")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payer.email} paid {self.payee.email} {self.amount}"
