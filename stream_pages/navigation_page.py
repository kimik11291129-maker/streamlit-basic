from pathlib import Path
import streamlit as st

pages_dir = Path(__file__).parent


def render_navigation_page():
    """Streamlit 공식 Navigation API(st.navigation, st.Page, st.page_link, st.switch_page) 실습 화면을 렌더링합니다."""
    # 미로그인 상태 접근 차단
    if not st.user.is_logged_in:
        st.warning("⚠️ 로그인이 필요한 페이지입니다.")
        st.page_link(pages_dir / "main.py", label="로그인 페이지로 이동", icon="🔐")
        st.stop()

    st.title("🧭 Navigation and pages 실습")
    st.caption("공식 Streamlit API Reference: https://docs.streamlit.io/develop/api-reference/navigation")

    st.info("이 페이지에서는 Streamlit 공식 내비게이션 API인 `st.navigation`, `st.Page`, `st.page_link`, `st.switch_page`를 직접 조작하고 테스트할 수 있습니다.")

    # ==============================================================================
    # 1. st.page_link (페이지 링크)
    # ==============================================================================
    st.header("1. `st.page_link`")
    st.write("다른 페이지나 외부 웹사이트로 이동할 수 있는 링크 요소를 렌더링합니다.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("내부 페이지 링크")
        # 내부 메인 페이지로 이동
        st.page_link(pages_dir / "main.py", label="메인 페이지로 이동", icon="🏠")
        
        # 쿼리 파라미터 포함하여 이동
        st.page_link(
            pages_dir / "main.py",
            label="쿼리 파라미터와 함께 메인으로 이동",
            icon="🔗",
            query_params={"from": "navigation_page", "status": "demo"},
        )
        
        # 비활성화(disabled)된 링크
        st.page_link(pages_dir / "main.py", label="비활성화된 링크 (disabled=True)", icon="🚫", disabled=True)

    with col2:
        st.subheader("외부 링크 (External URL)")
        # 외부 웹사이트 링크 (새 탭에서 열림)
        st.page_link(
            "https://docs.streamlit.io/develop/api-reference/navigation",
            label="Streamlit 공식 Navigation 문서",
            icon="🌐",
        )
        st.page_link(
            "https://docs.streamlit.io",
            label="Streamlit Docs 홈",
            icon="📖",
        )

    st.divider()

    # ==============================================================================
    # 2. st.switch_page (프로그래밍 방식 페이지 전환)
    # ==============================================================================
    st.header("2. `st.switch_page`")
    st.write("버튼 클릭 등의 이벤트 발생 시 파이썬 코드로 특정 페이지로 즉시 화면을 전환합니다.")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🚀 메인 페이지로 즉시 전환", type="primary"):
            st.switch_page(pages_dir / "main.py")

    with col_btn2:
        if st.button("🎯 쿼리 파라미터와 함께 전환"):
            st.switch_page(pages_dir / "main.py", query_params={"switched": "true", "type": "button"})

    st.divider()

    # ==============================================================================
    # 3. st.Page & st.navigation (멀티페이지 구조 및 메뉴 설정)
    # ==============================================================================
    st.header("3. `st.Page` & `st.navigation`")
    st.write("Streamlit의 멀티페이지 아키텍처를 구성하는 핵심 함수입니다.")

    tab1, tab2, tab3 = st.tabs(["📄 st.Page 속성", "📑 st.navigation 그룹화", "📍 메뉴 위치 (position)"])

    with tab1:
        st.markdown("""
        #### `st.Page` 주요 매개변수
        - **`page`**: 파이썬 파일 경로(`"path/to/file.py"` 또는 `Path` 객체) 또는 실행 함수(`callable`)
        - **`title`**: 메뉴에 표시될 페이지 제목
        - **`icon`**: 이모지(예: `"🏠"`) 또는 머티리얼 아이콘(예: `":material/home:"`)
        - **`url_path`**: 브라우저 URL에 표시될 경로 이름
        - **`default`**: `True` 설정 시 앱 첫 진입 시 기본으로 열리는 페이지
        """)
        st.code('''# st.Page 선언 예시
home_page = st.Page("main.py", title="홈", icon="🏠", default=True)
nav_page = st.Page("navigation_page.py", title="내비게이션", icon="🧭")''', language="python")

    with tab2:
        st.markdown("""
        #### `st.navigation` 동적 권한 제어 (현재 앱에 적용된 방식)
        로그인 여부(`st.user.is_logged_in`)에 따라 노출할 페이지 목록을 동적으로 구성하여 접근을 차단합니다.
        """)
        st.code('''if not st.user.is_logged_in:
    # 미로그인 시 로그인 페이지만 노출
    pages = [st.Page("main.py", title="로그인", icon="🔐")]
else:
    # 로그인 시 전체 페이지 노출
    pages = {
        "메인": [st.Page("main.py", title="홈")],
        "대시보드": [st.Page("dashboard.py", title="분석")],
    }
pg = st.navigation(pages)
pg.run()''', language="python")

    with tab3:
        st.markdown("""
        #### `position` 옵션 비교
        - **`position="sidebar"` (기본값)**: 사이드바 상단에 메뉴 표시
        - **`position="top"`**: 앱 상단 헤더 영역에 메뉴 표시 (모바일 화면이나 가로형 내비게이션에 적합)
        - **`position="hidden"`**: 기본 메뉴를 완전히 숨기고, 개발자가 직접 `st.page_link`로 커스텀 메뉴를 만들 때 사용
        """)
        st.code('''# 상단 메뉴 예시
pg = st.navigation(pages, position="top")
pg.run()

# 메뉴 숨김 (커스텀 내비게이션 구현 시)
pg = st.navigation(pages, position="hidden")
pg.run()''', language="python")


render_navigation_page()
