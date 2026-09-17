import streamlit as st
from components.chat.chat_basic import render_chat_basic
from components.chat.streaming import render_streaming


def render_chat_elements_page():
    # 채팅 요소 카테고리를 하위 탭으로 나누어 보여주는 페이지 함수
    st.title("💬 채팅 요소")
    st.caption("Streamlit 공식 Chat elements의 다양한 기능을 카테고리별 탭으로 확인합니다.")

    tab1, tab2 = st.tabs([
        "💬 채팅 인터페이스",
        "⌨️ 스트리밍 출력",
    ])

    with tab1:
        render_chat_basic()
    with tab2:
        render_streaming()
