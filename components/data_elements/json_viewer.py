import streamlit as st


def render_json_viewer():
    # st.json으로 구조화된 데이터를 확인하는 함수
    st.subheader("`st.json` - JSON 트리 뷰어")
    st.caption("딕셔너리/리스트 데이터를 접고 펼칠 수 있는 트리 형태로 보여줍니다.")

    sample_json = {
        "이름": "홍길동",
        "나이": 25,
        "취미": ["독서", "등산", "코딩"],
        "주소": {"도시": "서울", "구": "강남구"},
    }

    expanded = st.toggle("전체 펼치기 (expanded)", value=True)
    st.json(sample_json, expanded=expanded)
