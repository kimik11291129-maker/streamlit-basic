import streamlit as st
from components.layouts.columns_and_containers import render_columns_and_containers
from components.layouts.popover_form_dialog import render_popover_form_dialog
from components.layouts.tabs_and_expanders import render_tabs_and_expanders
from components.layouts.utilities import render_utilities


def render_layouts_page():
    # 레이아웃 & 컨테이너 카테고리를 하위 탭으로 나누어 보여주는 페이지 함수
    st.title("📐 레이아웃 & 컨테이너")
    st.caption("Streamlit 공식 Layouts and Containers의 모든 기능을 카테고리별 탭으로 확인합니다.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 컬럼 & 컨테이너",
        "📑 탭 & 확장",
        "💬 팝오버 & 폼 & 다이얼로그",
        "🔧 유틸리티 (empty, sidebar, space, bottom)",
    ])

    with tab1:
        render_columns_and_containers()
    with tab2:
        render_tabs_and_expanders()
    with tab3:
        render_popover_form_dialog()
    with tab4:
        render_utilities()

