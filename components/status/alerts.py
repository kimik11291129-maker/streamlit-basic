import streamlit as st


def render_alerts():
    # 알림 박스(success/info/warning/error/exception)를 렌더링하는 함수
    st.subheader("`st.success` / `st.info` / `st.warning` / `st.error`")
    st.success("성공했습니다! (st.success)", icon="✅")
    st.info("참고 정보입니다. (st.info)", icon="ℹ️")
    st.warning("주의가 필요합니다. (st.warning)", icon="⚠️")
    st.error("오류가 발생했습니다. (st.error)", icon="🚨")

    st.divider()

    st.subheader("`st.exception` - 예외 트레이스백 표시")
    if st.button("예외 발생시켜보기"):
        st.exception(ValueError("이것은 st.exception 데모용 예외입니다."))
