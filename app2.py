import base64
import os
import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

load_dotenv()

DB_PATH = Path("chat_history.db")
st.set_page_config(page_title="AI 채팅 어시스턴트", page_icon="🤖", layout="wide")
st.title("🤖 AI 채팅 어시스턴트")
st.caption("OpenAI API를 이용한 고급 채팅 - 이미지, 파일 분석 및 대화 저장 가능")


def init_database():
    # SQLite 데이터베이스 초기화 및 테이블 생성
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        image_filename TEXT,
        file_filename TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(conversation_id) REFERENCES conversations(id)
    )
    """)

    conn.commit()
    conn.close()


def create_conversation(name):
    # 새로운 대화 세션 생성
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO conversations (name) VALUES (?)", (name,))
    conn.commit()
    conv_id = c.lastrowid
    conn.close()
    return conv_id


def get_conversations():
    # 모든 대화 목록 조회
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, updated_at FROM conversations ORDER BY updated_at DESC")
    conversations = c.fetchall()
    conn.close()
    return conversations


def get_conversation_messages(conversation_id):
    # 특정 대화의 모든 메시지 조회
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    SELECT role, content, image_filename, file_filename, created_at
    FROM messages WHERE conversation_id = ? ORDER BY created_at ASC
    """, (conversation_id,))
    messages = c.fetchall()
    conn.close()
    return messages


def save_message(conversation_id, role, content, image_filename=None, file_filename=None):
    # 메시지를 데이터베이스에 저장
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO messages (conversation_id, role, content, image_filename, file_filename)
    VALUES (?, ?, ?, ?, ?)
    """, (conversation_id, role, content, image_filename, file_filename))
    c.execute("UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()


def delete_conversation(conversation_id):
    # 대화 세션 삭제
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    c.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
    conn.commit()
    conn.close()


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = False
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None
    if "conversation_name" not in st.session_state:
        st.session_state.conversation_name = f"대화_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def get_openai_client():
    api_key = st.session_state.get("api_key") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def encode_image_to_base64(image_bytes):
    return base64.standard_b64encode(image_bytes).decode("utf-8")


def process_image_file(uploaded_file):
    # 이미지 파일을 base64로 인코딩하여 OpenAI Vision API용으로 변환
    image_data = encode_image_to_base64(uploaded_file.read())
    return {
        "type": "image_url",
        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
    }


def process_text_file(uploaded_file):
    # 텍스트 파일 내용을 읽어서 반환
    return uploaded_file.read().decode("utf-8")


def send_message_to_openai(client, user_message, image_content=None, file_content=None):
    # 메시지 히스토리와 현재 메시지를 OpenAI API에 전송
    messages = []

    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})

    current_content = []
    current_content.append({"type": "text", "text": user_message})

    if image_content:
        current_content.append(image_content)

    if file_content:
        current_content.append({
            "type": "text",
            "text": f"\n[첨부된 파일 내용]\n{file_content}"
        })

    messages.append({"role": "user", "content": current_content})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=2000,
    )

    return response.choices[0].message.content


def main():
    init_database()
    init_session_state()

    with st.sidebar:
        st.subheader("⚙️ API 설정")

        api_key_env = os.getenv("OPENAI_API_KEY")
        if api_key_env:
            st.session_state.api_key = api_key_env
            st.session_state.api_key_set = True
            st.success("✅ .env에서 API 키 로드됨")
        else:
            api_key_input = st.text_input(
                "OpenAI API 키",
                type="password",
                value=st.session_state.get("api_key", ""),
                help="https://platform.openai.com/api-keys에서 생성",
            )
            if api_key_input:
                st.session_state.api_key = api_key_input
                st.session_state.api_key_set = True
            else:
                st.warning("⚠️ OpenAI API 키를 입력해주세요")

        st.divider()
        st.subheader("💾 대화 저장소")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ 새 대화", use_container_width=True):
                conv_name = st.session_state.conversation_name
                conv_id = create_conversation(conv_name)
                st.session_state.current_conversation_id = conv_id
                st.session_state.messages = []
                st.rerun()

        with col2:
            if st.button("🗑️ 현재 대화 삭제", use_container_width=True):
                if st.session_state.current_conversation_id:
                    delete_conversation(st.session_state.current_conversation_id)
                st.session_state.current_conversation_id = None
                st.session_state.messages = []
                st.rerun()

        st.divider()
        st.subheader("📂 저장된 대화")

        conversations = get_conversations()
        if conversations:
            for conv_id, conv_name, updated_at in conversations:
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(f"💬 {conv_name}", use_container_width=True, key=f"conv_{conv_id}"):
                        st.session_state.current_conversation_id = conv_id
                        st.session_state.messages = []

                        for role, content, _, _, _ in get_conversation_messages(conv_id):
                            st.session_state.messages.append({
                                "role": role,
                                "content": content,
                            })

                        st.rerun()

                with col2:
                    if st.button("🗑️", key=f"del_{conv_id}", help="삭제"):
                        delete_conversation(conv_id)
                        if st.session_state.current_conversation_id == conv_id:
                            st.session_state.current_conversation_id = None
                            st.session_state.messages = []
                        st.rerun()
        else:
            st.info("저장된 대화가 없습니다")

        st.divider()
        st.markdown("### 📝 사용 가능 기능")
        st.markdown("""
        - 💬 일반 텍스트 채팅
        - 🖼️ 이미지 분석 (JPG, PNG, GIF, WebP)
        - 📄 텍스트 파일 처리 (TXT, MD, etc)
        - 💾 SQLite에 대화 자동 저장
        - 📂 이전 대화 불러오기
        """)

    if not st.session_state.api_key_set:
        st.error("❌ OpenAI API 키가 설정되지 않았습니다. 좌측 사이드바에서 입력해주세요.")
        return

    if st.session_state.current_conversation_id:
        st.info(f"💾 현재 대화: {st.session_state.conversation_name} (ID: {st.session_state.current_conversation_id})")
    else:
        st.warning("📝 새 대화를 시작하세요")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💬 채팅 히스토리")
        chat_container = st.container(height=400)

        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    with col2:
        st.subheader("📎 파일 첨부")

        uploaded_image = st.file_uploader(
            "이미지 선택",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            key="image_uploader",
        )

        uploaded_file = st.file_uploader(
            "텍스트 파일 선택",
            type=["txt", "md", "csv", "json"],
            key="file_uploader",
        )

        if uploaded_image:
            st.image(uploaded_image, caption="첨부된 이미지", use_container_width=True)

        if uploaded_file:
            st.info(f"📄 {uploaded_file.name} 첨부됨")

    st.divider()

    st.subheader("✍️ 메시지 입력")
    user_input = st.chat_input(
        "메시지를 입력하세요...",
        key="chat_input",
    )

    if user_input:
        if not st.session_state.current_conversation_id:
            st.session_state.current_conversation_id = create_conversation(
                st.session_state.conversation_name
            )

        client = get_openai_client()
        if not client:
            st.error("❌ OpenAI 클라이언트 초기화 실패")
            return

        image_content = None
        file_content = None
        image_filename = None
        file_filename = None

        if uploaded_image:
            uploaded_image.seek(0)
            image_content = process_image_file(uploaded_image)
            image_filename = uploaded_image.name

        if uploaded_file:
            uploaded_file.seek(0)
            file_content = process_text_file(uploaded_file)
            file_filename = uploaded_file.name

        with st.spinner("🔄 응답 생성 중..."):
            try:
                response = send_message_to_openai(
                    client, user_input, image_content, file_content
                )

                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input,
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                })

                save_message(
                    st.session_state.current_conversation_id,
                    "user",
                    user_input,
                    image_filename,
                    file_filename,
                )

                save_message(
                    st.session_state.current_conversation_id,
                    "assistant",
                    response,
                )

                st.rerun()

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
