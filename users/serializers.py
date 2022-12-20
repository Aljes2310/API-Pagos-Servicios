from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=  ["email", "username", "password"]
         #hace que la contraseña no se muestre al crear el usuario
        extra_kwargs={
            "password": {'write_only':True}  
        }

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists:
            raise ValidationError("El email ya ha sido usado")
        return super().validate(attrs)

    def create(self, validated_data):
        password=validated_data.pop("password", None)#extrae la contraseña
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password) #hashea la contraseña
        instance.save()

        return instance


class GetUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]  


class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()

    def validate(self, attrs):
        self.token=attrs['refresh']

        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist
        
        except TokenError:
            self.fail("bad token")
