# apps/marketplace/urls.py
from rest_framework.routers import DefaultRouter
from .views import SellerViewSet, ShowViewSet, ProductViewSet

router = DefaultRouter()
router.register('sellers', SellerViewSet, basename='seller')
router.register('shows', ShowViewSet, basename='show')
router.register('products', ProductViewSet, basename='product')

urlpatterns = router.urls