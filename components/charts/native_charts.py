import numpy as np
import pandas as pd
import streamlit as st


def render_native_charts():
    # Streamlit 내장 차트 함수들(line/area/bar/scatter)을 확인하는 함수
    chart_data = pd.DataFrame(
        np.random.randn(20, 3), columns=["서울", "부산", "대구"]
    )

    st.subheader("1. `st.line_chart` / `st.area_chart` / `st.bar_chart`")
    tab_line, tab_area, tab_bar = st.tabs(["라인 차트", "영역 차트", "막대 차트"])
    with tab_line:
        st.line_chart(chart_data)
    with tab_area:
        st.area_chart(chart_data)
    with tab_bar:
        st.bar_chart(chart_data)

    st.divider()

    st.subheader("2. `st.scatter_chart` - 산점도")
    scatter_data = pd.DataFrame(
        {
            "x": np.random.randn(50),
            "y": np.random.randn(50),
            "크기": np.random.randint(10, 100, 50),
        }
    )
    st.scatter_chart(scatter_data, x="x", y="y", size="크기", color="#FF4B4B")
