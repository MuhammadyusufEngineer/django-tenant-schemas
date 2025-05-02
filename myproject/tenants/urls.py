from django.urls import path
from . import views

urlpatterns = [
  path('api/tenants/<int:pk>/', views.tenant_detail, name="tenant_detail"),
  path('api/config/<str:tenant_id>/', views.get_config, name="get_config"),
  path('<str:tenant_id>/page', views.tenant_page, name="tenant_page"),
]