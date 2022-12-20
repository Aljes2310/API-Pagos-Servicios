from rest_framework.serializers import ModelSerializer
from .models import Services, Payment_user, Expired_payments
from datetime import datetime, timezone
from users.models import User
from rest_framework.response import Response
from rest_framework import generics, status


class ServicesSerializer(ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment_user
        fields = ["Amount", "ExpirationDate", 'service_id' , "user_id"]

    def create(self, validated_data):
        instance=self.Meta.model(**validated_data)
        instance.save()

        ExpirationDate = validated_data.pop("ExpirationDate")
        amount=validated_data.pop("Amount")
        user_id=validated_data.pop("user_id")

        paymentdate= datetime.now(timezone.utc) 
        user=User.objects.filter(email=user_id)
        id=user[0].id

        if ExpirationDate < paymentdate:
            b=Expired_payments(Pay_user_id=id, Penalty_fee_amount=amount)
            b.save()

        return instance


class Expired_paymentsSerializer(ModelSerializer):
    class Meta:
        model = Expired_payments
        fields = "__all__"  