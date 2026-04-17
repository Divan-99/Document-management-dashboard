"""
process_manager.py
==================
Manages subprocess lifecycle for all registered processes.

Process handles (subprocess.Popen objects) are stored in a module-level
dict so they persist for the lifetime of the Django server process.

IMPORTANT: Run Django with --noreload so this dict is never duplicated
in a second process.  e.g.:
    python manage.py runserver 0.0.0.0:8888 --noreload
"""

import os
import subprocess
import threading
import logging
from collections import deque
from datetime import datetime

from .process_registry import PROCESS_MAP

logger = logging.getLogger(__name__)

# ── Internal state ────────────────────────────────────────────────────────────

_lock = threading.Lock()

# { process_id: subprocess.Popen }
_handles: dict = {}

# { process_id: deque of (timestamp_str, line_str) } — last 200 lines per process
_logs: dict = {pid: deque(maxlen=200) for pid in PROCESS_MAP}

# { process_id: datetime } — when the process was last started
_started_at: dict = {}


# ── Log reader thread ─────────────────────────────────────────────────────────

def _stream_logs(process_id: str, proc: subprocess.Popen):
    """Background thread: reads stdout and appends lines to _logs."""
    try:
        for raw in proc.stdout:
            try:
                line = raw.decode("utf-8", errors="replace").rstrip()
            except Exception:
                line = repr(raw)
            ts = datetime.now().strftime("%H:%M:%S")
            _logs[process_id].append((ts, line))
    except Exception as exc:
        logger.debug("Log reader for %s ended: %s", process_id, exc)


# ── Environment builder ───────────────────────────────────────────────────────

def _build_env(defn: dict) -> dict:
    """
    Build a clean environment for the subprocess.

    Key problem this solves:
    The dashboard itself runs with DJANGO_SETTINGS_MODULE=process_dashboard.settings
    That env var is inherited by every child process we spawn — which means
    when a webapp's manage.py starts, it picks up OUR settings module instead
    of its own, causing: ModuleNotFoundError: No module named 'process_dashboard'

    Fix: always set DJANGO_SETTINGS_MODULE to the value defined in the process
    registry (if provided), or completely unset it for non-Django processes.
    """
    env = os.environ.copy()

    settings_module = defn.get("settings_module")

    if settings_module:
        # Webapp: point Django at its own settings module
        env["DJANGO_SETTINGS_MODULE"] = settings_module
    else:
        # OCR script or non-Django process: remove it entirely so the
        # child process starts with a clean slate
        env.pop("DJANGO_SETTINGS_MODULE", None)

    return env


# ── Public API ────────────────────────────────────────────────────────────────

def start_process(process_id: str) -> dict:
    """
    Start a process by id.
    Returns {"ok": True, "pid": int} or {"ok": False, "error": str}.
    """
    defn = PROCESS_MAP.get(process_id)
    if not defn:
        return {"ok": False, "error": f"Unknown process id: {process_id!r}"}

    with _lock:
        existing = _handles.get(process_id)
        if existing and existing.poll() is None:
            return {"ok": False, "error": "Process is already running"}

        try:
            # Windows: CREATE_NO_WINDOW suppresses the console popup
            flags = 0
            if hasattr(subprocess, "CREATE_NO_WINDOW"):
                flags = subprocess.CREATE_NO_WINDOW

            proc = subprocess.Popen(
                defn["cmd"],
                cwd=defn["cwd"],
                env=_build_env(defn),          # <-- clean env, no settings bleed
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                creationflags=flags,
            )

            _handles[process_id] = proc
            _started_at[process_id] = datetime.now()
            _logs[process_id].clear()

            # Start background log reader
            t = threading.Thread(
                target=_stream_logs,
                args=(process_id, proc),
                daemon=True,
                name=f"log-{process_id}",
            )
            t.start()

            logger.info("Started %s  pid=%s", process_id, proc.pid)
            return {"ok": True, "pid": proc.pid}

        except FileNotFoundError as exc:
            logger.error("Start failed for %s: %s", process_id, exc)
            return {"ok": False, "error": f"File not found — check paths in process_registry.py: {exc}"}
        except PermissionError as exc:
            return {"ok": False, "error": f"Permission denied: {exc}"}
        except Exception as exc:
            logger.exception("Unexpected error starting %s", process_id)
            return {"ok": False, "error": str(exc)}


def stop_process(process_id: str) -> dict:
    """
    Stop a running process by id.
    Returns {"ok": True} or {"ok": False, "error": str}.
    """
    with _lock:
        proc = _handles.get(process_id)

    if proc is None:
        return {"ok": False, "error": "Process was never started in this session"}

    if proc.poll() is not None:
        return {"ok": False, "error": "Process is already stopped"}

    try:
        proc.terminate()
        try:
            proc.wait(timeout=8)
            logger.info("Stopped %s gracefully", process_id)
            return {"ok": True}
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3)
            logger.warning("Killed %s (terminate timed out)", process_id)
            return {"ok": True, "warning": "Process did not stop gracefully — killed"}
    except Exception as exc:
        logger.exception("Error stopping %s", process_id)
        return {"ok": False, "error": str(exc)}


def restart_process(process_id: str) -> dict:
    """Stop then start a process. Returns the start result."""
    result = stop_process(process_id)
    if not result["ok"] and "already stopped" not in result.get("error", ""):
        return result
    return start_process(process_id)


def get_status(process_id: str) -> dict:
    """
    Return status dict for one process:
    {
        "status":     "running" | "stopped",
        "pid":        int | None,
        "returncode": int | None,
        "started_at": "HH:MM:SS" | None,
    }
    """
    with _lock:
        proc = _handles.get(process_id)

    if proc is None:
        return {"status": "stopped", "pid": None, "returncode": None, "started_at": None}

    returncode = proc.poll()
    if returncode is None:
        started = _started_at.get(process_id)
        return {
            "status": "running",
            "pid": proc.pid,
            "returncode": None,
            "started_at": started.strftime("%H:%M:%S") if started else None,
        }
    else:
        return {
            "status": "stopped",
            "pid": None,
            "returncode": returncode,
            "started_at": None,
        }


def get_all_statuses() -> dict:
    """Return {process_id: status_dict} for every registered process."""
    return {pid: get_status(pid) for pid in PROCESS_MAP}


def get_logs(process_id: str, last_n: int = 100) -> list:
    """
    Return up to last_n log lines for a process as
    [{"ts": "HH:MM:SS", "line": "..."}, ...]
    """
    buf = _logs.get(process_id, deque())
    entries = list(buf)[-last_n:]
    return [{"ts": ts, "line": line} for ts, line in entries]
