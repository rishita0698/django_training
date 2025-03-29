from django.urls import path, include
from .views import OccasionManagementView, EventViewSet, PaymentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'occasions', OccasionManagementView, basename = 'occassion')
router.register(r'events', EventViewSet, basename = 'events')
router.register(r'payment', PaymentViewSet, basename = 'payment')


urlpatterns = [
    path('', include(router.urls)),
]