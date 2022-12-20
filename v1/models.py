from django.db import models

# Create your models here.

class Pagos(models.Model):

    class servicios(models.TextChoices):
        netflix= "NETFLIX"
        amazon= "AMAZON VIDEO"
        star= "STAR +"
        paramount= "PARAMOUNT +"

    user_id=models.IntegerField(primary_key=True)
    fecha_pago=models.DateTimeField(auto_now_add=True)
    services=models.CharField(max_length=20, choices=servicios.choices)
    monto=models.IntegerField()
