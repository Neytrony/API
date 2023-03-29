from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets, permissions, status, views
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from .models import BpToYc, YcToBp
from .serializers import BpToYcSerializer, YcToBpSerializer


class CreateListModelMixin(object):
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)


class BC_TO_YC_ViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    queryset = BpToYc.objects.all()
    serializer_class = BpToYcSerializer
    permission_classes = [permissions.IsAuthenticated]

class YC_TO_BC_ViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    queryset = YcToBp.objects.all()
    serializer_class = YcToBpSerializer
    permission_classes = [permissions.IsAuthenticated]


class FileUploadView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request,  format=None):
        file_obj = request.FILES['file']
        FileSystemStorage().save(file_obj.name, file_obj)
        # do some stuff with uploaded file
        return Response(status=204)

    def put(self, request):
        file = request.data.get('file', None)

        if file is not None:
            FileSystemStorage().save(f'{file.name}', file)
            return Response(f'File: {file.name} successfully uploaded!', status=HTTP_200_OK)
        else:
            return Response(f'File not found!', status=HTTP_400_BAD_REQUEST)
