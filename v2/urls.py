from rest_framework.routers import DefaultRouter
from .views import ServicesViewSet,PaymentViewSet, Expired_paymentsViewSet


from . import views

router = DefaultRouter()
router.register(r'services', ServicesViewSet, basename="services")
router.register(r'payment', PaymentViewSet, basename="payment")
router.register(r'expired-payment', Expired_paymentsViewSet, basename="expired")


urlpatterns = []

urlpatterns += router.urls