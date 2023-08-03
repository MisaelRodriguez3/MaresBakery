from django.urls import path

from ubicacion import views

app_name = 'ubicacion'

urlpatterns = [
    path('', views.ubicacion, name='Ubicacion'),
    path('conocenos/', views.conocenos, name='conocenos'),
]