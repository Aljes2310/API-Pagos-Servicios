# **Proyecto U5 Silabuz**

## _Api Pagos de Servicios_
## **Alumno**: Alfredo Alvarado Espinoza
## **Aula**: 5

___

Esta api tiene 2 versiones:
- **V1 :** Tarea del 16 de diciembre
- **V2 :** Funcionalidades señaladas en el proyecto

___

## **_Funcionalidades_**

### **1) Para la parte del login deben hacer uso de simpleJWT, y debe contar con las mismas funcionalidades que el login desarrollado en sesiones anteriores.**

En `users/urls.py` :
```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
```

### **2) La API deberá contar con el CRUD para todos los modelos presentados.**

Primero se crean los modelos correspondientes

``` python
from django.db import models
from users.models import User


# Create your models here.
class Services(models.Model):
    Name=models.CharField(max_length=100, unique=True)
    Description=models.CharField(max_length=100)
    Logo=models.CharField(max_length=100)

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
```

Luego de crear los modelos se procede a crear los serializers. Se crea un archivo `serializers.py`

```python
class ServicesSerializer(ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment_user
        fields = ["Amount", "ExpirationDate", 'service_id' , "user_id"]

class Expired_paymentsSerializer(ModelSerializer):
    class Meta:
        model = Expired_payments
        fields = "__all__"          
```

Posteriormente se crean las vistas. Se usuara `Modelviewset` porque incluye todas las operaciones CRUD

```python
class ServicesViewSet(ModelViewSet):
    serializer_class=ServicesSerializer
    queryset=Services.objects.all()

class PaymentViewSet(ModelViewSet):
    serializer_class=PaymentSerializer
    queryset=Payment_user.objects.all()

class Expired_paymentsViewSet(ReadOnlyModelViewSet):
    serializer_class=Expired_paymentsSerializer
    queryset=Expired_payments.objects.all()
```

Finalmente se tiene que configurar los routers en el archivo `urls.py`




### **3) Deben crear roles para el uso de la API.** 

Para esto se crea un archivo permissions.py en el cual se crea una clase que hereda de `Basepermission`
el metodo `has_permission` que nos permitara clasificar los request en base al metodo http y al tipo de usuario (superuser y user)

~~~ python
from rest_framework.permissions import BasePermission

class Permisos(BasePermission):
    def has_permission(self, request, view):

        if request.method in ["GET", "POST"] and request.user.is_authenticated:
            return True

        if request.method in ['PUT', 'DELETE'] and request.user.is_authenticated and request.user.is_superuser:
            return True
        return False

~~~

Este clase permisos se importa en `views.py` y se coloca dentro de las vistas creadas añadiendo el atributo `permission_classes` en cada vista

```python
from .permissions import Permisos
class ServicesViewSet(ModelViewSet):
    serializer_class=ServicesSerializer
    queryset=Services.objects.all()
    permission_classes=[Permisos]


```



### **4) La vista creada para el modelo de servicios debe ser estática, por lo que debe contar únicamente con el método GET.** 

Para esto se añade el atributo `http_method_names` en la vista services con el valor `['get']` lo cual solo permitira ese metodo http

```python
class ServicesViewSet(ModelViewSet):
    http_method_names = ['get']
```

### **5) La vista creada para el modelo Expired_payments, sólo debe admitir GET y POST.** 

Esto al igual que la 4) se puede hacer mediante el atributo `http_method_names = ['get', 'post']` añadiendolo a la vista `Expired_paymentsViewSet`


### **6) Añadir Paginación de 100 resultados por página.** 


Luego de hacer la configuracion respectiva en `settings.py` se crea un archivo `pagination` en el cual se crea una clase que permitira la paginacion de 100 resultados

```python
from rest_framework.pagination import PageNumberPagination

class SimplePagination(PageNumberPagination):
    page_size=100
    page_query_param="page_size"
    max_page_size=2000


```

Esto se imoorta en `views.py` y se coloca en cada vista por medio del atributo `pagination_class`


### **7) Si la fecha de pago supera a la fecha de expiración, se debe crear un registro automático en Expired_payments**

Esto se hace usando el metodo create en el serializers de "Expired_payments" ya que este recibe la data para serializarla

```python
class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment_user
        fields = ["Amount", "ExpirationDate", 'service_id' , "user_id"]

    def create(self, validated_data):
        instance=self.Meta.model(**validated_data)
        instance.save()

        #extrayendo los campos necesarios
        ExpirationDate = validated_data.pop("ExpirationDate")
        amount=validated_data.pop("Amount")
        user_id=validated_data.pop("user_id")
        paymentdate= datetime.now(timezone.utc)

        #buscando el id   
        user=User.objects.filter(email=user_id)
        id=user[0].id

        if ExpirationDate < paymentdate:
            b=Expired_payments(Pay_user_id=id, Penalty_fee_amount=amount)
            b.save()

        return instance

```


### **8) Implementar Throttling para la vista de pagos con 1000 request por día y las demás de 2000 por día. Para las pruebas realizar con 3 y 7 respectivamente**

Se crea el archivo throttles.py en el cual se crea los throttling correspondientes de 1000 y 2000.

```python
from rest_framework.throttling import UserRateThrottle


class Mil(UserRateThrottle):
    scope = 'mil'

class Dosmil(UserRateThrottle):
    scope="dosmil"

```

Estos son configurados en `settings.py`

```python
'DEFAULT_THROTTLE_RATES': {

        'mil': "1000/day",
        'dosmil' : "2000/day" }
```

Y se importan en las vistas respectivas usando el atributo `throttle_classes`


### **9) Generar la documentación de toda su API.**

La documentacion de la api se encuentra implementado en las ruta:

```python
    #swager
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui")
```