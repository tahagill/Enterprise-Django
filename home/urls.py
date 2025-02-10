from django.contrib import admin
from django.urls import path
from home import views 


urlpatterns = [
    
    path("", views.home, name="home"),
    path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'),
    path('login', views.loginUser, name='login'),
    path("logout", views.logoutuser, name='logout'),
    path('signup', views.signupUser, name='signup'),
    path("status", views.status, name='status'),
    path("orders", views.orders, name='orders'),
    path('success', views.success, name='success'),
]