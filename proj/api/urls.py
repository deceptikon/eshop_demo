from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tovars', views.ProductViewSet)
router.register('cart', views.CartViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('products', views.ProductView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
]
