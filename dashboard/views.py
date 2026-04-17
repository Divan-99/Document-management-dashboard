"""
dashboard/views.py
"""

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from .process_registry import PROCESSES, PROCESS_MAP
from . import process_manager as pm


# ── Auth helper ───────────────────────────────────────────────────────────────

def _is_authorised(request):
    if request.user.is_authenticated:
        return True
    return getattr(request, "_api_token_valid", False)


def _require_auth(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not _is_authorised(request):
            return JsonResponse({"error": "Unauthorised"}, status=401)
        return fn(request, *args, **kwargs)
    return wrapper


# ── Main dashboard page ───────────────────────────────────────────────────────

@login_required
@ensure_csrf_cookie
def index(request):
    webapps     = [p for p in PROCESSES if p["group"] == "webapp"]
    ocr_scripts = [p for p in PROCESSES if p["group"] == "ocr"]
    return render(request, "dashboard/index.html", {
        "webapps":     webapps,
        "ocr_scripts": ocr_scripts,
        "processes":   PROCESSES,
    })


# ── Status API — session OR Bearer token ──────────────────────────────────────

@csrf_exempt
@_require_auth
@require_GET
def api_status_all(request):
    return JsonResponse(pm.get_all_statuses())


@csrf_exempt
@_require_auth
@require_GET
def api_status_one(request, process_id):
    if process_id not in PROCESS_MAP:
        return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse(pm.get_status(process_id))


# ── Control API — session login only ─────────────────────────────────────────

@login_required
@require_POST
def api_start(request, process_id):
    if process_id not in PROCESS_MAP:
        return JsonResponse({"ok": False, "error": "Not found"}, status=404)
    result = pm.start_process(process_id)
    return JsonResponse(result, status=200 if result["ok"] else 400)


@login_required
@require_POST
def api_stop(request, process_id):
    if process_id not in PROCESS_MAP:
        return JsonResponse({"ok": False, "error": "Not found"}, status=404)
    result = pm.stop_process(process_id)
    return JsonResponse(result, status=200 if result["ok"] else 400)


@login_required
@require_POST
def api_restart(request, process_id):
    if process_id not in PROCESS_MAP:
        return JsonResponse({"ok": False, "error": "Not found"}, status=404)
    result = pm.restart_process(process_id)
    return JsonResponse(result, status=200 if result["ok"] else 400)


# ── Logs API — session OR Bearer token ───────────────────────────────────────

@csrf_exempt
@_require_auth
@require_GET
def api_logs(request, process_id):
    if process_id not in PROCESS_MAP:
        return JsonResponse({"error": "Not found"}, status=404)
    last_n = int(request.GET.get("n", 100))
    return JsonResponse({"logs": pm.get_logs(process_id, last_n)})
