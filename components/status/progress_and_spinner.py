import time

import streamlit as st


def render_progress_and_spinner():
    # st.progress, st.spinner, st.status의 동작을 확인하는 함수
    st.subheader("1. `st.progress` - 진행률 바")
    if st.button("진행률 시작하기", key="progress_btn"):
        bar = st.progress(0, text="진행 중...")
        for pct in range(0, 101, 20):
            time.sleep(0.2)
            bar.progress(pct, text=f"진행 중... {pct}%")

    st.divider()

    st.subheader("2. `st.spinner` - 로딩 스피너")
    if st.button("스피너 실행하기", key="spinner_btn"):
        with st.spinner("처리 중입니다..."):
            time.sleep(1.5)
        st.write("처리 완료!")

    st.divider()

    st.subheader("3. `st.status` - 상태 컨테이너 (단계별 로그)")
    if st.button("작업 실행하기", key="status_btn"):
        with st.status("데이터 처리 중...", expanded=True) as status:
            st.write("1단계: 데이터 불러오는 중")
            time.sleep(0.5)
            st.write("2단계: 데이터 가공 중")
            time.sleep(0.5)
            status.update(label="처리 완료!", state="complete", expanded=False)
