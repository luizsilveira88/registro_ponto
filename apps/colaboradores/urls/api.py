from rest_framework.routers import DefaultRouter

# from rest_framework_nested.routers import NestedDefaultRouter

from ..api.colaborador_viewsets import ColaboradorViewSet

app_name = "colaborador_api"

router = DefaultRouter()
router.register(r"colaboradores", ColaboradorViewSet, basename="colaborador")

# colaboradors_router = NestedDefaultRouter(router, r"colaboradores", lookup="colaborador")
# colaboradors_router.register(
#     r"configuracoes", ConfiguracaoViewSet, basename="colaborador-configuracao"
# )

urlpatterns = router.urls  # + colaboradors_router.urls
