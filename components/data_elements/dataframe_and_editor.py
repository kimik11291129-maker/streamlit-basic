import pandas as pd
import streamlit as st


def render_dataframe_and_editor():
    # st.dataframe과 st.data_editor의 동작을 확인하는 함수
    st.subheader("1. `st.dataframe` - 읽기 전용 인터랙티브 표")
    st.caption("정렬, 검색, 컬럼 너비 조절이 가능한 대화형 표입니다.")

    df = pd.DataFrame(
        {
            "이름": ["김철수", "이영희", "박민수"],
            "점수": [85, 92, 78],
            "합격여부": [True, True, False],
        }
    )
    st.dataframe(
        df,
        column_config={
            "점수": st.column_config.ProgressColumn("점수", min_value=0, max_value=100),
            "합격여부": st.column_config.CheckboxColumn("합격여부"),
        },
        hide_index=True,
    )

    st.divider()

    st.subheader("2. `st.data_editor` - 편집 가능한 표")
    st.caption("셀을 직접 수정하거나 행을 추가/삭제할 수 있습니다 (num_rows='dynamic').")

    edited_df = st.data_editor(df, num_rows="dynamic", hide_index=True, key="data_editor")
    st.write("편집된 결과:", edited_df)
