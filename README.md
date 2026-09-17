# streamlit-basic

Streamlit 학습용 프로젝트. 두 개의 독립 앱이 들어있다.

| 앱 | 실행 | 내용 |
|---|---|---|
| `app.py` | `streamlit run app.py` | Streamlit 위젯/레이아웃 기능 플레이그라운드 |
| `app2.py` | `streamlit run app2.py` | OpenAI API 기반 AI 채팅 (로그인 · 채팅 · 내역) |

---

## AI 채팅 앱 (`app2.py`)

### 구성

```
app2.py                 진입점: 로그인 게이트 + 페이지 내비게이션
chat/
  config.py             상수 · API 키 해석 · 키 문자열 마스킹
  database.py           SQLite 스키마 · CRUD · 보관 정책
  login_page.py         로그인(키 등록) · 보안 안내 · 계정 사이드바
  chat_page.py          채팅
  history_page.py       채팅 내역 열람
  styles.py             공통 CSS
```

### API 키 설정

키는 아래 순서로 찾는다. 앞쪽이 우선한다.

1. **로그인 화면에서 직접 등록한 키** — 서버에 키가 있어도 이걸로 덮어쓸 수 있다
2. **`st.secrets`** — 배포 환경용
3. **`.env`의 `OPENAI_API_KEY`** — 로컬 개발용

**로컬 실행**

```bash
cp .env.example .env     # 파일을 열어 OPENAI_API_KEY 입력
uv sync
streamlit run app2.py
```

**Streamlit Community Cloud 배포**

`.env`는 `.gitignore` 대상이라 배포본에 올라가지 않는다. 앱 설정의 **Secrets**에 아래를 입력한다.

```toml
OPENAI_API_KEY = "sk-proj-..."
```

로컬에서 배포 환경을 흉내 내려면 `.streamlit/secrets.toml`을 만든다 (이 파일도 gitignore 대상).

### 보관 정책

| 항목 | 한도 | 초과 시 |
|---|---|---|
| 세션당 대화 | **100턴** (내 메시지 + AI 답변 = 1턴) | 오래된 턴부터 삭제 |
| 저장 세션 수 | **10개** | 마지막 사용이 가장 오래된 세션부터 삭제 |

API로 보내는 대화 맥락은 최근 20턴으로 제한한다 (토큰·비용 방지).

### 보안 주의사항

- 이 앱은 **학습·데모용**이며 사용자 인증 체계가 없다. 배포 시 URL을 아는 누구나 접근할 수 있다.
- 로그인에 사용한 API 키는 **서버 세션 메모리에만** 보관하며 DB에 저장하지 않는다.
- **채팅 내용은 SQLite에 평문 저장**된다. 개인정보·비밀번호를 입력하지 말 것.
- 채팅창에 `sk-`로 시작하는 키를 붙여넣으면 저장 전에 자동으로 가려지지만, 애초에 입력하지 않는 것이 안전하다.
- `.env`, `chat_history.db`, `.streamlit/secrets.toml`은 모두 gitignore 대상이다.
