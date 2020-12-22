from rest_framework import routers

# import views that will be mapped to url paths
from .views import EnemyViewSet

router = routers.SimpleRouter()
router.register(r'', EnemyViewSet)
urlpatterns = router.urls