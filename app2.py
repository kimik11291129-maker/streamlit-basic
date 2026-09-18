from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Streamlit 멀티페이지 포털", page_icon="🚀", layout="wide")

pages_dir = Path(__file__).parent / "stream_pages"

# ------------------------------------------------------------------------------
# 로그인 여부(st.user.is_logged_in)에 따른 동적 네비게이션 제어
# ------------------------------------------------------------------------------
if not st.user.is_logged_in:
    # 🔒 미로그인 상태: 로그인/안내 페이지만 노출 (다른 모든 페이지 접근 차단)
    pages = [
        st.Page(pages_dir / "main.py", title="로그인", icon="🔐"),
    ]
else:
    # 🔓 로그인 상태: 전체 메뉴 및 서브페이지 노출
    pages = {
        "🏠 메인 & 대시보드": [
            st.Page(pages_dir / "main.py", title="홈 포털", icon="🏠", default=True),
            st.Page(pages_dir / "dashboard.py", title="데이터 분석 대시보드", icon="📊"),
        ],
        "⚙️ 계정 & 설정": [
            st.Page(pages_dir / "profile.py", title="사용자 프로필", icon="👤"),
            st.Page(pages_dir / "settings.py", title="환경 설정", icon="⚙️"),
        ],
        "🧭 API 실습": [
            st.Page(pages_dir / "navigation_page.py", title="내비게이션 기능 실습", icon="🧭"),
        ],
        "🚪 로그아웃": [
            st.Page(st.logout, title="로그아웃", icon="🚪"),
        ],
    }

pg = st.navigation(pages)
pg.run()