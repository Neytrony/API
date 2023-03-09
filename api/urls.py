from rest_framework import routers, permissions
from django.urls import path, include
from .views import BC_TO_YC_ViewSet, YC_TO_BC_ViewSet


router = routers.DefaultRouter()
router.register(r'v1/BC_TO_YC', BC_TO_YC_ViewSet, basename='BC_TO_YC')
router.register(r'v1/YC_TO_BC', YC_TO_BC_ViewSet, basename='YC_TO_BC')


urlpatterns = [
    path('', include(router.urls)),
]
