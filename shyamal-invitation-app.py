"""Shyamal & Tropa web invitation, served full-screen as a Streamlit app.

The invitation itself lives in shyamal-invitation/index.html (a self-contained
page); this app just shows it edge to edge with Streamlit's own chrome hidden.
Deploy on Streamlit Community Cloud with this file as the main file path.
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

SITE_DIR = Path(__file__).parent / "shyamal-invitation"

st.set_page_config(
    page_title="Shyamal & Tropa · Shubho Bibaho",
    page_icon=str(SITE_DIR / "favicon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit's header, toolbar, padding and footer, and stretch the
# invitation's frame to the full window (dvh keeps phones' browser bars in mind).
st.markdown(
    """
    <style>
      header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
      [data-testid="stStatusWidget"], #MainMenu, footer { display: none !important; }
      html, body, .stApp, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        background: #3e0814 !important;
      }
      .block-container, [data-testid="stAppViewBlockContainer"] {
        padding: 0 !important;
        max-width: 100% !important;
      }
      [data-testid="stVerticalBlock"] { gap: 0 !important; }
      .element-container:has(style) { display: none !important; }
      iframe[title="st.iframe"], [data-testid="stIFrame"] iframe, .element-container iframe {
        display: block;
        position: fixed;
        inset: 0;
        width: 100vw !important;
        height: 100vh !important;
        height: 100dvh !important;
        border: 0;
        z-index: 999;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html((SITE_DIR / "index.html").read_text(encoding="utf-8"), height=800, scrolling=True)
