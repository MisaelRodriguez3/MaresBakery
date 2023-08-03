from django.urls import path
from productos import views


urlpatterns = [
    path('productos/', views.mostrar_productos, name='Todos'),
    path('pan-fino/1/', views.ver_pan_fino, name='Pan_fino'),
    path('bolillo-y-pieza/2/', views.ver_bolillo_y_pieza, name='Bolillo_y_pieza'),
    path('lo-mismo/5/', views.pan_de_siempre, name='Lo_mismo'),
    path('detalle-pan/<int:producto_id>/', views.detalle_pan, name="info_pan"),
    path('Opinion/<int:producto_id>/', views.opinion, name='opinion'),
]