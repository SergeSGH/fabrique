from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import ClientViewSet, DistribViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('clients', ClientViewSet, basename='clients')
router_v1.register('distributions', DistribViewSet, basename='distributions')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/', views.obtain_auth_token),
    path('', include(router_v1.urls)),
]

