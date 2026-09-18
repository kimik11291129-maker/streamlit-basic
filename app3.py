import streamlit as st

st.set_page_config(page_title="Streamlit 사용자 인증", page_icon="🔐")

st.title("🔐 사용자 인증 (Authentication)")
st.caption("공식 Streamlit API Reference (`st.login`, `st.logout`, `st.user`) 실습")

# 1. 로그인 여부 확인 (st.user.is_logged_in)
if not st.user.is_logged_in:
    st.info("현재 로그인되어 있지 않습니다. 아래 버튼을 눌러 로그인을 진행하세요.")
    
    # st.login() 호출 - secrets.toml의 [auth] 설정을 사용해 OIDC 로그인 시작
    if st.button("로그인 (Log in)", type="primary"):
        st.login()
else:
    # 2. 로그인 성공 시 사용자 정보 표시 (st.user)
    st.success(f"환영합니다, **{st.user.name}**님! 👋")
    st.write(f"- **이메일:** {st.user.email}")
    
    # st.user 객체에 담긴 세부 속성 확인 (Playground 실습용)
    st.subheader("📋 세션 사용자 상세 정보 (`st.user`)")
    st.write(st.user)
    
    # 3. 로그아웃 (st.logout())
    if st.button("로그아웃 (Log out)"):
        st.logout()