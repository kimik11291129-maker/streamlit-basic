import streamlit as st

from chat.chat_page import render_chat_page
from chat.database import init_database
from chat.history_page import render_history_page
from chat.login_page import render_login_page
from chat.styles import apply_styles

st.set_page_config(page_title="AI 채팅", page_icon="💬", layout="wide")
apply_styles()
init_database()

# 키가 .env/secrets에 있어도 로그인 화면을 한 번 거치게 해서 보안 안내를 반드시 노출한다.
if not st.session_state.get("authenticated"):
    render_login_page()
    st.stop()

pages = {
    "AI 채팅": [
        st.Page(render_chat_page, title="채팅", icon="💬", default=True),
        st.Page(render_history_page, title="채팅 내역", icon="📜"),
    ],
}

st.navigation(pages).run()
