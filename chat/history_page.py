import streamlit as st

from chat.config import MAX_SESSIONS, MAX_TURNS_PER_SESSION
from chat.database import (
    delete_conversation,
    get_conversation_messages,
    get_conversations,
)
from chat.login_page import render_account_section


def render_history_page():
    if "history_selected_id" not in st.session_state:
        st.session_state.history_selected_id = None

    conversations = get_conversations()

    st.title("📜 채팅 내역")
    st.caption(
        f"저장된 대화를 검색하고 다시 살펴볼 수 있습니다. "
        f"(세션당 최대 {MAX_TURNS_PER_SESSION}턴 · 최대 {MAX_SESSIONS}개 세션)"
    )

    with st.sidebar:
        render_account_section()
        st.divider()

        st.markdown("### 🔍 대화 검색")
        keyword = st.text_input("대화 이름", placeholder="예: 대화_2026")

        matched = [
            conversation for conversation in conversations
            if keyword.lower() in conversation[1].lower()
        ] if keyword else conversations

        st.divider()
        st.markdown(f"### 📂 목록 ({len(matched)}/{len(conversations)})")

        if not matched:
            st.info("검색 결과가 없습니다")

        for conversation_id, name, _created, updated, row_count in matched:
            is_selected = conversation_id == st.session_state.history_selected_id
            if st.button(
                f"{'🟢' if is_selected else '💬'} {name}",
                key=f"hist_{conversation_id}",
                use_container_width=True,
                help=f"{row_count // 2}턴 · 마지막 사용 {updated}",
            ):
                st.session_state.history_selected_id = conversation_id
                st.rerun()

    if not conversations:
        st.info("아직 저장된 대화가 없습니다. 채팅 페이지에서 대화를 시작해보세요.")
        return

    selected = next(
        (c for c in conversations if c[0] == st.session_state.history_selected_id),
        None,
    )

    if selected is None:
        st.info("← 사이드바에서 대화를 선택하면 내용을 볼 수 있습니다.")
        return

    conversation_id, name, created, updated, row_count = selected

    header, action = st.columns([4, 1])
    with header:
        st.subheader(name)
        st.caption(f"생성 {created} · 마지막 사용 {updated} · {row_count // 2}턴")
    with action:
        if st.button("🗑️ 삭제", use_container_width=True):
            delete_conversation(conversation_id)
            st.session_state.history_selected_id = None
            st.rerun()

    st.divider()

    for role, content, created_at in get_conversation_messages(conversation_id):
        with st.chat_message(role):
            st.markdown(content)
            st.caption(created_at)
