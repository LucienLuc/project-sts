from rest_framework import routers

# import views that will be mapped to url paths
from .views import ShopViewSet

router = routers.SimpleRouter()
router.register(r'', ShopViewSet)
urlpatterns = router.urls