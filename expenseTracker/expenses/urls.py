from django.urls import path, include
from .views import OccasionManagementView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'occasions', OccasionManagementView, basename = 'occassion')


urlpatterns = [
    path('', include(router.urls))
]