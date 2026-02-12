from rest_framework.routers import DefaultRouter

# from rest_framework_nested.routers import NestedDefaultRouter

from ..api.ponto_viewsets import PontoViewSet

app_name = "ponto_api"

router = DefaultRouter()
router.register(r"pontos", PontoViewSet, basename="pontos")

urlpatterns = router.urls
