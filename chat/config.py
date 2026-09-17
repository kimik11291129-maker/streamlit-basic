import re

import streamlit as st

# 채팅 내용은 DB에 평문 저장되므로, 키를 실수로 붙여넣어도 원문이 남지 않게 가린다.
_SECRET_PATTERN = re.compile(r"sk-[A-Za-z0-9_\-]{16,}")

DEFAULT_MODEL = "gpt-5.6-terra"

# 보관 정책 (1턴 = 내 메시지 1 + AI 답변 1)
MAX_TURNS_PER_SESSION = 100
MAX_SESSIONS = 10

# API로 전송할 최근 대화 턴 수. 100턴을 모두 보내면 요청마다 토큰/비용이 급증한다.
API_HISTORY_TURNS = 20


def get_available_models():
    # OpenAI 공식 모델 목록 기준 (developers.openai.com/api/docs/models/all)
    return [
        ("gpt-6-astra", "GPT-6 Astra (최상위 성능)"),
        ("gpt-5.6-sol", "GPT-5.6 Sol (복잡한 전문 작업)"),
        ("gpt-5.6-terra", "GPT-5.6 Terra (성능/비용 균형)"),
        ("gpt-5.6-luna", "GPT-5.6 Luna (비용 최적화)"),
        ("gpt-5.5-pro", "GPT-5.5 Pro (정밀한 응답)"),
        ("gpt-5.5", "GPT-5.5 (코딩/전문 작업)"),
    ]


def resolve_api_key():
    # 서버가 미리 등록해둔 키(.env/st.secrets)는 절대 쓰지 않는다.
    # 공개 배포 시 인증 없이 누구나 그 키를 눌러 쓸 수 있게 되는 경로라
    # 방문자가 직접 등록한 키만 사용하도록 의도적으로 제한한다.
    return st.session_state.get("user_api_key")


def mask_key(key):
    return f"{key[:7]}{'•' * 8}{key[-4:]}" if len(key) > 12 else "•" * len(key)


def redact_secrets(text):
    return _SECRET_PATTERN.sub("[API 키 삭제됨]", text)
