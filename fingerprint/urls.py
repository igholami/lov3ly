from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='fingerprint'),
    path('auth', views.authenticate, name='auth'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('complete_registration', views.complete_registration, name='complete_registration'),
    path('complete_login', views.complete_login, name='complete_login'),
    path('logout', views.logout, name='logout'),
]