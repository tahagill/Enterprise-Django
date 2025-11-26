from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from home import views 


urlpatterns = [
    
    path("", views.home, name="home"),
    path("about/", views.about, name='about'),
    path("services/", views.services, name='services'),
    path("contact/", views.contact, name='contact'),
    path('login/', views.loginUser, name='login'),
    path("logout/", views.logoutuser, name='logout'),
    path('signup/', views.signupUser, name='signup'),
    path("status/", views.status, name='status'),
    path("orders/", views.orders, name='orders'),
    path('success/', views.success, name='success'),
    path('search/', views.search, name='search'),
    
    # User Profile URLs
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]