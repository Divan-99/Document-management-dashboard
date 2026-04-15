# ISCAR Document Management Dashboard

A Streamlit web application that lets ISCAR staff search and download documents (Delivery Notes, Purchase Orders, Picking Slips, Shipments) from network drives.

---

## Requirements

- Python 3.10+
- Network drives mapped/mounted and accessible from the machine running the app

---

## Local Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd document-management-dashboard

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and set the correct folder paths for your environment

# 5. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501` by default.

---

## Configuration

All folder paths are read from environment variables. Copy `.env.example` to `.env` and fill in the correct paths:

| Variable | Description | Default |
|---|---|---|
| `FOLDER_DELIVERY_NOTES` | Path to Delivery Notes folder | `Z:/` |
| `FOLDER_PURCHASE_ORDERS` | Path to Purchase Orders folder | `W:/` |
| `FOLDER_PICKING_SLIPS` | Path to Picking Slips folder | `Y:/` |
| `FOLDER_SHIPMENTS` | Path to Shipments folder | `X:/` |

On Linux/macOS, use mounted paths such as `/mnt/delivery-notes` instead of drive letters.

---

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── favicon.png         # Browser tab icon
├── header_logo.png     # Header logo displayed in the app
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── .github/
    └── workflows/
        └── lint.yml    # CI — lint on every push/PR
```

---

## Development

```bash
# Install dev linting tools
pip install ruff

# Lint
ruff check app.py
```

---

## Deployment Notes

- The app must run on a machine with access to the network drives.
- Do **not** expose the app to the public internet without adding authentication.
- Consider placing it behind a reverse proxy (nginx, Caddy) with HTTP Basic Auth or SSO if wider access is needed.
