from rest_framework import routers

# import views that will be mapped to url paths
from .views import RewardViewSet

router = routers.SimpleRouter()
router.register(r'', RewardViewSet)
urlpatterns = router.urls