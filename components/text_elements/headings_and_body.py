import streamlit as st


def render_headings_and_body():
    # 제목, 헤더, 캡션 등 기본 텍스트 요소들을 렌더링하는 함수
    st.subheader("1. 제목 계층 (`st.title` / `st.header` / `st.subheader`)")
    st.title("타이틀입니다 (st.title)")
    st.header("헤더입니다 (st.header)", divider="rainbow")
    st.subheader("서브헤더입니다 (st.subheader)")

    st.divider()

    st.subheader("2. 캡션 & 일반 텍스트 (`st.caption` / `st.text`)")
    st.caption("캡션은 작은 글씨의 보조 설명 텍스트입니다.")
    st.text("st.text는 마크다운이 적용되지 않는 순수 텍스트입니다. **굵게** 안 됨.")
