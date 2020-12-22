from rest_framework import routers

# import views that will be mapped to url paths
from .views import BattleViewSet

router = routers.SimpleRouter()
router.register(r'', BattleViewSet)
urlpatterns = router.urls