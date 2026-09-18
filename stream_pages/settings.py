from pathlib import Path
import streamlit as st

pages_dir = Path(__file__).parent


def render_settings_page():
    """애플리케이션 환경 설정 및 옵션 제어 페이지를 렌더링합니다."""
    # 미로그인 상태 접근 차단
    if not st.user.is_logged_in:
        st.warning("⚠️ 로그인이 필요한 페이지입니다.")
        st.page_link(pages_dir / "main.py", label="로그인 페이지로 이동", icon="🔐")
        st.stop()

    st.title("⚙️ 환경 설정")
    st.caption("앱 동작 모드, 알림 설정 및 테마 옵션을 제어합니다.")

    st.subheader("일반 설정")
    col1, col2 = st.columns(2)
    with col1:
        st.toggle("다크 모드 강제 적용", value=False)
        st.toggle("자동 새로고침 활성화", value=True)
    with col2:
        st.toggle("이메일 알림 받기", value=True)
        st.toggle("실험적 기능(Beta) 미리보기", value=False)

    st.divider()

    st.subheader("인터페이스 옵션")
    theme_color = st.color_picker("포인트 테마 컬러", "#FF4B4B")
    st.write(f"선택된 색상 코드: `{theme_color}`")

    page_layout = st.radio("기본 화면 레이아웃", ["중앙 정렬 (Centered)", "전체 화면 (Wide)"], horizontal=True)
    st.write(f"현재 선택된 레이아웃: **{page_layout}**")

    st.divider()

    # 페이지 이동 링크
    st.subheader("빠른 메뉴 이동")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.page_link(pages_dir / "main.py", label="메인 홈", icon="🏠")
    with c2:
        st.page_link(pages_dir / "dashboard.py", label="데이터 분석", icon="📊")
    with c3:
        st.page_link(pages_dir / "profile.py", label="내 프로필", icon="👤")


render_settings_page()
