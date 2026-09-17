import numpy as np
import pandas as pd
import streamlit as st


def render_map_chart():
    # st.map으로 위경도 좌표 데이터를 지도에 표시하는 함수
    st.subheader("`st.map` - 지도 위 좌표 시각화")
    st.caption("서울 시청 근처에 무작위로 흩뿌린 좌표 50개를 표시합니다.")

    zoom = st.slider("지도 확대 정도 (zoom)", min_value=9, max_value=15, value=11)

    map_data = pd.DataFrame(
        {
            "lat": 37.5665 + np.random.randn(50) * 0.02,
            "lon": 126.9780 + np.random.randn(50) * 0.02,
        }
    )
    st.map(map_data, zoom=zoom, size=50, color="#FF4B4B")
