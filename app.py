import os
import re

import streamlit as st
from PIL import Image

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
FAVICON_PATH = "favicon.png"
HEADER_LOGO_PATH = "header_logo.png"

st.set_page_config(
    page_title="ISCAR Documents",
    page_icon=FAVICON_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ── Brand tokens ──────────────────────────────────────────────────── */
    :root {
        --blue:        #22529A;
        --blue-dark:   #1a3e78;
        --blue-deeper: #132d58;
        --yellow:      #FEDF27;
        --yellow-hover:#e5c818;
        --white:       #ffffff;
        --text-muted:  rgba(255,255,255,0.7);
    }

    /* ── Hide Streamlit chrome ─────────────────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }

    /* ── Page background ───────────────────────────────────────────────── */
    .stApp {
        background: linear-gradient(150deg, var(--blue) 0%, var(--blue-dark) 55%, var(--blue-deeper) 100%);
        min-height: 100vh;
    }

    /* ── Central card ──────────────────────────────────────────────────── */
    .block-container {
        max-width: 760px;
        padding: 0 2rem 3rem;
        margin: 1.5rem auto;
        background: rgba(255,255,255,0.06);
        border-radius: 16px;
        border-top: 4px solid var(--yellow);
        box-shadow: 0 8px 40px rgba(0,0,0,0.3);
        backdrop-filter: blur(6px);
        text-align: center;
        color: var(--white) !important;
    }

    /* ── Typography ────────────────────────────────────────────────────── */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: var(--white) !important;
    }

    /* Page title — yellow underline accent */
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        padding-bottom: 0.4rem !important;
        border-bottom: 3px solid var(--yellow) !important;
        display: inline-block !important;
        margin-bottom: 0.25rem !important;
    }

    /* Subtitle / body copy */
    p { color: var(--text-muted) !important; }

    /* ── Section labels ────────────────────────────────────────────────── */
    label, .stSelectbox label, .stTextInput label {
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
        color: var(--text-muted) !important;
    }

    /* ── Inputs ────────────────────────────────────────────────────────── */
    .stTextInput input,
    input[type="text"],
    input[type="search"] {
        background: rgba(255,255,255,0.08) !important;
        color: var(--white) !important;
        border: 1.5px solid rgba(255,255,255,0.18) !important;
        border-radius: 8px !important;
        padding: 0.55rem 0.9rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stTextInput input:focus,
    input[type="text"]:focus {
        border-color: var(--yellow) !important;
        box-shadow: 0 0 0 3px rgba(254,223,39,0.2) !important;
        outline: none !important;
    }

    /* ── Select / combobox ─────────────────────────────────────────────── */
    div[data-baseweb="select"] > div,
    div[role="combobox"],
    div[aria-haspopup="listbox"] {
        background: rgba(255,255,255,0.08) !important;
        color: var(--white) !important;
        border: 1.5px solid rgba(255,255,255,0.18) !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease !important;
        box-shadow: none !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[role="combobox"]:focus-within {
        border-color: var(--yellow) !important;
        box-shadow: 0 0 0 3px rgba(254,223,39,0.2) !important;
    }

    /* Dropdown overlay */
    div[data-baseweb="popover"],
    div[role="listbox"] {
        background: var(--blue-dark) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35) !important;
    }
    div[role="option"],
    li[role="option"] {
        background: transparent !important;
        color: var(--white) !important;
        transition: background 0.15s ease !important;
    }
    div[role="option"]:hover,
    li[role="option"]:hover {
        background: rgba(254,223,39,0.12) !important;
        color: var(--yellow) !important;
    }

    /* ── Buttons ───────────────────────────────────────────────────────── */
    .stButton button,
    .stDownloadButton button,
    button[data-baseweb="button"] {
        background: var(--yellow) !important;
        color: var(--blue) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        padding: 0.5rem 1.6rem !important;
        transition: background 0.2s ease, transform 0.1s ease, box-shadow 0.2s ease !important;
        box-shadow: 0 2px 10px rgba(254,223,39,0.25) !important;
    }
    .stButton button:hover,
    .stDownloadButton button:hover,
    button[data-baseweb="button"]:hover {
        background: var(--yellow-hover) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 18px rgba(254,223,39,0.35) !important;
    }
    .stButton button:active,
    .stDownloadButton button:active {
        transform: translateY(0) !important;
    }

    /* ── File result rows ──────────────────────────────────────────────── */
    div.stMarkdown p {
        background: rgba(255,255,255,0.05) !important;
        border-left: 3px solid var(--yellow) !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 0.45rem 0.9rem !important;
        margin-bottom: 0.3rem !important;
        text-align: left !important;
        font-size: 0.92rem !important;
        color: var(--white) !important;
    }

    /* ── Alerts / messages ─────────────────────────────────────────────── */
    div[data-testid="stAlert"] {
        border-radius: 8px !important;
        border: none !important;
    }
    .stAlert, div.stWarning, div.stSuccess, div.stError, div.stInfo {
        color: var(--white) !important;
        background: rgba(255,255,255,0.08) !important;
        border-left: 4px solid var(--yellow) !important;
        border-radius: 8px !important;
    }

    /* ── Placeholder ───────────────────────────────────────────────────── */
    ::placeholder { color: var(--text-muted) !important; }

    /* ── Misc ──────────────────────────────────────────────────────────── */
    .stBlock, .stExpander { background: transparent !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header logo
# ---------------------------------------------------------------------------
if os.path.exists(HEADER_LOGO_PATH):
    with Image.open(HEADER_LOGO_PATH) as header_logo:
        st.image(header_logo, width=800)

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title("ISCAR Documents")
st.write("Welcome to the ISCAR document portal.")

# ---------------------------------------------------------------------------
# Document folders — loaded from environment variables so paths are never
# hardcoded in source control. Set these in a .env file (see .env.example).
# ---------------------------------------------------------------------------
DOC_FOLDERS: dict[str, str] = {
    "Delivery Notes": os.environ.get("FOLDER_DELIVERY_NOTES", "Z:/"),
    "Purchase Orders": os.environ.get("FOLDER_PURCHASE_ORDERS", "W:/"),
    "Picking Slips": os.environ.get("FOLDER_PICKING_SLIPS", "Y:/"),
    "Shipments": os.environ.get("FOLDER_SHIPMENTS", "X:/"),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
_SAFE_INPUT_RE = re.compile(r"^[\w\-. ]+$")


def is_safe_search_term(value: str) -> bool:
    """Return True only if the search term contains safe characters."""
    return bool(value.strip()) and bool(_SAFE_INPUT_RE.match(value))


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
doc_type = st.selectbox("Select Document Type", list(DOC_FOLDERS.keys()))

if doc_type:
    folder_path = DOC_FOLDERS[doc_type]

    if not os.path.exists(folder_path):
        st.error(f"The folder for {doc_type} is not accessible: {folder_path}")
    else:
        search_number = st.text_input(f"Enter the {doc_type} number to search:")

        if search_number:
            if not is_safe_search_term(search_number):
                st.error("Invalid search term. Use only letters, digits, hyphens, dots, and spaces.")
            else:
                with st.spinner("Searching files..."):
                    try:
                        files = sorted(
                            f for f in os.listdir(folder_path) if search_number in f
                        )

                        if files:
                            st.success(f"Found {len(files)} file(s):")
                            for f in files:
                                file_path = os.path.join(folder_path, f)
                                if os.path.isfile(file_path):
                                    st.write(f)
                                    # Open the file lazily so it is streamed to
                                    # the browser rather than loaded fully into
                                    # memory before the download starts.
                                    with open(file_path, "rb") as fh:
                                        st.download_button(
                                            label="Download",
                                            data=fh,
                                            file_name=f,
                                            mime="application/octet-stream",
                                            # Unique key prevents DuplicateWidgetID
                                            # errors when multiple results are shown.
                                            key=f"dl_{f}",
                                        )
                                else:
                                    st.warning(f"{f} is not a valid file.")
                        else:
                            st.warning("No files found matching that number.")
                    except OSError as e:
                        st.error(f"Error accessing files: {e}")
