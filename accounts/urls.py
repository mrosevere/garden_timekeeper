"""
URL configuration for the accounts app.

Defines routes for registration, login, logout, account deletion, and
other user-related actions. These routes provide a clean separation
between authentication logic and the rest of the application.
"""


from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("delete/", views.delete_account, name="delete_account"),
    path("settings/", views.account_settings, name="account_settings"),
]
