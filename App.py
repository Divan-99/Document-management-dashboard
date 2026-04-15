import streamlit as st
import os
from PIL import Image

# Config
favicon_path = "favicon.png"
header_logo_path = "header_logo.png"

st.set_page_config(
    page_title="ISCAR Documents",
    page_icon=favicon_path,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS that targets both the select control and any overlay rendered in a portal
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
    unsafe_allow_html=True
)

# Header logo
if os.path.exists(header_logo_path):
    header_logo = Image.open(header_logo_path)
    st.image(header_logo, width=800)

# Title
st.title("ISCAR Documents")

# Body text
st.write("Welcome to the ISCAR document portal.")

# Document folders
DOC_FOLDERS = {
    "Delivery Notes": "Z:/",
    "Purchase Orders": "W:/",
    "Picking Slips": "Y:/",
    "Shipments": "X:/"
}

# Select document type
doc_type = st.selectbox("Select Document Type", list(DOC_FOLDERS.keys()))

if doc_type:
    folder_path = DOC_FOLDERS[doc_type]

    if not os.path.exists(folder_path):
        st.error(f"The folder for {doc_type} is not accessible.")
    else:
        search_number = st.text_input(f"Enter the {doc_type} number to search:")

        if search_number:
            with st.spinner('Searching files...'):
                try:
                    files = [f for f in os.listdir(folder_path) if search_number in f]
                    files.sort()

                    if files:
                        st.success(f"Found {len(files)} file(s):")
                        for f in files:
                            file_path = os.path.join(folder_path, f)
                            if os.path.isfile(file_path):
                                with open(file_path, "rb") as file:
                                    file_bytes = file.read()
                                st.write(f)
                                st.download_button(
                                    label="Download",
                                    data=file_bytes,
                                    file_name=f,
                                    mime="application/octet-stream"
                                )
                            else:
                                st.warning(f"{f} is not a valid file")
                    else:
                        st.warning("No files found matching that number.")
                except Exception as e:
                    st.error(f"Error accessing files: {e}")
