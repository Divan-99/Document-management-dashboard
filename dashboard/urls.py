"""
dashboard/urls.py
"""

from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # ── Pages ─────────────────────────────────────────────────────────────
    path("", views.index, name="index"),

    # ── Status API ─────────────────────────────────────────────────────────
    path("api/status/",                  views.api_status_all, name="status_all"),
    path("api/status/<str:process_id>/", views.api_status_one, name="status_one"),

    # ── Control API ────────────────────────────────────────────────────────
    path("api/start/<str:process_id>/",   views.api_start,   name="start"),
    path("api/stop/<str:process_id>/",    views.api_stop,    name="stop"),
    path("api/restart/<str:process_id>/", views.api_restart, name="restart"),

    # ── Logs API ───────────────────────────────────────────────────────────
    path("api/logs/<str:process_id>/",    views.api_logs,    name="logs"),
]
