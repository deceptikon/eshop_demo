from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html'), name='index'),
    path('category', views.CatsView.as_view(), name='products_category_all'),
    path('category/<slug:slug>', views.CatsView.as_view(), name='products_category'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.log_out, name='logout'),
    path('register', views.register, name='register'),
    path('protected', views.protected, name="test"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)