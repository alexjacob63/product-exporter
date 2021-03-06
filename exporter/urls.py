"""exporter URL Configuration

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
from django.urls import path
from django.views.generic import RedirectView

from products import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home')),
    path('admin/', admin.site.urls),
    path('upload/', views.simple_upload, name='upload'),
    path('stream/', views.stream, name='stream'),
    path('products/', views.ProductListView.as_view(), name='home'),
    path('products/add/', views.ProductCreateView.as_view(), name='product-add'),
    path('product/<pk>/', views.ProductDetailView.as_view(), name='product-view'),
    path('product/<pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('products/delete-all/', views.ProductDeleteAll.as_view(), name='delete-all')
]
