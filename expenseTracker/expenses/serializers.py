from rest_framework import serializers
from users.models import CustomUser
from .models import Occasion, Event,Utlizers, Payment


class OccasionSerializer(serializers.ModelSerializer):
    """serializer for the occassion object"""
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Occasion
        fields = ["id","name","description"]



class EventSerializer(serializers.ModelSerializer):
    """serializer for the Event object"""
    id = serializers.IntegerField(read_only = True)

    class Meta:
        model = Event
        fields = ["id","name","occasion","expender","total_amount"]


class UtlizersSerializer(serializers.ModelSerializer):
    """serializer for the Utilizers object"""
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Utlizers
        fields = ["id","utlizer","amount"]


class EventUtilizerSerializer(serializers.ModelSerializer):
    """serializer for the Event utilizer object"""
    id = serializers.IntegerField(read_only = True)
    utilizers_data= UtlizersSerializer(many = True)
    
    class Meta:
        model = Event
        fields = ["id","name","occasion","expender","total_amount","utilizers_data"]



class PaymentSerializer(serializers.ModelSerializer):
    """serializer for the Payment object"""
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Payment
        fields = ["id","event","payer","payee","amount"]