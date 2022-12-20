from django_filters import DateTimeFilter, FilterSet
from .models import Payment_user

class MyModelFilter(FilterSet):
    ExpirationDate = DateTimeFilter(field_name='ExpirationDate', lookup_expr='gte')
    ExpirationDate1 = DateTimeFilter(field_name='ExpirationDate', lookup_expr='lte')
    class Meta:
        model = Payment_user
        fields = ['ExpirationDate', "ExpirationDate1"]