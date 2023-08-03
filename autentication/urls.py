from django.urls import path
from .views import profile

urlpatterns = [
    # path('', home, name='home'),
    path('accounts/profile/', profile, name = 'profile'),
]
