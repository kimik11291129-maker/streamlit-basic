import pandas as pd
import streamlit as st


def render_markdown_and_write():
    # st.markdown의 다양한 표현과 st.write의 매직 기능을 확인하는 함수
    st.subheader("1. `st.markdown` - 마크다운 & 컬러/이모지 텍스트")
    st.markdown(
        "일반 마크다운: **굵게**, *기울임*, `코드`, [링크](https://streamlit.io)"
    )
    st.markdown(":blue[파란 글씨] / :red[빨간 글씨] / :green[초록 글씨] :sunglasses:")

    st.divider()

    st.subheader("2. `st.write` - 무엇이든 그려주는 매직 함수")
    st.caption("타입에 따라 자동으로 적절한 형태로 렌더링됩니다.")

    st.write("① 문자열:", "그냥 문자열도 렌더링")
    st.write("② 딕셔너리:", {"이름": "홍길동", "나이": 25})
    st.write("③ 데이터프레임:", pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
    st.write("④ 여러 인자 나열:", 1, "개", True)
