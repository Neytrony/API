import base64
import json

from rest_framework import viewsets, permissions, views
from django.db.models import Q
from rest_framework.response import Response

from .models import BpToYc, YcToBp
from .serializers import BpToYcSerializer, YcToBpSerializer


class CreateListModelMixin(object):
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(CreateListModelMixin, self).get_serializer(*args, **kwargs)


class Base64Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return base64.b64encode(o).decode()
        return json.JSONEncoder.default(self, o)


class BC_TO_YC_ViewSet(CreateListModelMixin, viewsets.ModelViewSet):
    serializer_class = BpToYcSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = BpToYc.objects.all()
        query_params_dict = dict(self.request.query_params.lists())
        SNILS = query_params_dict.get('SNILS')
        dateStartLearn = query_params_dict.get('dateStartLearn')
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

    def get_queryset(self):
        queryset = YcToBp.objects.all()
        query_params_dict = dict(self.request.query_params.lists())
        tabNum = query_params_dict.get('tabNum')
        eduStatus = query_params_dict.get('eduStatus')
        platformStatus = query_params_dict.get('platformStatus')
        if tabNum is not None and eduStatus is not None and platformStatus is not None:
            queryset = queryset.filter(
                Q(tabNum__in=tabNum) & Q(eduStatus__in=eduStatus) & Q(platformStatus__in=platformStatus))
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


class BpToYcAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = self.get_queryset()
        print(queryset)
        response = []
        for elem in queryset:
            attrs = [attr for attr in elem.__dict__.keys() if not attr.startswith('_') and not attr == 'id']
            obj_dict = dict()
            for attr in attrs:
                if attr != 'foto':
                    obj_dict[attr] = elem.__getattribute__(attr)
                else:
                    foto = elem.__getattribute__(attr)
                    obj_dict['fotoName'] = foto.name
                    obj_dict['fotoPath'] = foto.path
                    obj_dict[attr] = json.dumps(open(foto.path, 'rb').read(), cls=Base64Encoder)[1:-1]
            response.append(obj_dict)
        return Response(response)

    def get_queryset(self):
        queryset = BpToYc.objects.all()
        query_params_dict = dict(self.request.query_params.lists())
        my_dict = dict()
        for key, value in query_params_dict.items():
            new_key = f'{key}__in'
            my_dict[new_key] = value
        queryset = queryset.filter(Q(**my_dict))
        #
        # tabNum = query_params_dict.get('tabNum')
        # eduInst = query_params_dict.get('eduInst')
        # platformStatus = query_params_dict.get('platformStatus')
        # if tabNum is not None and eduInst is not None and platformStatus is not None:
        #     queryset = queryset.filter(
        #         Q(tabNum__in=tabNum) & Q(eduInst__in=eduInst) & Q(platformStatus__in=platformStatus))
        # elif tabNum is None and eduInst is not None and platformStatus is not None:
        #     queryset = queryset.filter(Q(eduInst__in=eduInst) & Q(platformStatus__in=platformStatus))
        # elif tabNum is not None and eduInst is None and platformStatus is not None:
        #     queryset = queryset.filter(Q(tabNum__in=tabNum) & Q(platformStatus__in=platformStatus))
        # elif tabNum is not None and eduInst is not None and platformStatus is None:
        #     queryset = queryset.filter(Q(tabNum__in=tabNum) & Q(eduInst__in=eduInst))
        # elif tabNum is not None and eduInst is None and platformStatus is None:
        #     queryset = queryset.filter(Q(tabNum__in=tabNum))
        # elif tabNum is None and eduInst is not None and platformStatus is None:
        #     queryset = queryset.filter(Q(eduInst__in=eduInst))
        # elif tabNum is None and eduInst is None and platformStatus is not None:
        #     queryset = queryset.filter(Q(platformStatus__in=platformStatus))
        return queryset

# class getFile(views.APIView):
#     parser_classes = (FileUploadParser,)
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         query_params_dict = dict(self.request.query_params.lists())
#         tabNum = query_params_dict.get('tabNum')[0]
#         protocol = query_params_dict.get('protocol')
#         file = YcToBp.objects.get(tabNum=tabNum).protocol
#         filePath = file.path
#         fileName = file.name
#         file = open(f'{filePath}', 'rb')
#         response = HttpResponse(File(file), content_type='application/force-download')
#         response['Content-Disposition'] = f'attachment; filename="{fileName}"'
#         return response
# class FileUploadView(viewsets.ViewSet):
#     parser_classes = (MultiPartParser,)
#
#     def create(self, request):
#         serializer_class = FileSerializer(data=request.data)
#         if 'file' not in request.FILES or not serializer_class.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         else:
#             files = request.FILES.getlist('file')
#             for file in files:
#                 FileSystemStorage().save(file.name, file)
#             return Response(status=status.HTTP_201_CREATED)
