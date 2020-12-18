from rest_framework import routers

# import views that will be mapped to url paths
from .views import TestViewSet

router = routers.SimpleRouter()
router.register(r'', TestViewSet)
urlpatterns = router.urls