from django.urls import include, path
from rest_framework import routers

from .views import ClientViewSet, DistribViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('clients', ClientViewSet, basename='clients')
router_v1.register('distributions', DistribViewSet, basename='distributions')

urlpatterns = [
    path('', include(router_v1.urls)),
]
