import streamlit as st


def render_columns_and_containers():
    # st.columns와 st.container의 동작을 확인하는 함수

    st.subheader("`st.columns` - 가로 열 배치")
    st.caption("화면을 가로로 분할하여 위젯을 나란히 배치합니다.")

    col1, col2, col3 = st.columns(3)
    col1.write("**첫 번째 열**")
    col1.button("버튼 A", key="col_btn_a")
    col2.write("**두 번째 열**")
    col2.button("버튼 B", key="col_btn_b")
    col3.write("**세 번째 열**")
    col3.button("버튼 C", key="col_btn_c")

    st.caption("비율 지정 (2:1:1):")
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.info("넓은 열 (2)")
    c2.warning("좁은 열 (1)")
    c3.error("좁은 열 (1)")

    st.divider()

    st.subheader("`st.container` - 컨테이너 그룹핑")
    st.caption("여러 요소를 하나의 컨테이너로 묶어 순서를 조절할 수 있습니다.")

    with st.container(border=True):
        st.write("이 영역은 `border=True` 컨테이너 안에 있습니다.")
        st.slider("컨테이너 안 슬라이더", 0, 100, 50, key="container_slider")

    st.write("이 텍스트는 컨테이너 바깥입니다.")

