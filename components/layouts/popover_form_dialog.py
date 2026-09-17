import streamlit as st


def render_popover_form_dialog():
    # st.popover, st.form, @st.dialog의 동작을 확인하는 함수

    st.subheader("`st.popover` - 팝오버 (말풍선)")
    st.caption("버튼을 누르면 말풍선처럼 떠오르는 팝업 영역입니다.")

    with st.popover("🔧 설정 열기"):
        st.write("팝오버 안의 위젯들:")
        pop_name = st.text_input("이름 입력", key="pop_name")
        pop_color = st.color_picker("테마 색상", "#FF4B4B", key="pop_color")

    st.write(f"팝오버에서 입력된 이름: **{pop_name}**, 색상: **{pop_color}**")

    st.divider()

    st.subheader("`st.form` - 양식 (제출 버튼으로 일괄 반영)")
    st.caption("입력할 때마다 리런 되지 않고, 제출 버튼을 누를 때 한번에 반영됩니다.")

    with st.form("sample_form"):
        form_name = st.text_input("이름", key="form_name")
        form_age = st.number_input("나이", min_value=0, max_value=150, value=25, key="form_age")
        form_submitted = st.form_submit_button("제출하기")

    if form_submitted:
        st.success(f"제출 완료! 이름: {form_name}, 나이: {form_age}")

    st.divider()

    st.subheader("`@st.dialog` - 다이얼로그 (모달 팝업)")
    st.caption("버튼을 누르면 화면 위에 모달 팝업이 뜹니다.")

    @st.dialog("투표하기")
    def vote_dialog():
        # 다이얼로그 모달 안에서 투표 선택 UI를 보여주는 함수
        item = st.radio("좋아하는 과일은?", ["사과 🍎", "바나나 🍌", "체리 🍒"], key="dialog_radio")
        if st.button("확인", key="dialog_confirm"):
            st.session_state.vote_result = item
            st.rerun()

    if st.button("투표 다이얼로그 열기", key="open_dialog"):
        vote_dialog()

    if "vote_result" in st.session_state:
        st.write(f"투표 결과: **{st.session_state.vote_result}**")

