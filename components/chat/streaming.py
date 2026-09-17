import time

import streamlit as st


def _stream_words(text: str):
    # 단어 단위로 잘라 한 글자씩 지연 출력하는 제너레이터
    for word in text.split():
        yield word + " "
        time.sleep(0.1)


def render_streaming():
    # st.write_stream으로 타이핑 효과를 내는 스트리밍 출력을 확인하는 함수
    st.subheader("`st.write_stream` - 스트리밍(타이핑 효과) 출력")
    st.caption("제너레이터를 넘기면 단어 단위로 순차적으로 출력됩니다.")

    if st.button("스트리밍 응답 생성하기", key="stream_btn"):
        response_text = "이것은 st.write_stream을 이용한 스트리밍 출력 데모입니다. 마치 챗봇이 실시간으로 답하는 것처럼 보입니다."
        st.write_stream(_stream_words(response_text))
