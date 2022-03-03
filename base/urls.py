from dynamic_rest.routers import DynamicRouter

urlpatterns = []

router = DynamicRouter()
# router.register('request', ViewSet)

urlpatterns += router.urls
app_name = "base"
