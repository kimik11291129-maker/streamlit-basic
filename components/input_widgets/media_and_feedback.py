import streamlit as st


def render_media_and_feedback():
    # 파일 업로더, 별점/좋아요 피드백 및 채팅 입력창 위젯을 렌더링하는 함수
    st.subheader("1. 파일 업로드 위젯")
    uploaded_file = st.file_uploader("파일 업로더 (st.file_uploader)")
    st.write("업로드된 파일 정보:", uploaded_file)

    st.divider()

    st.subheader("2. 별점 및 피드백 위젯 (Streamlit 최신 위젯)")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        stars = st.feedback("stars")
        st.write("별점 평가 결과 (0~4):", stars)

    with col_f2:
        thumbs = st.feedback("thumbs")
        st.write("좋아요/싫어요 평가 (0 또는 1):", thumbs)

    st.divider()

    st.subheader("3. 하단 채팅 입력창")
    chat_input_val = st.chat_input("채팅 입력창 (st.chat_input) - 메시지를 입력해보세요")
    st.write("입력된 채팅 메시지:", chat_input_val)

