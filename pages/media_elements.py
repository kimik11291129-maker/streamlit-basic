import streamlit as st
from components.media.image_and_logo import render_image_and_logo
from components.media.audio_and_video import render_audio_and_video


def render_media_elements_page():
    # 미디어 요소 카테고리를 하위 탭으로 나누어 보여주는 페이지 함수
    st.title("🖼️ 미디어 요소")
    st.caption("Streamlit 공식 Media elements의 다양한 기능을 카테고리별 탭으로 확인합니다.")

    tab1, tab2 = st.tabs([
        "🖼️ 이미지 & 로고",
        "🎵 오디오 & 비디오",
    ])

    with tab1:
        render_image_and_logo()
    with tab2:
        render_audio_and_video()
