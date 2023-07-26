from .models import SoutToAc, SoutFromAc
from rest_framework.response import Response
from rest_framework import viewsets, permissions, views
from django.db.models import Q

# Create your views here.
class SoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = self.get_queryset()
        return Response([obj.serializer() for obj in queryset])

    def get_queryset(self):
        queryset = SoutFromAc.objects.all()
        query_params_dict = dict(self.request.query_params.lists())
        my_dict = dict()
        for key, value in query_params_dict.items():
            new_key = f'{key}__in'
            my_dict[new_key] = value
        queryset = queryset.filter(Q(**my_dict))
        return queryset

    def post(self, request):
        data = request.data
        result = []
        for validated_data in data:
            duble = SoutToAc.objects.filter(cardNum=validated_data['cardNum'])
            if duble.exists():
                instance = duble.first()
            else:
                instance = SoutToAc.objects.create()
            result.append(SoutToAc_cteate_or_update(instance, validated_data))
        return Response([res.serializer() for res in result])


def SoutToAc_cteate_or_update(instance, validated_data):
    for key, value in validated_data.items():
        setattr(instance, key, value)
    instance.save()
    return instance
