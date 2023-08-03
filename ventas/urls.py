from django.urls import path
from ventas import views

urlpatterns = [
    path("carrito/", views.carrito, name="carrito"),
    path("compra_cliente/", views.correo_compra_clientes, name="compra_cliente"),
    path("encargo_cliente/", views.correo_encargo_clientes, name="encargo_cliente"),
    path("borrar_item/<int:producto_id>/", views.eliminar_producto, name="eliminar"),
    path("agregar_item/<int:producto_id>/", views.agregar_producto, name="agregar"),
    path("aumentar/<int:producto_id>/", views.aumentar, name="aumentar"),
    path("restar/<int:producto_id>/", views.restar_producto, name="restar"),
    path("compra/", views.comprar, name="comprar"),
    path("verificar-encargo/", views.verificar_encargo, name="verificar"),
    path("encargo/", views.encargar, name="encargar"),
    path('proceso/', views.proceso, name='proceso'),
    path('guardar-datos-pago/', views.GuardarDatosPagoView.as_view(), name='guardar_datos_pago'),
    path('proceso_encargo/<str:fecha>/', views.proceso_encargo, name='proceso_encargo'),
    path('guardar_datos_encargo', views.GuardarDatosEncargoView.as_view(), name='guardar_datos_encargo'),
]
