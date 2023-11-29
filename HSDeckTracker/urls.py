from django.urls import path
from . import views

urlpatterns=[
    path('', views.HSDT_home, name="HSDT_home"),
    path('create/', views.HSDT_create, name="HSDT_create"),
    path('read/', views.HSDT_read, name="HSDT_read"),
    path('<int:pk>/details/', views.HSDT_details, name="HSDT_details"),
    path('<int:pk>/edit/', views.HSDT_edit, name="HSDT_edit"),
    path('bs/', views.HSDT_bs, name="HSDT_bs"),
    path('api/', views.HSDT_api, name="HSDT_api"),
]