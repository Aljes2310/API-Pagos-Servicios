from rest_framework.routers import DefaultRouter
from .views import PagosViewSet,TaskReadOnlyViewSet


from . import views

router = DefaultRouter()
router.register(r'pagos', PagosViewSet, basename="pagos")
router.register(r'lectura', TaskReadOnlyViewSet, basename="todo_read_only_model_viewset")


urlpatterns = []

urlpatterns += router.urls