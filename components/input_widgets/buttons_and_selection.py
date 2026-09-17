import streamlit as st


def render_buttons_and_selection():
    # 클릭 버튼, 토글, 라디오 및 다중 선택 위젯을 렌더링하는 함수
    st.subheader("1. 클릭 및 토글 위젯")
    col1, col2, col3 = st.columns(3)
    with col1:
        btn = st.button("일반 버튼 (st.button)")
        st.write("버튼 클릭 상태:", btn)

    with col2:
        chk = st.checkbox("체크박스 (st.checkbox)", value=True)
        st.write("체크박스 상태:", chk)

    with col3:
        tog = st.toggle("토글 스위치 (st.toggle)", value=False)
        st.write("토글 상태:", tog)

    st.divider()

    st.subheader("2. 단일 및 다중 선택 위젯")
    col4, col5 = st.columns(2)
    with col4:
        radio_val = st.radio("라디오 버튼 (st.radio)", ["사과 🍎", "바나나 🍌", "포도 🍇"])
        st.write("선택된 과일:", radio_val)

        pills_val = st.pills("알약 버튼 (st.pills)", ["Python", "Streamlit", "AI", "Cloud"], default="Streamlit")
        st.write("선택된 태그:", pills_val)

    with col5:
        select_val = st.selectbox("셀렉트박스 (st.selectbox)", ["서울", "부산", "대구", "인천", "광주"])
        st.write("선택된 도시:", select_val)

        seg_val = st.segmented_control("세그먼트 컨트롤 (st.segmented_control)", ["기본", "그리드", "상세"], default="기본")
        st.write("선택된 모드:", seg_val)

    st.divider()

    multi_val = st.multiselect(
        "다중 선택박스 (st.multiselect)",
        ["축구 ⚽", "농구 🏀", "야구 ⚾", "수영 🏊", "테니스 🎾"],
        default=["축구 ⚽", "야구 ⚾"],
    )
    st.write("선택된 항목 목록:", multi_val)

