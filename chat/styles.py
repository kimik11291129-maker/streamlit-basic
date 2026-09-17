import streamlit as st

_CSS = """
<style>
  .block-container { max-width: 900px; padding-top: 2.5rem; }

  [data-testid="stChatMessage"] {
    border-radius: 16px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    border: 1px solid rgba(128, 128, 128, 0.18);
  }
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: rgba(255, 75, 75, 0.07);
  }
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: rgba(128, 128, 128, 0.08);
  }

  .empty-card {
    border: 1px dashed rgba(128, 128, 128, 0.4);
    border-radius: 18px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    margin: 1.5rem 0 1rem;
  }
  .empty-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.35rem; }
  .empty-sub { opacity: 0.7; font-size: 0.9rem; }

  .login-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    background: rgba(128, 128, 128, 0.15);
    font-size: 0.78rem;
  }

  [data-testid="stSidebar"] .stButton button { justify-content: flex-start; text-align: left; }
  [data-testid="stSidebar"] h3 { font-size: 0.95rem; margin-bottom: 0.4rem; }
</style>
"""


def apply_styles():
    st.markdown(_CSS, unsafe_allow_html=True)
