import streamlit as st


def render_text_and_numeric():
    # 텍스트 입력창, 장문 메모 및 숫자 슬라이더 위젯들을 렌더링하는 함수
    st.subheader("1. 텍스트 입력 위젯")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        text_val = st.text_input("한 줄 텍스트 (st.text_input)", value="홍길동", placeholder="이름을 입력하세요")
        st.write("입력값:", text_val)

        pw_val = st.text_input("비밀번호 마스킹 (type='password')", type="password", value="1234")
        st.write("비밀번호 길이:", len(pw_val))

    with col_t2:
        search_val = st.text_input("검색창 타입 (type='search')", placeholder="검색어를 입력해보세요", type="search")
        st.write("검색어:", search_val)

        limit_val = st.text_input("글자 수 제한 (max_chars=6)", max_chars=6, placeholder="최대 6글자")
        st.write("제한 입력값:", limit_val)

    st.divider()

    st.subheader("2. 장문 텍스트 입력")
    area_val = st.text_area("여러 줄 텍스트 (st.text_area)", value="줄바꿈이 가능한\n여러 줄 메모입니다.", height=100)
    st.write("작성된 내용:", area_val)

    st.divider()

    st.subheader("3. 숫자 입력 및 슬라이더")
    col_n1, col_n2, col_n3 = st.columns(3)
    with col_n1:
        num_val = st.number_input("숫자 입력 (st.number_input)", min_value=0, max_value=100, value=25, step=5)
        st.write("선택된 숫자:", num_val)

    with col_n2:
        slider_val = st.slider("숫자 슬라이더 (st.slider)", min_value=0, max_value=100, value=60)
        st.write("슬라이더 값:", slider_val)

    with col_n3:
        range_val = st.slider("범위 슬라이더", min_value=0, max_value=100, value=(20, 80))
        st.write("선택된 범위:", range_val)

    select_slide_val = st.select_slider(
        "문자열 슬라이더 (st.select_slider)",
        options=["XS", "S", "M", "L", "XL", "XXL"],
        value="M",
    )
    st.write("선택된 사이즈:", select_slide_val)

