from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category', views.cats, name='products_category_all'),
    path('category/<slug:slug>', views.cats, name='products_category'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('register', views.register, name='register'),
    path('protected', views.protected, name="test"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)