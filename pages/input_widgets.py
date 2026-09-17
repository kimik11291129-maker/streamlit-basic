import streamlit as st
from components.input_widgets.buttons_and_selection import render_buttons_and_selection
from components.input_widgets.datetime_and_color import render_datetime_and_color
from components.input_widgets.media_and_feedback import render_media_and_feedback
from components.input_widgets.text_and_numeric import render_text_and_numeric


def render_input_widgets_page():
    # 인풋 위젯 카테고리를 하위 탭으로 나누어 보여주는 페이지 함수
    st.title("🎛️ 인풋 위젯")
    st.caption("Streamlit 공식 Input Widgets의 다양한 위젯들을 카테고리별 탭으로 확인합니다.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔘 선택 & 버튼",
        "✍️ 텍스트 & 숫자",
        "📅 날짜, 시간 & 색상",
        "📁 미디어 & 피드백",
    ])

    with tab1:
        render_buttons_and_selection()
    with tab2:
        render_text_and_numeric()
    with tab3:
        render_datetime_and_color()
    with tab4:
        render_media_and_feedback()

