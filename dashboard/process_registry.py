"""
process_registry.py
====================
Defines every process the dashboard can manage.
Pre-configured with real paths for this machine.
"""

import os

# Global Python fallback (Python 3.13 install)
PYTHON = r"C:\Program Files\Python313\python.exe"


def _venv_or_global(project_dir: str, args: list) -> list:
    """
    Use the project's venv python if it exists,
    otherwise fall back to the global Python 3.13 install.
    """
    venv_python = os.path.join(project_dir, "venv", "Scripts", "python.exe")
    interpreter = venv_python if os.path.exists(venv_python) else PYTHON
    return [interpreter] + args


# ─────────────────────────────────────────────────────────────────────────────
#  HOW TO FIND THE settings_module VALUE FOR A DJANGO WEBAPP
#
#  Open that webapp's manage.py and look for this line:
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "something.settings")
#  The value in quotes IS the settings_module — copy it exactly.
#
#  Example:
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "label_app.settings")
#    → settings_module = "label_app.settings"
#
#  This prevents the dashboard's own settings from leaking into the
#  child process and causing: ModuleNotFoundError: No module named 'process_dashboard'
# ─────────────────────────────────────────────────────────────────────────────

PROCESSES = [

    # ── Django Web App 1 — Label Web Page ─────────────────────────────────────
    # To find settings_module: open "Label Web Page Django\manage.py"
    # and copy the string from:  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "???")
    {
        "id":             "label_webapp",
        "label":          "Label Web Page",
        "group":          "webapp",
        "description":    "Django label web application  ·  port 8000",
        "url":            "https://label.sa.iscar.com",
        "cwd":            r"C:\Users\ISSA-OCRD\OneDrive - IMC\Desktop\Label Web Page Django",
        "settings_module": "labelgen.settings",   # <-- CHECK manage.py and update if different
        "cmd":            _venv_or_global(
                              r"C:\Users\ISSA-OCRD\OneDrive - IMC\Desktop\Label Web Page Django",
                              ["manage.py", "runserver", "0.0.0.0:8000", "--noreload"],
                          ),
    },

    # ── Django Web App 2 — Iscar Documents ────────────────────────────────────
    # To find settings_module: open "iscar_docs\manage.py"
    # and copy the string from:  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "???")
    {
        "id":             "iscar_docs",
        "label":          "Iscar Documents",
        "group":          "webapp",
        "description":    "Django Iscar documents application  ·  port 8080",
        "url":            "http://isdoc.sa.iscar.com",
        "cwd":            r"C:\Users\ISSA-OCRD\OneDrive - IMC\Desktop\iscar_docs",
        "settings_module": "iscar_docs.settings",  # <-- CHECK manage.py and update if different
        "cmd":            _venv_or_global(
                              r"C:\Users\ISSA-OCRD\OneDrive - IMC\Desktop\iscar_docs",
                              ["manage.py", "runserver", "0.0.0.0:8080", "--noreload"],
                          ),
    },

    # ── OCR Script 1 — Delivery Notes ─────────────────────────────────────────
    {
        "id":          "delivery_notes",
        "label":       "Delivery Notes",
        "group":       "ocr",
        "description": "deliverynotes.py",
        "cwd":         r"C:\Users\ISSA-OCRD\OneDrive - IMC\Desktop\Delivery notes",
        "cmd":         [PYTHON, "deliverynotes.py"],
    },

    # ── OCR Script 2 — Picking Slips ──────────────────────────────────────────
    {
        "id":          "picking_slips",
        "label":       "Picking Slips",
        "group":       "ocr",
        "description": "pickingslip.py",
        "cwd":         r"C:\Users\ISSA-OCRD\OneDrive - IMC\Desktop\Picking slips ocr",
        "cmd":         [PYTHON, "pickingslip.py"],
    },

    # ── OCR Script 3 — Purchase Orders ────────────────────────────────────────
    {
        "id":          "purchase_orders",
        "label":       "Purchase Orders",
        "group":       "ocr",
        "description": "purchaseorder.py",
        "cwd":         r"C:\Users\ISSA-OCRD\OneDrive - IMC\Desktop\Purchase order",
        "cmd":         [PYTHON, "purchaseorder.py"],
    },

    # ── OCR Script 4 — Shipments ──────────────────────────────────────────────
    {
        "id":          "shipments",
        "label":       "Shipments",
        "group":       "ocr",
        "description": "shipment.py",
        "cwd":         r"C:\Users\ISSA-OCRD\OneDrive - IMC\Desktop\Shipment",
        "cmd":         [PYTHON, "shipment.py"],
    },

]

# Internal lookup — do not edit
PROCESS_MAP = {p["id"]: p for p in PROCESSES}
