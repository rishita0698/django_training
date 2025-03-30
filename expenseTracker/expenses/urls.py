from django.urls import path, include
from .views import OccasionManagementView, EventViewSet, PaymentViewSet,UtilizerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'occasions', OccasionManagementView, basename = 'occassion')
router.register(r'events', EventViewSet, basename = 'events')
router.register(r'payment', PaymentViewSet, basename = 'payment')
router.register(r'utilizer', UtilizerViewSet, basename = 'utilizer')


urlpatterns = [
    path('', include(router.urls)),
]