from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status, views
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files import File
from django.db.models import Q

from .models import BpToYc, YcToBp
from .serializers import BpToYcSerializer, YcToBpSerializer, FileSerializer


class CreateListModelMixin(object):
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)


class BC_TO_YC_ViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    # queryset = BpToYc.objects.all()
    serializer_class = BpToYcSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['SNILS', 'dateStartLearn']
    def get_queryset(self):
        queryset = BpToYc.objects.all()
        query_params_dict = dict(self.request.query_params.lists())
        SNILS = query_params_dict.get('SNILS')
        dateStartLearn = query_params_dict.get('dateStartLearn')
        my_filter = Q()
        # for key, value in query_params_dict.items():
        #     my_filter &= Q(**{key: value})
        #     print(my_filter)
        # print(queryset.filter(my_filter))
        if query_params_dict is not None:
            queryset = queryset.filter(**query_params_dict)
        if SNILS is not None and dateStartLearn is not None:
            queryset = queryset.filter(Q(SNILS__in=SNILS) & Q(dateStartLearn__in=dateStartLearn))
        elif SNILS is None and dateStartLearn is not None:
            queryset = queryset.filter(dateStartLearn__in=dateStartLearn)
        elif SNILS is not None and dateStartLearn is None:
            queryset = queryset.filter(SNILS__in=SNILS)
        return queryset


class YC_TO_BC_ViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    queryset = YcToBp.objects.all()
    serializer_class = YcToBpSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['tabNum', 'eduStatus', 'platformStatus']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = YcToBp.objects.all()
        query_params_dict = dict(self.request.query_params.lists())
        tabNum = query_params_dict.get('tabNum')
        eduStatus = query_params_dict.get('eduStatus')
        platformStatus = query_params_dict.get('platformStatus')
        # if query_params_dict is not None:
        #     queryset = queryset.filter(**query_params_dict)
        if tabNum is not None and eduStatus is not None and platformStatus is not None:
            queryset = queryset.filter(Q(tabNum__in=tabNum) & Q(eduStatus__in=eduStatus) & Q(platformStatus__in=platformStatus))
        elif tabNum is None and eduStatus is not None and platformStatus is not None:
            queryset = queryset.filter(Q(eduStatus__in=eduStatus) & Q(platformStatus__in=platformStatus))
        elif tabNum is not None and eduStatus is None and platformStatus is not None:
            queryset = queryset.filter(Q(tabNum__in=tabNum) & Q(platformStatus__in=platformStatus))
        elif tabNum is not None and eduStatus is not None and platformStatus is None:
            queryset = queryset.filter(Q(tabNum__in=tabNum) & Q(eduStatus__in=eduStatus))
        elif tabNum is not None and eduStatus is None and platformStatus is None:
            queryset = queryset.filter(Q(tabNum__in=tabNum))
        elif tabNum is None and eduStatus is not None and platformStatus is None:
            queryset = queryset.filter(Q(eduStatus__in=eduStatus))
        elif tabNum is None and eduStatus is None and platformStatus is not None:
            queryset = queryset.filter(Q(platformStatus__in=platformStatus))
        return queryset


class getFile(views.APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        query_params_dict = dict(self.request.query_params.lists())
        tabNum = query_params_dict.get('tabNum')[0]
        protocol = query_params_dict.get('protocol')
        file = YcToBp.objects.get(tabNum=tabNum).protocol
        filePath = file.path
        fileName = file.name
        file = open(f'{filePath}', 'rb')
        response = HttpResponse(File(file), content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{fileName}"'
        return response

class FileUploadView(viewsets.ViewSet):
    parser_classes = (MultiPartParser,)

    def create(self, request):
        serializer_class = FileSerializer(data=request.data)
        if 'file' not in request.FILES or not serializer_class.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            files = request.FILES.getlist('file')
            for file in files:
                FileSystemStorage().save(file.name, file)
            return Response(status=status.HTTP_201_CREATED)