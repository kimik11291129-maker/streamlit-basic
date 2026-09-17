import streamlit as st


def render_utilities():
    # st.empty, st.sidebar, st.space, st.bottom의 동작을 확인하는 함수

    st.subheader("`st.empty` - 빈 자리 표시자 (동적 교체)")
    st.caption("나중에 콘텐츠를 동적으로 교체할 수 있는 빈 슬롯입니다.")

    placeholder = st.empty()
    placeholder.info("이 자리는 `st.empty()`로 만든 빈 영역입니다.")

    if st.button("내용 교체하기", key="replace_empty"):
        placeholder.success("✅ 내용이 교체되었습니다!")

    st.divider()

    st.subheader("`st.sidebar` - 사이드바")
    st.caption("좌측 사이드바에 위젯을 배치합니다. ← 사이드바를 확인하세요!")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧪 레이아웃 테스트 영역")
    sidebar_val = st.sidebar.slider("사이드바 슬라이더", 0, 100, 30, key="sidebar_slider")
    st.write(f"사이드바에서 선택한 값: **{sidebar_val}**")

    st.divider()

    st.subheader("`st.space` - 빈 간격 삽입")
    st.caption("요소 사이에 수직 여백을 삽입합니다.")

    st.write("위 텍스트")
    st.space("lg")
    st.write("아래 텍스트 (위와 `lg` 간격)")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("sm 간격:")
        st.button("위 버튼", key="space_btn1")
        st.space("sm")
        st.button("아래 버튼", key="space_btn2")
    with col_s2:
        st.write("xl 간격:")
        st.button("위 버튼", key="space_btn3")
        st.space("xl")
        st.button("아래 버튼", key="space_btn4")

    st.divider()

    st.subheader("`st.bottom` - 하단 고정 컨테이너")
    st.caption("화면 맨 아래에 고정되는 영역입니다. ↓ 페이지 하단을 확인하세요!")

    with st.bottom():
        st.write("📌 이 영역은 `st.bottom()`으로 하단에 고정되어 있습니다.")

