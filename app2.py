import base64
import os
import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = "gpt-5.6-terra"
IMAGE_TYPES = ["jpg", "jpeg", "png", "gif", "webp"]
FILE_TYPES = ["txt", "md", "csv", "json", "py"]

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
    if "attached_image" not in st.session_state:
        st.session_state.attached_image = None
    if "attached_file" not in st.session_state:
        st.session_state.attached_file = None


def load_conversation(conversation_id, conversation_name):
    # 저장된 대화를 현재 세션으로 불러오기
    st.session_state.current_conversation_id = conversation_id
    st.session_state.conversation_name = conversation_name
    st.session_state.messages = [
        {"role": role, "content": content}
        for role, content, _, _, _ in get_conversation_messages(conversation_id)
    ]


def get_openai_client():
    api_key = st.session_state.get("api_key") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def get_available_models():
    # OpenAI 공식 모델 목록 기준 (developers.openai.com/api/docs/models/all)
    # 전부 비전(이미지 입력) 지원 모델
    return [
        ("gpt-6-astra", "GPT-6 Astra (최상위 성능)"),
        ("gpt-5.6-sol", "GPT-5.6 Sol (복잡한 전문 작업)"),
        ("gpt-5.6-terra", "GPT-5.6 Terra (성능/비용 균형)"),
        ("gpt-5.6-luna", "GPT-5.6 Luna (비용 최적화)"),
        ("gpt-5.5-pro", "GPT-5.5 Pro (정밀한 응답)"),
        ("gpt-5.5", "GPT-5.5 (코딩/전문 작업)"),
    ]


def build_attachment(uploaded_file):
    # 업로드된 파일을 세션에 보관 가능한 형태(bytes)로 변환
    return {
        "name": uploaded_file.name,
        "mime": uploaded_file.type,
        "data": uploaded_file.getvalue(),
    }


def process_image_attachment(attachment):
    # 이미지를 base64 data URL로 인코딩하여 Vision 입력으로 변환
    encoded = base64.standard_b64encode(attachment["data"]).decode("utf-8")
    return {
        "type": "image_url",
        "image_url": {"url": f"data:{attachment['mime']};base64,{encoded}"},
    }


def process_file_attachment(attachment):
    # 텍스트 파일 내용을 문자열로 디코딩
    return attachment["data"].decode("utf-8")


@st.dialog("🖼️ 이미지 첨부")
def image_upload_dialog():
    # 팝업 안에서 드래그&드롭으로 이미지를 첨부하는 다이얼로그
    st.caption("이미지를 이 영역에 드래그&드롭 하거나 클릭해서 선택하세요.")
    uploaded = st.file_uploader(
        "이미지 드래그&드롭",
        type=IMAGE_TYPES,
        key="image_dialog_uploader",
        label_visibility="collapsed",
    )

    if uploaded:
        st.image(uploaded, caption=uploaded.name, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 첨부하기", use_container_width=True, disabled=uploaded is None):
            st.session_state.attached_image = build_attachment(uploaded)
            st.rerun()
    with col2:
        if st.button("취소", use_container_width=True):
            st.rerun()


@st.dialog("📄 파일 첨부")
def file_upload_dialog():
    # 팝업 안에서 드래그&드롭으로 텍스트 파일을 첨부하는 다이얼로그
    st.caption("파일을 이 영역에 드래그&드롭 하거나 클릭해서 선택하세요.")
    uploaded = st.file_uploader(
        "파일 드래그&드롭",
        type=FILE_TYPES,
        key="file_dialog_uploader",
        label_visibility="collapsed",
    )

    if uploaded:
        st.success(f"📄 {uploaded.name} ({uploaded.size:,} bytes)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 첨부하기", use_container_width=True, disabled=uploaded is None):
            st.session_state.attached_file = build_attachment(uploaded)
            st.rerun()
    with col2:
        if st.button("취소", use_container_width=True):
            st.rerun()


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
        model=st.session_state.get("model", DEFAULT_MODEL),
        messages=messages,
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
        st.subheader("🤖 모델 선택")

        models = get_available_models()
        model_labels = [label for _, label in models]
        model_ids = [model_id for model_id, _ in models]

        current_model = st.session_state.get("model", DEFAULT_MODEL)
        selected_label = next(
            (label for model_id, label in models if model_id == current_model),
            model_labels[0],
        )

        selected_label = st.selectbox(
            "사용할 모델",
            model_labels,
            index=model_labels.index(selected_label),
            help="https://platform.openai.com/docs/models 참조",
        )

        st.session_state.model = model_ids[model_labels.index(selected_label)]
        st.caption(f"📌 현재 선택: `{st.session_state.model}`")

        st.divider()
        st.subheader("💾 대화 저장소")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ 새 대화", use_container_width=True):
                st.session_state.conversation_name = (
                    f"대화_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                st.session_state.current_conversation_id = create_conversation(
                    st.session_state.conversation_name
                )
                st.session_state.messages = []
                st.session_state.attached_image = None
                st.session_state.attached_file = None
                st.rerun()

        with col2:
            if st.button("🗑️ 현재 대화 삭제", use_container_width=True):
                if st.session_state.current_conversation_id:
                    delete_conversation(st.session_state.current_conversation_id)
                st.session_state.current_conversation_id = None
                st.session_state.messages = []
                st.rerun()

        st.divider()
        st.subheader("📂 이전 채팅 내역")

        conversations = get_conversations()
        if conversations:
            for conv_id, conv_name, updated_at in conversations:
                is_current = conv_id == st.session_state.current_conversation_id
                col1, col2 = st.columns([4, 1])
                with col1:
                    label = f"{'🟢' if is_current else '💬'} {conv_name}"
                    if st.button(
                        label,
                        use_container_width=True,
                        key=f"conv_{conv_id}",
                        help=f"마지막 수정: {updated_at}",
                    ):
                        load_conversation(conv_id, conv_name)
                        st.rerun()

                with col2:
                    if st.button("🗑️", key=f"del_{conv_id}", help="삭제"):
                        delete_conversation(conv_id)
                        if is_current:
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
        st.info(
            f"💾 현재 대화: **{st.session_state.conversation_name}** "
            f"(메시지 {len(st.session_state.messages)}개)"
        )
    else:
        st.warning("📝 메시지를 보내면 새 대화가 자동으로 시작됩니다")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("💬 채팅 히스토리")
        chat_container = st.container(height=400)

        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    with col2:
        st.subheader("📎 첨부")

        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("🖼️ 이미지 업로드", use_container_width=True):
                image_upload_dialog()
        with btn2:
            if st.button("📄 파일 업로드", use_container_width=True):
                file_upload_dialog()

        attached_image = st.session_state.attached_image
        attached_file = st.session_state.attached_file

        if attached_image:
            st.image(
                attached_image["data"],
                caption=f"🖼️ {attached_image['name']}",
                use_container_width=True,
            )
            if st.button("❌ 이미지 제거", use_container_width=True, key="remove_image"):
                st.session_state.attached_image = None
                st.rerun()

        if attached_file:
            st.success(f"📄 {attached_file['name']}")
            if st.button("❌ 파일 제거", use_container_width=True, key="remove_file"):
                st.session_state.attached_file = None
                st.rerun()

        if not attached_image and not attached_file:
            st.caption("첨부된 항목이 없습니다.")

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

        image_content = process_image_attachment(attached_image) if attached_image else None
        file_content = process_file_attachment(attached_file) if attached_file else None
        image_filename = attached_image["name"] if attached_image else None
        file_filename = attached_file["name"] if attached_file else None

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

                st.session_state.attached_image = None
                st.session_state.attached_file = None
                st.rerun()

            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main()
