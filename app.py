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
# Styling — Modern redesign
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ── Import Fonts ──────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Brand tokens ──────────────────────────────────────────────────── */
    :root {
        --blue:         #22529A;
        --blue-light:   #2d6bc4;
        --blue-pale:    #e8f0fc;
        --blue-wash:    #f4f7fc;
        --yellow:       #FEDF27;
        --yellow-soft:  #fff7cc;
        --yellow-hover: #f5d520;

        --bg:           #f8f9fb;
        --surface:      #ffffff;
        --surface-alt:  #f1f3f7;
        --border:       #e2e6ee;
        --border-focus: var(--blue);

        --text-primary:   #1a1f2e;
        --text-secondary: #5a6378;
        --text-muted:     #8b93a7;

        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 20px;
        --radius-xl: 28px;

        --shadow-sm:  0 1px 3px rgba(26,31,46,0.06);
        --shadow-md:  0 4px 16px rgba(26,31,46,0.08);
        --shadow-lg:  0 12px 48px rgba(26,31,46,0.10);
        --shadow-btn: 0 2px 8px rgba(34,82,154,0.20);
    }

    /* ── Hide Streamlit chrome ─────────────────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    header    { visibility: hidden; }

    /* ── Page background ───────────────────────────────────────────────── */
    .stApp {
        background: var(--bg) !important;
        font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ── Central card ──────────────────────────────────────────────────── */
    .block-container {
        max-width: 680px !important;
        padding: 2.5rem 2.5rem 3rem !important;
        margin: 2rem auto !important;
        background: var(--surface) !important;
        border-radius: var(--radius-xl) !important;
        border: 1px solid var(--border) !important;
        box-shadow: var(--shadow-lg) !important;
        text-align: left !important;
        position: relative;
        overflow: hidden;
    }

    /* Top accent stripe */
    .block-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--blue) 0%, var(--blue) 60%, var(--yellow) 60%, var(--yellow) 100%);
    }

    /* Subtle corner decoration */
    .block-container::after {
        content: '';
        position: absolute;
        top: 4px;
        right: 0;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle at top right, rgba(254,223,39,0.06) 0%, transparent 70%);
        pointer-events: none;
    }

    /* ── Typography ────────────────────────────────────────────────────── */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    p, label, span, div, li {
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Page title */
    h1 {
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
        border-bottom: none !important;
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
        display: block !important;
        color: var(--text-primary) !important;
    }

    /* Subtitle */
    .block-container > div > div > div > .stMarkdown:nth-child(3) p,
    .element-container:nth-child(3) p {
        color: var(--text-secondary) !important;
        font-size: 0.95rem !important;
        background: none !important;
        border-left: none !important;
        padding: 0 !important;
        margin-bottom: 1.5rem !important;
    }

    /* ── Section labels ────────────────────────────────────────────────── */
    label, .stSelectbox label, .stTextInput label {
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: var(--text-muted) !important;
        margin-bottom: 0.35rem !important;
    }

    /* ── Inputs ────────────────────────────────────────────────────────── */
    .stTextInput input,
    input[type="text"],
    input[type="search"] {
        background: var(--surface-alt) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        padding: 0.65rem 1rem !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    .stTextInput input:focus,
    input[type="text"]:focus {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(34,82,154,0.12) !important;
        outline: none !important;
        background: var(--surface) !important;
    }

    /* ── Select / combobox ─────────────────────────────────────────────── */
    div[data-baseweb="select"] > div,
    div[role="combobox"],
    div[aria-haspopup="listbox"] {
        background: var(--surface-alt) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[role="combobox"]:focus-within {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(34,82,154,0.12) !important;
    }

    /* Select text color */
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: var(--text-primary) !important;
    }

    /* Dropdown overlay */
    div[data-baseweb="popover"],
    div[role="listbox"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-lg) !important;
        overflow: hidden !important;
    }
    div[role="option"],
    li[role="option"] {
        background: transparent !important;
        color: var(--text-primary) !important;
        transition: all 0.15s ease !important;
        border-radius: 6px !important;
        margin: 2px 4px !important;
    }
    div[role="option"]:hover,
    li[role="option"]:hover {
        background: var(--blue-pale) !important;
        color: var(--blue) !important;
    }

    /* ── Buttons ───────────────────────────────────────────────────────── */
    .stButton button,
    .stDownloadButton button,
    button[data-baseweb="button"] {
        background: var(--blue) !important;
        color: var(--surface) !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.02em !important;
        padding: 0.55rem 1.4rem !important;
        transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
        box-shadow: var(--shadow-btn) !important;
        cursor: pointer !important;
    }
    .stButton button:hover,
    .stDownloadButton button:hover,
    button[data-baseweb="button"]:hover {
        background: var(--blue-light) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(34,82,154,0.30) !important;
    }
    .stButton button:active,
    .stDownloadButton button:active {
        transform: translateY(0) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* Download button specific — yellow accent */
    .stDownloadButton button {
        background: var(--blue) !important;
        position: relative;
        overflow: hidden;
    }
    .stDownloadButton button::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--yellow);
    }

    /* ── File result rows ──────────────────────────────────────────────── */
    div.stMarkdown p {
        background: var(--surface-alt) !important;
        border-left: 3px solid var(--yellow) !important;
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0 !important;
        padding: 0.6rem 1rem !important;
        margin-bottom: 0.4rem !important;
        text-align: left !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: var(--text-primary) !important;
        transition: background 0.15s ease !important;
    }
    div.stMarkdown p:hover {
        background: var(--blue-pale) !important;
    }

    /* ── Alerts / messages ─────────────────────────────────────────────── */
    div[data-testid="stAlert"] {
        border-radius: var(--radius-md) !important;
        border: none !important;
    }

    /* Success */
    div.stSuccess, [data-testid="stAlert"][data-type="success"] {
        background: #f0faf0 !important;
        border-left: 4px solid #2d9a3e !important;
        border-radius: var(--radius-md) !important;
    }
    div.stSuccess p, [data-testid="stAlert"][data-type="success"] p {
        color: #1a5c26 !important;
        background: transparent !important;
        border-left: none !important;
        padding: 0 !important;
    }

    /* Warning */
    div.stWarning, [data-testid="stAlert"][data-type="warning"] {
        background: var(--yellow-soft) !important;
        border-left: 4px solid var(--yellow-hover) !important;
        border-radius: var(--radius-md) !important;
    }
    div.stWarning p, [data-testid="stAlert"][data-type="warning"] p {
        color: #6b5c00 !important;
        background: transparent !important;
        border-left: none !important;
        padding: 0 !important;
    }

    /* Error */
    div.stError, [data-testid="stAlert"][data-type="error"] {
        background: #fef0f0 !important;
        border-left: 4px solid #c53030 !important;
        border-radius: var(--radius-md) !important;
    }
    div.stError p, [data-testid="stAlert"][data-type="error"] p {
        color: #7c1d1d !important;
        background: transparent !important;
        border-left: none !important;
        padding: 0 !important;
    }

    /* Info */
    div.stInfo, [data-testid="stAlert"][data-type="info"] {
        background: var(--blue-pale) !important;
        border-left: 4px solid var(--blue) !important;
        border-radius: var(--radius-md) !important;
    }
    div.stInfo p, [data-testid="stAlert"][data-type="info"] p {
        color: var(--blue) !important;
        background: transparent !important;
        border-left: none !important;
        padding: 0 !important;
    }

    /* ── Spinner ───────────────────────────────────────────────────────── */
    .stSpinner > div {
        border-top-color: var(--blue) !important;
    }

    /* ── Placeholder ───────────────────────────────────────────────────── */
    ::placeholder {
        color: var(--text-muted) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Image (logo) ──────────────────────────────────────────────────── */
    .stImage {
        margin-bottom: 0.5rem !important;
    }
    .stImage img {
        border-radius: var(--radius-md) !important;
    }

    /* ── Custom badge / tag styling ────────────────────────────────────── */
    .doc-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--blue-pale);
        color: var(--blue);
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 100px;
        margin-bottom: 0.75rem;
    }
    .doc-badge::before {
        content: '';
        width: 6px;
        height: 6px;
        background: var(--yellow);
        border-radius: 50%;
    }

    /* ── Divider ───────────────────────────────────────────────────────── */
    hr {
        border: none !important;
        height: 1px !important;
        background: var(--border) !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Misc ──────────────────────────────────────────────────────────── */
    .stBlock, .stExpander { background: transparent !important; }

    /* ── Scrollbar ─────────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-muted);
    }

    /* ── Animation for results ─────────────────────────────────────────── */
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .stDownloadButton,
    div.stMarkdown {
        animation: fadeSlideUp 0.3s ease-out forwards;
    }
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
# Badge + Title
# ---------------------------------------------------------------------------
st.markdown('<div class="doc-badge">Document Portal</div>', unsafe_allow_html=True)
st.title("ISCAR Documents")
st.write("Search and download delivery notes, purchase orders, picking slips, and shipments.")

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Document folders
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
                                    with open(file_path, "rb") as fh:
                                        st.download_button(
                                            label="Download",
                                            data=fh,
                                            file_name=f,
                                            mime="application/octet-stream",
                                            key=f"dl_{f}",
                                        )
                                else:
                                    st.warning(f"{f} is not a valid file.")
                        else:
                            st.warning("No files found matching that number.")
                    except OSError as e:
                        st.error(f"Error accessing files: {e}")
