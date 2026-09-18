import streamlit as st

from chat.chat_page import render_chat_page
from chat.config import resolve_api_key
from chat.database import init_database
from chat.history_page import render_history_page
from chat.login_page import render_login_page
from chat.styles import apply_styles

st.set_page_config(page_title="AI 채팅", page_icon="💬", layout="wide")
apply_styles()
init_database()

# "로그인 완료" 여부는 별도 플래그가 아니라 "본인 키를 등록했는가"로만 판단한다.
# 상태를 하나로 합쳐야 authenticated=True인데 키가 없는 불일치 상태 자체가 생길 수 없다.
if not resolve_api_key():
    render_login_page()
    st.stop()

pages = {
    "AI 채팅": [
        st.Page(render_chat_page, title="채팅", icon="💬", default=True),
        st.Page(render_history_page, title="채팅 내역", icon="📜"),
    ],
}

st.navigation(pages).run()
