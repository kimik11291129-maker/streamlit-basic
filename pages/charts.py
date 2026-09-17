import streamlit as st
from components.charts.native_charts import render_native_charts
from components.charts.map_chart import render_map_chart


def render_charts_page():
    # 차트 요소 카테고리를 하위 탭으로 나누어 보여주는 페이지 함수
    st.title("📈 차트 요소")
    st.caption("Streamlit 공식 Chart elements의 다양한 기능을 카테고리별 탭으로 확인합니다.")

    tab1, tab2 = st.tabs([
        "📉 기본 차트 (line/area/bar/scatter)",
        "🗺️ 지도 차트",
    ])

    with tab1:
        render_native_charts()
    with tab2:
        render_map_chart()
