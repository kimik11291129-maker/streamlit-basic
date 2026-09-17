import streamlit as st


def render_celebrations():
    # st.toast, st.balloons, st.snow의 동작을 확인하는 함수
    st.subheader("`st.toast` - 잠깐 나타났다 사라지는 알림")
    if st.button("토스트 띄우기", key="toast_btn"):
        st.toast("저장되었습니다!", icon="🎉")

    st.divider()

    st.subheader("`st.balloons` / `st.snow` - 화면 전체 애니메이션")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎈 풍선 날리기", key="balloons_btn"):
            st.balloons()
    with col2:
        if st.button("❄️ 눈 내리기", key="snow_btn"):
            st.snow()
