"""
URL configuration for the accounts app.

Defines routes for registration, login, logout, account deletion, and
other user-related actions. These routes provide a clean separation
between authentication logic and the rest of the application.
"""


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("delete/", views.delete_account, name="delete_account"),
    path("settings/", views.account_settings, name="account_settings"),
    
    # Password Reset (Django’s built‑in flow)
    path("password-reset/",
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"
         ),
         name="password_reset"),

    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_done.html"
         ),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_confirm.html"
         ),
         name="password_reset_confirm"),

    path("reset/done/",
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_complete.html"
         ),
         name="password_reset_complete"),

]
