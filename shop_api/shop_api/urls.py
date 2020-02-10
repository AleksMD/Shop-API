"""shop_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop_api.views import healthcheck, index, signup_page, login_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthcheck/', healthcheck, name='healthcheck'),
    path('products/', include('product_app.urls')),
    path('baskets/', include('basket_app.urls')),
    path('shops/', include('shop_app.urls')),
    path('', index, name='index'),
    path('login/', login_page, name='login_page'),
    path('signup/', signup_page, name='signup_page')
]
