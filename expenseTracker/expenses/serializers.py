from rest_framework import serializers
from users.models import CustomUser
from .models import Occasion

class OccasionSerializer(serializers.ModelSerializer):
    """serializer for the occassion object"""
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Occasion
        fields = ["id","name","description"]
       