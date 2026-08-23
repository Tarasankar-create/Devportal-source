from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, EnvironmentViewSet, DeploymentViewSet

router= DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'environments', EnvironmentViewSet)
router.register(r'deployments', DeploymentViewSet)

urlpatterns=router.urls