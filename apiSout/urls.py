from django.urls import path, include
from .views import SoutFromAcAPIView, SoutToAcAPIView, OneSoutFromAcAPIView
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('SoutFromAc/', SoutFromAcAPIView.as_view(),  name='SoutFromAc'),
    path('SoutFromAc/<str:cardNum>/', OneSoutFromAcAPIView.as_view(),  name='OneSoutFromAc'),
    path('SoutToAc/', SoutToAcAPIView.as_view(),  name='SoutToAc'),
    # path('SoutFromAc/', name='SoutFromAc'),
#     path('v1/BpToYc/', BpToYcAPIView.as_view(), name='BpToYcAPIView'),
#     path('v1/YcToBp/', YcToBpAPIView.as_view(), name='YcToBpAPIView')
]
