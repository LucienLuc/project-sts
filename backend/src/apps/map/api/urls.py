from rest_framework import routers

# import views that will be mapped to url paths
from .views import MapViewSet

router = routers.SimpleRouter()
router.register(r'', MapViewSet)
urlpatterns = router.urls