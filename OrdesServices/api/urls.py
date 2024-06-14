from rest_framework.routers import  DefaultRouter
from .views import  OrderViewSet

router = DefaultRouter()

router.register(r'ordes',OrderViewSet,basename='ordes')

urlpatterns = router.urls