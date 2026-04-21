from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', view=views.LoginView.as_view(), name='login'),
    path('loginpage', view=views.login_page, name='loginpage'),
    path('logout', view=views.LogoutView.as_view(), name='logout'),
]
