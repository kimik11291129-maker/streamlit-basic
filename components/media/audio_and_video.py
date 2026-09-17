import streamlit as st


def render_audio_and_video():
    # st.audio와 st.video의 동작을 확인하는 함수 (파일 업로드 기반)
    st.subheader("1. `st.audio` - 오디오 플레이어")
    st.caption("오디오 파일을 업로드하면 플레이어가 나타납니다.")
    audio_file = st.file_uploader("오디오 파일 업로드", type=["mp3", "wav", "ogg"], key="audio_uploader")
    if audio_file is not None:
        st.audio(audio_file)

    st.divider()

    st.subheader("2. `st.video` - 비디오 플레이어")
    st.caption("비디오 파일을 업로드하면 플레이어가 나타납니다 (start_time 옵션 지원).")
    video_file = st.file_uploader("비디오 파일 업로드", type=["mp4", "mov", "webm"], key="video_uploader")
    start_time = st.number_input("시작 시간(초)", min_value=0, value=0, key="video_start")
    if video_file is not None:
        st.video(video_file, start_time=start_time)
