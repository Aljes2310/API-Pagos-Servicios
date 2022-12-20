from rest_framework.serializers import ModelSerializer
from .models import Pagos

class PagoSerializer(ModelSerializer):
    class Meta:
        model = Pagos
        fields = ["services", "monto"]