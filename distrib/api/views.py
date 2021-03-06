from datetime import datetime as dt
from urllib import parse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ClientFilter
from .models import Client, Distrib, User
from .serializers import (ClientSerializer, DistribCreateSerializer,
                          DistribDetailSerializer, DistribListSerializer,
                          UserSerializer,
                          make_distrib, time_format)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class ClientViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ClientFilter


class DistribViewSet(viewsets.ModelViewSet):
    queryset = Distrib.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            pk = self.kwargs.get('pk')
            if pk:
                return DistribDetailSerializer
            return DistribListSerializer
        return DistribCreateSerializer

    @action(
        detail=False,
        methods=('post',),
        url_path='process',
        permission_classes=(IsAuthenticated,),
    )
    def process(self, request):
        distribs = Distrib.objects.all()
        for distrib in distribs:
            start_dt = dt.strptime(distrib.start_time, time_format)
            end_dt = dt.strptime(distrib.finish_time, time_format)
            filter_string = distrib.client_filter
            filters = dict(
                parse.parse_qsl(parse.urlsplit(filter_string).query)
            )
            if '??????' in filters and '??????' in filters:
                clients = Client.objects.all()
                clients = clients.filter(
                    tag=filters['??????']
                ).filter(code=filters['??????'])
                start_dt = dt.strptime(distrib.start_time, time_format)
                end_dt = dt.strptime(distrib.finish_time, time_format)
                if start_dt < dt.now() < end_dt:
                    make_distrib(clients, distrib, start_dt, end_dt, 0)
        return Response(status=status.HTTP_200_OK)
