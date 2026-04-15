# CLAUDE.md — Project Context for Claude Code

## What this project is

A single-page Streamlit app (`app.py`) that lets ISCAR staff search for and download documents stored on Windows network drives (mapped as drive letters Z:, W:, Y:, X:). The UI uses a dark-blue corporate theme.

## How to run locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit .env with real drive paths
streamlit run app.py
```

## Key decisions

- **Env vars for paths**: Network drive paths live in `.env` (see `.env.example`), never hardcoded.
- **Input validation**: `is_safe_search_term()` in `app.py` whitelists safe filename characters before the search runs.
- **No full file buffering**: Download buttons receive an open file handle so large files are streamed rather than loaded into RAM.
- **Unique widget keys**: Every `st.download_button` uses `key=f"dl_{filename}"` to avoid `DuplicateWidgetID` errors when multiple results are returned.
- **Image context manager**: `header_logo.png` is opened with `with Image.open(...) as img` to ensure the file handle is closed.

## Linting

```bash
pip install ruff
ruff check app.py
```

CI runs `ruff` on every push via `.github/workflows/lint.yml`.

## What to watch out for

- The app must run on a host with access to the network drives — it will not work on any machine that cannot reach those paths.
- No authentication is built in. Do not expose to the public internet without adding auth (reverse proxy + Basic Auth or SSO).
- The `.env` file must **never** be committed — it is gitignored.
