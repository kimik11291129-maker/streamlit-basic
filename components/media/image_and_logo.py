import streamlit as st


def render_image_and_logo():
    # st.image와 st.logo의 동작을 확인하는 함수
    st.subheader("1. `st.image` - 이미지 표시")
    st.image(
        "https://static.streamlit.io/examples/cat.jpg",
        caption="고양이 예시 이미지 (Streamlit 공식 예제 리소스)",
        width=300,
    )

    st.divider()

    st.subheader("2. `st.logo` - 앱 로고 (사이드바 상단)")
    st.caption("사이드바 상단에 로고가 표시됩니다. ← 사이드바를 확인하세요!")
    st.logo(
        "https://static.streamlit.io/examples/cat.jpg",
        link="https://streamlit.io",
    )
