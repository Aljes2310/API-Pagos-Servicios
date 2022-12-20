from django.shortcuts import render
from .models import Services, Payment_user, Expired_payments
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import PaymentSerializer, Expired_paymentsSerializer, ServicesSerializer
# Create your views here.
from rest_framework import filters, generics
from django_filters import DateTimeFilter, FilterSet
from rest_framework.permissions  import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from v1.pagination import SimplePagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .permissions import Permisos
from .pagination import SimplePagination
from .filters import MyModelFilter
from .throttles import Mil, Dosmil

class ServicesViewSet(ModelViewSet):
    serializer_class=ServicesSerializer
    queryset=Services.objects.all()
    permission_classes=[Permisos]
    http_method_names = ['get']
    pagination_class= SimplePagination

    throttle_classes=[Dosmil]

"""  permission_classes_by_action = {
        'create': [IsAdminUser],
        'list': [IsAdminUser],
        'retrieve': [IsAdminUser],
        'update': [IsAdminUser],

        'partial_update': [IsAdminUser],

        'destroy': [IsAdminUser]
        }   """


class PaymentViewSet(ModelViewSet):
    serializer_class=PaymentSerializer
    queryset=Payment_user.objects.all()
    permission_classes=[Permisos]
    pagination_class= SimplePagination
    filter_fields = ('ExpirationDate', 'ExpirationDate1')
    filterset_class = MyModelFilter
    throttle_classes=[Mil]



class Expired_paymentsViewSet(ReadOnlyModelViewSet):
    serializer_class=Expired_paymentsSerializer
    queryset=Expired_payments.objects.all()
    permission_classes=[Permisos]
    http_method_names = ['get', 'post', 'head']
    pagination_class=SimplePagination
    throttle_classes=[Dosmil]