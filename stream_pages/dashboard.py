from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np

pages_dir = Path(__file__).parent


def render_dashboard_page():
    """데이터 분석 및 차트 시각화 대시보드 페이지를 렌더링합니다."""
    # 미로그인 상태 접근 차단
    if not st.user.is_logged_in:
        st.warning("⚠️ 로그인이 필요한 페이지입니다.")
        st.page_link(pages_dir / "main.py", label="로그인 페이지로 이동", icon="🔐")
        st.stop()

    st.title("📊 데이터 분석 대시보드")
    st.caption("차트, 메트릭 및 필터 위젯을 활용한 실시간 인터랙티브 대시보드")

    # 상단 요약 메트릭
    col1, col2, col3 = st.columns(3)
    col1.metric("총 방문자 수", "12,450명", "+14%")
    col2.metric("전환율", "3.8%", "+0.5%")
    col3.metric("평균 체류 시간", "4분 21초", "-12초")

    st.divider()

    # 인터랙티브 컨트롤 필터
    st.subheader("데이터 시뮬레이션 필터")
    c1, c2 = st.columns(2)
    with c1:
        data_points = st.slider("데이터 포인트 개수", min_value=10, max_value=100, value=30, step=10)
    with c2:
        chart_type = st.selectbox("차트 종류 선택", ["선 차트 (Line)", "면적 차트 (Area)", "막대 차트 (Bar)"])

    # 샘플 시계열 데이터 생성
    dates = pd.date_range("2026-01-01", periods=data_points)
    chart_data = pd.DataFrame(
        np.random.randn(data_points, 3).cumsum(axis=0) + 50,
        index=dates,
        columns=["유입량 (A)", "구매량 (B)", "이탈량 (C)"]
    )

    # 선택한 차트 렌더링
    if chart_type == "선 차트 (Line)":
        st.line_chart(chart_data)
    elif chart_type == "면적 차트 (Area)":
        st.area_chart(chart_data)
    else:
        st.bar_chart(chart_data)

    st.divider()

    # 다른 페이지로 이동 링크
    st.subheader("빠른 페이지 이동")
    c_link1, c_link2 = st.columns(2)
    with c_link1:
        st.page_link(pages_dir / "main.py", label="홈으로 돌아가기", icon="🏠")
    with c_link2:
        st.page_link(pages_dir / "settings.py", label="대시보드 환경설정으로 이동", icon="⚙️")


render_dashboard_page()
