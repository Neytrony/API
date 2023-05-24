from rest_framework import routers, permissions
from django.urls import path, include
from .views import BC_TO_YC_ViewSet, YC_TO_BC_ViewSet, BpToYcAPIView, YcToBpAPIView
from rest_framework import routers, permissions
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

router = routers.DefaultRouter()
# router.register(r'v1/BpToYc', BC_TO_YC_ViewSet, basename='BpToYc')
# router.register(r'v1/YcToBp', YC_TO_BC_ViewSet, basename='YcToBp')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('v1/BpToYcAPIView/', BpToYcAPIView.as_view(), name='BpToYcAPIView'),
    # path('v1/YcToBpAPIView/', YcToBpAPIView.as_view(), name='YcToBpAPIView')
    path('v1/BpToYc/', BpToYcAPIView.as_view(), name='BpToYcAPIView'),
    path('v1/YcToBp/', YcToBpAPIView.as_view(), name='YcToBpAPIView')
]
