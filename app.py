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
    /* Hide Streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* App background and container */
    .stApp { background-color: #204f96; color: white; }
    .block-container {
        max-width: 900px;
        padding-top: 0rem;
        margin: auto;
        text-align: center;
        color: white !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* General text */
    h1, h2, h3, h4, h5, h6, p, label, span { color: white !important; }

    /* Labels */
    label { color: white !important; }

    /* Inputs */
    .stTextInput input,
    textarea,
    input[type="text"],
    input[type="search"] {
        color: white !important;
        background-color: #1a3b70 !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
    }

    /* Buttons */
    .stButton button,
    .stDownloadButton button,
    button[data-baseweb="button"] {
        color: white !important;
        background-color: #1a3b70 !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
    }

    /* Main visible select field and combobox trigger */
    div[data-baseweb="select"] > div,
    div[role="combobox"],
    div[aria-haspopup="listbox"] {
        background-color: #1a3b70 !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.22) !important;
        box-shadow: none !important;
    }

    /* Dropdown overlay and listbox when rendered in a portal */
    div[data-baseweb="popover"],
    div[role="listbox"] {
        background-color: #1a3b70 !important;
        color: white !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Individual options */
    div[role="option"],
    li[role="option"] {
        background-color: #1a3b70 !important;
        color: white !important;
    }

    /* Hover and selected states */
    div[role="option"]:hover,
    li[role="option"]:hover {
        background-color: #163567 !important;
        color: white !important;
    }

    /* Placeholder text */
    ::placeholder { color: rgba(255,255,255,0.7) !important; }

    /* Make common widget boxes transparent */
    .stBlock, .stExpander { background-color: transparent !important; }

    /* Alerts and messages */
    .stAlert, div.stWarning, div.stSuccess, div.stError {
        color: white !important;
        background-color: transparent !important;
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
