import streamlit as st
from components.data_elements.dataframe_and_editor import render_dataframe_and_editor
from components.data_elements.table_and_metric import render_table_and_metric
from components.data_elements.json_viewer import render_json_viewer


def render_data_elements_page():
    # 데이터 요소 카테고리를 하위 탭으로 나누어 보여주는 페이지 함수
    st.title("📊 데이터 요소")
    st.caption("Streamlit 공식 Data elements의 다양한 기능을 카테고리별 탭으로 확인합니다.")

    tab1, tab2, tab3 = st.tabs([
        "🧮 데이터프레임 & 에디터",
        "📋 테이블 & 지표",
        "🌳 JSON 뷰어",
    ])

    with tab1:
        render_dataframe_and_editor()
    with tab2:
        render_table_and_metric()
    with tab3:
        render_json_viewer()
