from dynamic_rest.routers import DynamicRouter

from .apis import UserViewSet, ProductViewSet

urlpatterns = []

router = DynamicRouter()
router.register('users', UserViewSet)
router.register('products', ProductViewSet)

urlpatterns += router.urls
app_name = "base"
