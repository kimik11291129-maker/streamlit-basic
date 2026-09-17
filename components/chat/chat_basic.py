import streamlit as st


def render_chat_basic():
    # st.chat_message와 st.chat_input으로 대화형 UI를 구성하는 함수
    st.subheader("`st.chat_message` + `st.chat_input` - 채팅 인터페이스")
    st.caption("메시지를 입력하면 대화 목록 아래에 이어서 쌓입니다.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"},
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("메시지를 입력하세요", key="chat_basic_input")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append(
            {"role": "assistant", "content": f"'{user_input}' 라고 말씀하셨네요!"}
        )
        st.rerun()
