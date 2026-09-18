# 프로젝트 규칙: Streamlit 기능 탐색 및 실습용 플레이그라운드 (Playground / Testbed)

이 프로젝트(`streamlit-basic`)는 Streamlit의 다양한 기능, 위젯, 옵션들을 **직접 이것저것 테스트하고 눈으로 확인해보기 위한 실습/실험용 공간**입니다.

---

## 📌 핵심 원칙

1. **학습 및 실험 중심 (Playground / Sandbox)**
   - 다양한 옵션과 파라미터(예: 타입별 동작, 옵션 변경에 따른 변화, 입력 위젯별 차이 등)를 직접 조작하고 그 결과를 화면에서 바로 체감할 수 있도록 구성합니다.

2. **예외 처리 및 방어 코드 지양 (No Defensive Code)**
   - `try-except` 블록, 과도한 유효성 검사(Validation), 방어적 예외 처리, 중첩된 Null/None 체크 등 코드를 길고 복잡하게 만드는 코드는 작성하지 않습니다.
   - 불필요한 사전 검증 없이 각 기능의 순수한 동작 방식을 한눈에 파악할 수 있게 합니다.

3. **간결하고 직관적인 구현 (KISS - Keep It Simple, Stupid)**
   - 복잡한 클래스 구조나 래퍼 함수 대신 한눈에 알아볼 수 있는 직관적인 스크립트 스타일을 우선합니다.
   - 코드를 처음 보는 사람도 어떤 옵션이 어떤 결과를 만드는지 최소한의 코드로 즉시 알 수 있게 합니다.

4. **공식 Streamlit API 레퍼런스 준수 (필수)**
   - 사용자가 기능이나 예시 코드 작성을 요청할 경우, 공식 Streamlit API 레퍼런스 문서를 적극 참고하여 표준적이고 최신의 코드를 작성합니다.
   - **기본 참고 문서 주소**: https://docs.streamlit.io/develop/api-reference
   - 해당 주소 및 하위 카테고리(Text elements, Data elements, Input widgets, Layouts, Chat elements 등) 페이지들의 공식 가이드와 예제를 기준으로 코드를 작성합니다.

5. **OpenAI 추론 모델(Reasoning) 및 Responses API 가이드 준수 (필수)**
   - OpenAI 추론 모델(Reasoning models) 및 최신 Responses API를 다룰 경우, 공식 가이드 문서를 참고하여 표준적이고 최신의 코드를 작성합니다.
   - **기본 참고 문서 주소**: https://developers.openai.com/api/docs/guides/reasoning?api-mode=responses
   - **주요 가이드**:
     - Responses API(`client.responses.create`) 기반으로 작성하며, 추론 강도는 `reasoning={"effort": "low"}` (또는 `medium`, `high`, `xhigh` 등) 형태로 지정합니다.
     - 토큰 제한이 필요한 경우 Responses API 표준인 `max_output_tokens`를 활용합니다.
     - 추론 토큰은 응답의 `output_tokens_details.reasoning_tokens`에서 확인 가능하며 충분한 토큰 버퍼를 고려합니다.
