from pathlib import Path
import streamlit as st

pages_dir = Path(__file__).parent


def render_main_page():
    """메인 홈 화면을 렌더링하며, 로그인 상태에 따라 로그인 화면 또는 대시보드 포털 화면을 표시합니다."""
    # 1. 로그인하지 않은 경우 -> 로그인 화면 렌더링
    if not st.user.is_logged_in:
        st.title("🔐 로그인 필요")
        st.info("현재 로그인되어 있지 않습니다. 서비스의 다른 페이지(데이터 분석, 프로필, 설정 등)에 접근하려면 먼저 로그인을 완료해 주세요.")

        with st.container(border=True):
            st.subheader("계정 로그인")
            st.write("Google 계정을 통해 안전하게 인증을 진행합니다.")
            if st.button("Google 계정으로 로그인 (Log in)", type="primary"):
                st.login()

        st.caption("🔒 로그인하기 전까지는 사이드바 및 다른 페이지 메뉴가 숨겨집니다.")
        return

    # 2. 로그인된 경우 -> 전체 메인 포털 화면 렌더링
    st.title("🏠 메인 포털")
    st.success(f"환영합니다, **{st.user.name}**님 ({st.user.email})! 👋")
    st.caption("로그인이 완료되어 모든 서비스 페이지에 접근하실 수 있습니다.")

    # 쿼리 파라미터가 전달된 경우 표시
    if st.query_params:
        st.info(f"📥 전달받은 쿼리 파라미터: `{dict(st.query_params)}`")

    st.divider()

    # 빠른 바로가기 카드 섹션
    st.subheader("📌 바로가기 메뉴 (`st.page_link`)")
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 📊 데이터 분석")
            st.write("차트, 필터 및 시뮬레이션 지표를 확인합니다.")
            st.page_link(pages_dir / "dashboard.py", label="대시보드 바로가기", icon="📊")

        with st.container(border=True):
            st.markdown("### 👤 사용자 프로필")
            st.write("프로필 정보를 조회하고 수정할 수 있습니다.")
            st.page_link(pages_dir / "profile.py", label="프로필 관리 바로가기", icon="👤")

    with col2:
        with st.container(border=True):
            st.markdown("### ⚙️ 환경 설정")
            st.write("테마 색상 및 알림 옵션을 설정합니다.")
            st.page_link(pages_dir / "settings.py", label="환경 설정 바로가기", icon="⚙️")

        with st.container(border=True):
            st.markdown("### 🧭 내비게이션 실습")
            st.write("공식 Navigation API(switch_page, page_link 등)를 실습합니다.")
            st.page_link(pages_dir / "navigation_page.py", label="API 실습실 바로가기", icon="🧭")

    st.divider()

    # st.switch_page 버튼 전환 테스트
    st.subheader("🚀 프로그래밍 방식 페이지 즉시 전환 (`st.switch_page`)")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("📊 대시보드로 즉시 전환", type="primary"):
            st.switch_page(pages_dir / "dashboard.py")
    with b2:
        if st.button("👤 프로필로 즉시 전환"):
            st.switch_page(pages_dir / "profile.py")
    with b3:
        if st.button("🧭 내비 실습실로 전환"):
            st.switch_page(pages_dir / "navigation_page.py")

    st.divider()

    # 로그아웃 버튼
    if st.button("🚪 로그아웃 (Log out)"):
        st.logout()


render_main_page()