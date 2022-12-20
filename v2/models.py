from django.db import models
from users.models import User


# Create your models here.
class Services(models.Model):
    Name=models.CharField(max_length=100, unique=True)
    Description=models.CharField(max_length=100)
    Logo=models.CharField(max_length=100)

    # en lugar que salga services object sale el name del service en service_id
    def __str__(self):
        return self.Name

    class Meta:
        db_table="services"

class Payment_user(models.Model):
    user_id=models.ForeignKey(User, on_delete=models.CASCADE)
    service_id=models.ForeignKey(Services, to_field='Name', on_delete=models.CASCADE)
    Amount=models.IntegerField()
    PaymentDate=models.DateTimeField(auto_now_add=True)
    ExpirationDate=models.DateTimeField(default="")

    class Meta:
        db_table="Payment_user"


class Expired_payments(models.Model):
    Pay_user_id=models.IntegerField()
    Penalty_fee_amount=models.IntegerField()

    class Meta:
        db_table="Expired_payments"