"""
URL configuration for process_dashboard project.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect root to dashboard
    path("", RedirectView.as_view(url="/dashboard/", permanent=False)),

    # Django admin
    path("admin/", admin.site.urls),

    # Built-in auth views (login / logout)
    path("accounts/login/",  auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Dashboard app
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
]
