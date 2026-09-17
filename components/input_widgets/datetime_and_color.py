import streamlit as st


def render_datetime_and_color():
    # 날짜, 시간 선택기 및 컬러 피커 위젯을 렌더링하는 함수
    st.subheader("1. 날짜 및 시간 선택")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        date_val = st.date_input("날짜 선택 (st.date_input)")
        st.write("선택된 날짜:", date_val)

    with col_d2:
        time_val = st.time_input("시간 선택 (st.time_input)")
        st.write("선택된 시간:", time_val)

    st.divider()

    st.subheader("2. 색상 선택기")
    color_val = st.color_picker("색상 선택 (st.color_picker)", "#FF4B4B")
    st.write("선택된 색상 코드 (HEX):", color_val)

