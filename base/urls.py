from dynamic_rest.routers import DynamicRouter

from .apis import UserViewSet

urlpatterns = []

router = DynamicRouter()
router.register('users', UserViewSet)

urlpatterns += router.urls
app_name = "base"
