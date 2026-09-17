import streamlit as st

from chat.config import mask_key, resolve_api_key

SECURITY_NOTICE = """
- **인증 체계 없음** — 이 앱은 학습·데모용입니다. 공개 URL이므로 주소를 아는 누구나 접근할 수 있습니다.
- **본인 키만 사용됨** — 서버에 등록된 키는 절대 자동으로 쓰이지 않으며, 반드시 각자 자신의 OpenAI API 키를 입력해야 채팅이 가능합니다.
- **API 키 보관 방식** — 입력한 키는 서버 세션 메모리에만 두며 DB·파일에 저장하지 않습니다. 서버가 재시작되거나 로그아웃하면 사라집니다.
- **채팅 내용 평문 저장** — 대화는 서버의 SQLite에 암호화 없이 저장됩니다. 개인정보·비밀번호·사내 자료는 입력하지 마세요.
- **채팅창에 키 입력 금지** — 채팅 내용은 DB에 남습니다. 실수로 붙여넣는 경우를 대비해 `sk-`로 시작하는 문자열은 자동으로 가리지만, 애초에 입력하지 않는 것이 안전합니다.
- **과금 주의** — API 키는 사용량 과금과 직결됩니다. 사용 한도(usage limit)를 설정한 테스트 전용 키를 권장합니다.
- **공용 PC 사용 시** — 사용을 마치면 반드시 사이드바에서 로그아웃하세요.
- **유출 대응** — 키가 노출된 것 같으면 platform.openai.com에서 즉시 폐기(revoke)하세요.
"""


def render_login_page():
    _, center, _ = st.columns([1, 3, 1])

    with center:
        st.title("🔐 로그인")
        st.caption("본인의 OpenAI API 키로 로그인합니다.")

        st.warning(
            "**보안 안내** — 이 앱은 학습·데모용이며 실제 사용자 인증 체계가 없습니다. "
            "민감한 정보를 입력하지 마세요."
        )

        with st.expander("⚠️ 보안 취약점 상세 안내 (반드시 읽어주세요)", expanded=True):
            st.markdown(SECURITY_NOTICE)

        st.divider()

        with st.form("login_form"):
            key_input = st.text_input(
                "OpenAI API 키 등록",
                type="password",
                placeholder="sk-...",
                help="https://platform.openai.com/api-keys 에서 발급",
            )
            submitted = st.form_submit_button("로그인", use_container_width=True)

        if submitted and key_input:
            st.session_state.user_api_key = key_input.strip()
            st.rerun()


def render_account_section():
    # 채팅/내역 페이지 사이드바 공통 계정 영역
    key = resolve_api_key()

    st.markdown("### 👤 계정")
    st.code(mask_key(key), language=None)

    if st.button("🚪 로그아웃", use_container_width=True):
        st.session_state.clear()
        st.rerun()
