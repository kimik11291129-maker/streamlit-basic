from datetime import datetime

import streamlit as st
from openai import OpenAI

from chat.config import (
    API_HISTORY_TURNS,
    DEFAULT_MODEL,
    MAX_SESSIONS,
    MAX_TURNS_PER_SESSION,
    get_available_models,
    redact_secrets,
    resolve_api_key,
)
from chat.database import (
    create_conversation,
    delete_conversation,
    get_conversation_messages,
    get_conversations,
    save_turn,
)
from chat.login_page import render_account_section

EXAMPLE_PROMPTS = [
    "파이썬 리스트 컴프리헨션 설명해줘",
    "오늘 할 일 체크리스트 만들어줘",
    "Streamlit을 3줄로 요약해줘",
]


def _new_conversation_name():
    return f"대화_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None
    if "conversation_name" not in st.session_state:
        st.session_state.conversation_name = _new_conversation_name()
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


def start_new_conversation():
    # DB 행은 첫 메시지를 보낼 때 만든다. 빈 세션이 저장 한도를 차지하지 않도록.
    st.session_state.conversation_name = _new_conversation_name()
    st.session_state.current_conversation_id = None
    st.session_state.messages = []


def load_conversation(conversation_id, name):
    st.session_state.current_conversation_id = conversation_id
    st.session_state.conversation_name = name
    st.session_state.messages = [
        {"role": role, "content": content}
        for role, content, _ in get_conversation_messages(conversation_id)
    ]


def render_sidebar():
    with st.sidebar:
        render_account_section()
        st.divider()

        conversations = get_conversations()
        st.markdown(f"### 💬 대화 ({len(conversations)}/{MAX_SESSIONS})")

        if st.button("➕ 새 대화", type="primary", use_container_width=True):
            start_new_conversation()
            st.rerun()

        for conversation_id, name, _created, updated, row_count in conversations:
            is_current = conversation_id == st.session_state.current_conversation_id
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    f"{'🟢' if is_current else '💬'} {name}",
                    key=f"sb_conv_{conversation_id}",
                    use_container_width=True,
                    help=f"{row_count // 2}턴 · 마지막 사용 {updated}",
                ):
                    load_conversation(conversation_id, name)
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"sb_del_{conversation_id}", help="삭제"):
                    delete_conversation(conversation_id)
                    if is_current:
                        start_new_conversation()
                    st.rerun()

        st.caption(
            f"세션당 {MAX_TURNS_PER_SESSION}턴 · 최대 {MAX_SESSIONS}개 세션까지 저장되며 "
            "한도를 넘으면 오래된 것부터 삭제됩니다."
        )

        st.divider()
        st.markdown("### ⚙️ 설정")

        models = get_available_models()
        labels = [label for _, label in models]
        model_ids = [model_id for model_id, _ in models]
        current_model = st.session_state.get("model", DEFAULT_MODEL)
        index = model_ids.index(current_model) if current_model in model_ids else 0

        selected = st.selectbox("모델", labels, index=index)
        st.session_state.model = model_ids[labels.index(selected)]


def render_empty_state():
    st.markdown(
        "<div class='empty-card'>"
        "<div class='empty-title'>새 대화를 시작해보세요</div>"
        "<div class='empty-sub'>아래 예시를 누르거나 직접 질문을 입력하세요.</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    for col, example in zip(st.columns(len(EXAMPLE_PROMPTS)), EXAMPLE_PROMPTS):
        with col:
            if st.button(example, key=f"ex_{example}", use_container_width=True):
                st.session_state.pending_prompt = example
                st.rerun()


def request_completion(client, prompt):
    # 최근 API_HISTORY_TURNS 턴만 전송해 토큰/비용 급증을 막는다.
    history = st.session_state.messages[-API_HISTORY_TURNS * 2:]
    messages = [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=st.session_state.get("model", DEFAULT_MODEL),
        messages=messages,
    )
    return response.choices[0].message.content


def handle_prompt(raw_prompt):
    # 화면·DB·API 어디로도 키 원문이 흘러가지 않도록 입구에서 한 번 가린다.
    prompt = redact_secrets(raw_prompt)
    if prompt != raw_prompt:
        st.toast("API 키로 보이는 문자열을 가렸습니다. 키는 채팅창에 입력하지 마세요.", icon="🔒")

    api_key, _ = resolve_api_key()
    client = OpenAI(api_key=api_key)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("응답 생성 중..."):
            try:
                answer = redact_secrets(request_completion(client, prompt))
            except Exception as error:
                st.error(f"요청에 실패했습니다: {error}")
                return
        st.markdown(answer)

    if st.session_state.current_conversation_id is None:
        st.session_state.current_conversation_id = create_conversation(
            st.session_state.conversation_name
        )

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": answer})
    # 화면(세션)도 DB와 같은 한도로 잘라 둘이 어긋나지 않게 한다.
    del st.session_state.messages[: -MAX_TURNS_PER_SESSION * 2]

    save_turn(st.session_state.current_conversation_id, prompt, answer)
    st.rerun()


def render_chat_page():
    init_session_state()
    render_sidebar()

    turns = len(st.session_state.messages) // 2

    st.title("💬 AI 채팅")
    left, right = st.columns([3, 1])
    with left:
        st.caption(f"현재 대화: **{st.session_state.conversation_name}**")
    with right:
        st.caption(f"{turns} / {MAX_TURNS_PER_SESSION}턴")
    st.progress(min(turns / MAX_TURNS_PER_SESSION, 1.0))

    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        render_empty_state()

    prompt = st.chat_input("메시지를 입력하세요...")

    if st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if prompt:
        handle_prompt(prompt)
