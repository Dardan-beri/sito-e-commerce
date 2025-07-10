from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from DjangoProject.views import index
from store.views import home_view
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path('', home_view, name='home'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register', user_views.register_view, name='register-direct'),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
]