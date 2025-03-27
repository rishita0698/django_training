from django.db import models
from users.models import CustomUser

# Create your models here.
class Occasion(models.Model):
    """model for occasion"""
    name = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True,null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="occasion")
    created_on = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name
    

