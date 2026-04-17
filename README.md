# Process Dashboard

A Django web dashboard to monitor and control your Django web apps and OCR scripts
from a single browser tab — running entirely on your local Windows machine.

---

## Project structure

```
process_dashboard/
├── manage.py                        Django entry point
├── requirements.txt                 pip dependencies (just Django)
├── setup.bat                        First-time setup wizard
├── start.bat                        Start the dashboard server
│
├── process_dashboard/               Django project package
│   ├── settings.py                  All Django settings
│   ├── urls.py                      Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── dashboard/                       The dashboard app
│   ├── process_registry.py          ★ EDIT THIS — your process paths go here
│   ├── process_manager.py           Subprocess lifecycle management
│   ├── views.py                     Page + API views
│   ├── urls.py                      Dashboard URL patterns
│   ├── models.py                    (empty — no DB models needed)
│   ├── admin.py
│   ├── apps.py
│   │
│   ├── templates/dashboard/
│   │   ├── index.html               Main dashboard page
│   │   └── partials/
│   │       └── process_card.html    Individual process card
│   │
│   ├── static/dashboard/
│   │   ├── css/
│   │   │   ├── main.css             Global styles, navbar, login
│   │   │   └── dashboard.css        Cards, badges, log drawer
│   │   └── js/
│   │       ├── utils.js             Toast notifications
│   │       └── dashboard.js         Polling, controls, log viewer
│   │
│   └── management/commands/
│       ├── startall.py              python manage.py startall
│       └── stopall.py               python manage.py stopall
│
└── templates/
    ├── base.html                    Shared HTML layout
    └── registration/
        └── login.html               Login page
```

---

## Step 1 — Configure your processes

Open **`dashboard/process_registry.py`** and update every line marked `# <-- CHANGE THIS`.

Example for a Django web app running on port 8001:
```python
{
    "id":    "webapp_one",
    "label": "Invoicing App",
    "group": "webapp",
    "url":   "http://localhost:8001",
    "cwd":   r"C:\Projects\invoicing",
    "cmd":   [PYTHON, "manage.py", "runserver", "0.0.0.0:8001", "--noreload"],
},
```

Example for an OCR script:
```python
{
    "id":    "ocr_invoices",
    "label": "Invoice OCR",
    "group": "ocr",
    "cwd":   r"C:\Projects\ocr",
    "cmd":   [PYTHON, r"C:\Projects\ocr\invoice_ocr.py", "--config", r"C:\Projects\ocr\invoice.json"],
},
```

**Important:** Use raw strings (`r"C:\..."`) for Windows paths to avoid backslash issues.

If your OCR scripts don't use `--config`, change `cmd` to match whatever arguments they actually accept.

---

## Step 2 — First-time setup

Double-click **`setup.bat`** (or run it in a terminal):

```
setup.bat
```

This will:
1. Install Django via pip
2. Create the SQLite database (`db.sqlite3`)
3. Prompt you to create an admin username and password

---

## Step 3 — Start the dashboard

Double-click **`start.bat`** (or run in a terminal):

```
start.bat
```

Then open your browser at:

```
http://localhost:8000
```

You will be redirected to the login page. Sign in with the admin account you created.

---

## Features

| Feature | How it works |
|---|---|
| Status badges | Polls `/dashboard/api/status/` every 5 seconds |
| Start / Stop / Restart | POST to the control API; buttons update immediately |
| Live logs | Streams stdout from the process into a slide-up drawer |
| Open link | Appears on running web apps — opens the app in a new tab |
| Login required | All pages and API endpoints require authentication |

---

## API endpoints

These are all protected by login. Useful if you want to script or automate things.

| Method | URL | Description |
|---|---|---|
| GET | `/dashboard/api/status/` | All process statuses |
| GET | `/dashboard/api/status/<id>/` | Single process status |
| POST | `/dashboard/api/start/<id>/` | Start a process |
| POST | `/dashboard/api/stop/<id>/` | Stop a process |
| POST | `/dashboard/api/restart/<id>/` | Restart a process |
| GET | `/dashboard/api/logs/<id>/` | Recent stdout lines |

---

## Accessing from another machine on your network

1. In `process_dashboard/settings.py`, make sure your machine's IP is in `ALLOWED_HOSTS`:
   ```python
   ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.1.50"]  # your machine's IP
   ```
2. Start the dashboard as normal (`start.bat`)
3. From another machine: `http://192.168.1.50:8000`

---

## Troubleshooting

**"File not found" error when clicking Start**
→ The path in `process_registry.py` is wrong. Check `cwd` and `cmd` paths.

**Status stays "Stopped" right after clicking Start**
→ The process is crashing immediately. Open the Logs drawer — it will show the error output.

**"Process was never started in this session"**
→ You restarted the Django server. In-memory handles were lost. Just click Start again.

**Django web apps: port already in use**
→ Change the port number in `cmd` in `process_registry.py`.

**Must run with --noreload**
→ Django's file-watcher reloader forks a second Python process, which loses the in-memory
   process handles. Always use `start.bat` or add `--noreload` manually.
