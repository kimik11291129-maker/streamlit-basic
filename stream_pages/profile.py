from pathlib import Path
import streamlit as st

pages_dir = Path(__file__).parent


def render_profile_page():
    """사용자 프로필 관리 및 세션 상태(st.session_state) 연동 페이지를 렌더링합니다."""
    # 미로그인 상태 접근 차단
    if not st.user.is_logged_in:
        st.warning("⚠️ 로그인이 필요한 페이지입니다.")
        st.page_link(pages_dir / "main.py", label="로그인 페이지로 이동", icon="🔐")
        st.stop()

    st.title("👤 사용자 프로필")
    st.caption("프로필 정보를 수정하고 다른 페이지에서도 유지되는 session_state를 테스트합니다.")

    # 로그인한 실제 사용자 정보 연동
    login_name = st.user.get("name", "홍길동")
    login_email = st.user.get("email", "user@example.com")
    login_picture = st.user.get("picture", None)

    # session_state 초기화
    if "user_name" not in st.session_state:
        st.session_state.user_name = login_name
    if "user_role" not in st.session_state:
        st.session_state.user_role = "데이터 분석가"
    if "user_bio" not in st.session_state:
        st.session_state.user_bio = f"Google 계정({login_email})으로 로그인된 사용자입니다."

    # 프로필 카드 표시
    st.subheader("현재 프로필 카드")
    with st.container(border=True):
        col_avatar, col_info = st.columns([1, 4])
        with col_avatar:
            if login_picture:
                st.image(login_picture, width=100)
            else:
                st.image("https://api.dicebear.com/7.x/bottts/svg?seed=" + st.session_state.user_name, width=100)
        with col_info:
            st.markdown(f"### {st.session_state.user_name}")
            st.write(f"📧 **이메일:** `{login_email}`")
            st.badge(st.session_state.user_role)
            st.write(st.session_state.user_bio)

    st.divider()

    # 정보 수정 폼
    st.subheader("프로필 정보 수정")
    new_name = st.text_input("이름", value=st.session_state.user_name)
    new_role = st.selectbox(
        "직무 / 역할",
        ["데이터 분석가", "소프트웨어 엔지니어", "AI 연구원", "프로덕트 매니저"],
        index=["데이터 분석가", "소프트웨어 엔지니어", "AI 연구원", "프로덕트 매니저"].index(st.session_state.user_role),
    )
    new_bio = st.text_area("자기소개", value=st.session_state.user_bio)

    if st.button("프로필 저장", type="primary"):
        st.session_state.user_name = new_name
        st.session_state.user_role = new_role
        st.session_state.user_bio = new_bio
        st.success("프로필이 성공적으로 저장되었습니다! (홈 또는 대시보드 페이지로 이동해도 유지됩니다)")

    st.divider()

    # 페이지 이동 링크
    st.subheader("연관 페이지")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link(pages_dir / "settings.py", label="계정 및 환경설정", icon="⚙️")
    with col2:
        if st.button("홈으로 이동하여 변경사항 확인 (st.switch_page)"):
            st.switch_page(pages_dir / "main.py")


render_profile_page()
