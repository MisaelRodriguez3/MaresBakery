from django.urls import path

from inicio import views

urlpatterns = [
    path("", views.home, name="Inicio"),
    path("buscar/", views.buscar_productos, name="buscar_productos"),
]
