from django_filters import rest_framework

from .models import Client


class ClientFilter(rest_framework.FilterSet):

    class Meta:
        model = Client
        fields = ('code', 'tag')
