from rest_framework import viewsets, permissions
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import BC_TO_YC, YC_TO_BC
from .serializers import BC_TO_YC_Serializer, YC_TO_BC_Serializer


class BC_TO_YC_ViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = BC_TO_YC.objects.all()
    serializer_class = BC_TO_YC_Serializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]

class YC_TO_BC_ViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = YC_TO_BC.objects.all()
    serializer_class = YC_TO_BC_Serializer
    permission_classes = [permissions.AllowAny]
