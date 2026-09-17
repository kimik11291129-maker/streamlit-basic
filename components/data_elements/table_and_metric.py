import pandas as pd
import streamlit as st


def render_table_and_metric():
    # st.table의 정적 표시와 st.metric의 지표 표시를 확인하는 함수
    st.subheader("1. `st.table` - 정적 표")
    st.caption("st.dataframe과 달리 정렬/스크롤이 없는 고정된 표입니다.")

    df = pd.DataFrame({"제품": ["사과", "바나나", "체리"], "가격": [1500, 800, 3200]})
    st.table(df)

    st.divider()

    st.subheader("2. `st.metric` - 핵심 지표 카드")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("매출", "₩1,200,000", "+8.2%")
    with col2:
        st.metric("방문자 수", "3,421", "-2.1%", delta_color="inverse")
    with col3:
        st.metric("전환율", "4.5%", "0%", delta_color="off")
