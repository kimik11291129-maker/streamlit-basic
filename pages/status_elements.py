import streamlit as st
from components.status.alerts import render_alerts
from components.status.progress_and_spinner import render_progress_and_spinner
from components.status.celebrations import render_celebrations


def render_status_elements_page():
    # 상태 및 알림 요소 카테고리를 하위 탭으로 나누어 보여주는 페이지 함수
    st.title("🚦 상태 & 알림 요소")
    st.caption("Streamlit 공식 Status elements의 다양한 기능을 카테고리별 탭으로 확인합니다.")

    tab1, tab2, tab3 = st.tabs([
        "🔔 알림 박스",
        "⏳ 진행률 & 스피너",
        "🎉 축하 애니메이션",
    ])

    with tab1:
        render_alerts()
    with tab2:
        render_progress_and_spinner()
    with tab3:
        render_celebrations()
