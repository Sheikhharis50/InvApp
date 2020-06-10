from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('ping', views.check_status, name='ping'),
    path('setCookie', views.setCookieExpiry, name='setCookie'),
    path('register', views.register, name='register'),
    # path('dashboard', views.dashboard, name='dashboard')
]
