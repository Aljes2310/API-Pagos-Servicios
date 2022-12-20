from django.shortcuts import render
from .models import Pagos
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import PagoSerializer
# Create your views here.
from rest_framework import filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ReadPagination, SimplePagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class PagosViewSet(ModelViewSet):
    serializer_class=PagoSerializer
    queryset=Pagos.objects.all()
    filter_backends= [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields=["services" ]
    search_fields=["user__id", "fecha_pago ", "services" ]
    pagination_class=SimplePagination

    throttle_classes = [UserRateThrottle]

    permission_classes=[permissions.IsAuthenticated]

class TaskReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class=PagoSerializer
    queryset=Pagos.objects.all()
    filter_backends= [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields=["services" ]
    search_fields=["user__id", "fecha_pago ", "services" ]
    pagination_class=ReadPagination

    throttle_classes = [UserRateThrottle]

