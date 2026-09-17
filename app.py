import streamlit as st
from pages.input_widgets import render_input_widgets_page
from pages.layouts import render_layouts_page
from pages.text_elements import render_text_elements_page
from pages.data_elements import render_data_elements_page
from pages.charts import render_charts_page
from pages.media_elements import render_media_elements_page
from pages.status_elements import render_status_elements_page
from pages.chat_elements import render_chat_elements_page


# Streamlit 공식 st.navigation으로 네이티브 사이드바 목차 구성
pages = {
    "🎨 인터랙션 & 레이아웃": [
        st.Page(render_input_widgets_page, title="인풋 위젯", icon="🎛️", default=True),
        st.Page(render_layouts_page, title="레이아웃 & 컨테이너", icon="📐"),
    ],
    "📋 콘텐츠 표시": [
        st.Page(render_text_elements_page, title="텍스트 요소", icon="📝"),
        st.Page(render_data_elements_page, title="데이터 요소", icon="📊"),
        st.Page(render_charts_page, title="차트 요소", icon="📈"),
    ],
    "🎬 미디어 & 상태": [
        st.Page(render_media_elements_page, title="미디어 요소", icon="🖼️"),
        st.Page(render_status_elements_page, title="상태 & 알림", icon="🚦"),
    ],
    "💬 인터랙션": [
        st.Page(render_chat_elements_page, title="채팅 요소", icon="💬"),
    ],
}

pg = st.navigation(pages)
pg.run()