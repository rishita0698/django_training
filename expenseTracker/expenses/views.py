from django.shortcuts import render

# Create your views here.
from .serializers import OccasionSerializer
from .models import Occasion
from rest_framework import viewsets, permissions, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from users.models import CustomUser
from django.shortcuts import get_object_or_404

# class OccasionManagementView(viewsets.ModelViewSet):
#     serializer_class = [OccasionSerializer,]
#     permission_classes = [permissions.IsAuthenticated,]
    

#     def get_queryset(self):
#         import json
#         print("user", self.request.user.id)
#         # user_detail = CustomUser.objects.filter(email = self.request.user).values()
#         return Occasion.objects.filter(created_by = self.request.user.id)
    

#     # def perform_create(self, serializer):
#     #     return serializer.save(created_by = self.request.user.id)


class OccasionManagementView(viewsets.ViewSet):
    """View for Managing Occassion related operation respect to the user"""
    permission_classes = [permissions.IsAuthenticated,]
    

    def list(self, request):
        print("user_id",  request.user.id)
        occasions = Occasion.objects.filter(created_by = request.user)
        serializer = OccasionSerializer(occasions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
            request_body=OccasionSerializer,
            responses={201:OccasionSerializer()}
    )
    def create(self, request):
        print("request_body", request.data)
        serializer = OccasionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED )
        return Response(serializer.errors, status = status. HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None):
        occasions = get_object_or_404(Occasion, pk=pk, created_by = request.user)
        serializer = OccasionSerializer(occasions)
        return Response (serializer.data)
    
    @swagger_auto_schema(
            request_body=OccasionSerializer,
            responses={200:OccasionSerializer()}
    )
    def update(self, request, pk=None):
        occasions = get_object_or_404(Occasion, pk=pk, created_by = request.user)
        serializer = OccasionSerializer(occasions, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None):
        occasions = get_object_or_404(Occasion, pk=pk, created_by = request.user)
        occasions.delete()
        return Response({"message":"occassion deleted successfully"}, status = status.HTTP_204_NO_CONTENT)

        