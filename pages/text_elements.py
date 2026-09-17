import streamlit as st
from components.text_elements.headings_and_body import render_headings_and_body
from components.text_elements.markdown_and_write import render_markdown_and_write
from components.text_elements.code_and_math import render_code_and_math


def render_text_elements_page():
    # 텍스트 요소 카테고리를 하위 탭으로 나누어 보여주는 페이지 함수
    st.title("📝 텍스트 요소")
    st.caption("Streamlit 공식 Text elements의 다양한 기능을 카테고리별 탭으로 확인합니다.")

    tab1, tab2, tab3 = st.tabs([
        "🔠 제목 & 본문",
        "✍️ 마크다운 & write",
        "💻 코드 & 수식",
    ])

    with tab1:
        render_headings_and_body()
    with tab2:
        render_markdown_and_write()
    with tab3:
        render_code_and_math()
