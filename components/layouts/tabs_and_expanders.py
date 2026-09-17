import streamlit as st


def render_tabs_and_expanders():
    # st.tabs와 st.expander의 동작을 확인하는 함수

    st.subheader("`st.tabs` - 탭 레이아웃")
    st.caption("관련 콘텐츠를 탭으로 나눠 전환하며 볼 수 있습니다.")

    tab_a, tab_b, tab_c = st.tabs(["🐱 고양이", "🐶 강아지", "🐹 햄스터"])
    with tab_a:
        st.write("고양이 탭 콘텐츠입니다. 🐱")
        st.text_input("고양이 이름", value="나비", key="cat_name")
    with tab_b:
        st.write("강아지 탭 콘텐츠입니다. 🐶")
        st.text_input("강아지 이름", value="바둑이", key="dog_name")
    with tab_c:
        st.write("햄스터 탭 콘텐츠입니다. 🐹")
        st.text_input("햄스터 이름", value="햄찌", key="hamster_name")

    st.divider()

    st.subheader("`st.expander` - 접기/펼치기 영역")
    st.caption("클릭하면 내용이 펼쳐지는 접이식 영역입니다.")

    with st.expander("클릭하여 세부 정보 보기"):
        st.write("이 안에는 숨겨진 상세 콘텐츠가 들어갑니다.")
        st.code("print('expander 안의 코드')")

    with st.expander("처음부터 펼쳐진 영역", expanded=True):
        st.write("`expanded=True`로 설정하면 처음부터 열려 있습니다.")
        st.color_picker("색상 선택 (expander 내부)", "#00FF00", key="exp_color")

