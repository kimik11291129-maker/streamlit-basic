import sqlite3
from pathlib import Path

import streamlit as st

DB_PATH = Path("chat_history.db")


def get_conversations():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    SELECT c.id, c.name, c.created_at, c.updated_at, COUNT(m.id)
    FROM conversations c
    LEFT JOIN messages m ON m.conversation_id = c.id
    GROUP BY c.id
    ORDER BY c.updated_at DESC
    """)
    conversations = c.fetchall()
    conn.close()
    return conversations


def get_conversation_messages(conversation_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    SELECT role, content, image_filename, file_filename, created_at
    FROM messages WHERE conversation_id = ? ORDER BY created_at ASC
    """, (conversation_id,))
    messages = c.fetchall()
    conn.close()
    return messages


def delete_conversation(conversation_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    c.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()


def init_session_state():
    if "history_selected_id" not in st.session_state:
        st.session_state.history_selected_id = None


def render_history_page():
    st.title("📜 채팅 히스토리")
    st.caption("채팅 페이지에서 나눈 대화들을 검색하고 다시 살펴볼 수 있습니다.")

    init_session_state()

    if not DB_PATH.exists():
        st.info("아직 저장된 대화가 없습니다. 채팅 페이지에서 대화를 시작해보세요.")
        return

    conversations = get_conversations()

    with st.sidebar:
        st.subheader("🔍 대화 검색")
        keyword = st.text_input("대화 이름으로 검색", placeholder="예: 대화_2025")

        filtered = [
            conv for conv in conversations
            if keyword.lower() in conv[1].lower()
        ] if keyword else conversations

        st.divider()
        st.subheader(f"📂 전체 대화 ({len(filtered)}개)")

        if not filtered:
            st.info("검색 결과가 없습니다")

        for conv_id, name, created_at, updated_at, msg_count in filtered:
            is_selected = conv_id == st.session_state.history_selected_id
            label = f"{'🟢' if is_selected else '💬'} {name}"
            if st.button(
                label,
                use_container_width=True,
                key=f"hist_{conv_id}",
                help=f"메시지 {msg_count}개 · 마지막 수정: {updated_at}",
            ):
                st.session_state.history_selected_id = conv_id
                st.rerun()

    selected_id = st.session_state.history_selected_id

    if selected_id is None:
        st.info("← 좌측에서 대화를 선택하면 내용을 볼 수 있습니다.")
        return

    selected = next((c for c in conversations if c[0] == selected_id), None)
    if selected is None:
        st.session_state.history_selected_id = None
        st.rerun()
        return

    _, name, created_at, updated_at, msg_count = selected

    col1, col2 = st.columns([5, 1])
    with col1:
        st.subheader(f"💬 {name}")
        st.caption(f"생성: {created_at} · 마지막 수정: {updated_at} · 메시지 {msg_count}개")
    with col2:
        if st.button("🗑️ 대화 삭제", use_container_width=True):
            delete_conversation(selected_id)
            st.session_state.history_selected_id = None
            st.rerun()

    st.divider()

    for role, content, image_filename, file_filename, created_at in get_conversation_messages(selected_id):
        with st.chat_message(role):
            st.markdown(content)
            if image_filename:
                st.caption(f"🖼️ 첨부 이미지: {image_filename}")
            if file_filename:
                st.caption(f"📄 첨부 파일: {file_filename}")
            st.caption(created_at)


if __name__ == "__main__":
    st.set_page_config(page_title="채팅 히스토리", page_icon="📜", layout="wide")
    render_history_page()
