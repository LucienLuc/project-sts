from rest_framework import routers

# import views that will be mapped to url paths
from .views import GameViewSet

router = routers.SimpleRouter()
router.register(r'', GameViewSet)
urlpatterns = router.urls