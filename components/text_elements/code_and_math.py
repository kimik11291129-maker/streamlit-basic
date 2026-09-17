import streamlit as st


def render_code_and_math():
    # 코드 블록, 수식, 뱃지 등 표현용 텍스트 요소를 렌더링하는 함수
    st.subheader("1. `st.code` - 코드 블록")
    st.code(
        "def hello():\n    print('Hello, Streamlit!')",
        language="python",
        line_numbers=True,
    )

    st.divider()

    st.subheader("2. `st.latex` - 수식")
    st.latex(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}")

    st.divider()

    st.subheader("3. `st.badge` - 뱃지")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.badge("완료", icon="✅", color="green")
    with col2:
        st.badge("진행 중", icon="⏳", color="orange")
    with col3:
        st.badge("실패", icon="🚫", color="red")
