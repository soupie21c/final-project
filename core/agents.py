"""AI Agent 코어 모듈
- Evaluator Agent: 프롬프트 구성요소(역할, 맥락, 형식 등) 진단 및 점수 산출
- Prompt Tuning Agent: 거친 질문을 고품질 프롬프트로 개선 및 비포/애프터 생성
- Mentor Persona Agent: 선택된 멘토의 성격과 Long-term Memory를 반영한 코칭 생성
- Smart Mock Engine: API Key 미입력 시에도 완벽한 시뮬레이션 데모 제공
"""

import os
from openai import OpenAI
from core.mentors import get_mentor

def get_openai_client(api_key: str = None):
    key = api_key or os.getenv("OPENAI_API_KEY")
    if key and key.strip():
        return OpenAI(api_key=key.strip())
    return None

def tune_and_compare_prompt(raw_prompt: str, mentor_id: str, api_key: str = None, user_memory: dict = None) -> dict:
    """사용자의 원본 질문을 받아 원본 결과, 튜닝된 프롬프트, 튜닝 결과, 멘토 총평을 반환합니다."""
    client = get_openai_client(api_key)
    mentor = get_mentor(mentor_id)
    mentor_name = mentor["name"]
    mentor_title = mentor["title"]

    # 1. API 키가 있는 경우: 실시간 LLM 에이전트 체인 실행
    if client:
        try:
            # (1) 원본 프롬프트로 기본 답변 생성 (일반적인 평범한 답변)
            raw_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "너는 일반적인 AI 비서야. 사용자의 질문에 평범하고 일반적인 톤으로 답변해."},
                    {"role": "user", "content": raw_prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            raw_answer = raw_res.choices[0].message.content

            # (2) Prompt Tuning Agent: 고도화된 프롬프트 설계
            tuning_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": (
                        "너는 세계 최고의 프롬프트 엔지니어링 에이전트야. "
                        "사용자가 입력한 모호하고 거친 질문을 분석하여, "
                        "[1. 구체적인 전문가 역할(Role)] "
                        "[2. 배경 맥락(Context)] "
                        "[3. 구체적 제약 조건(Constraints)] "
                        "[4. 명확한 출력 형식(Format - 표, 불릿, 항목별)] "
                        "위 4요소가 완벽히 포함된 전문가급 프롬프트로 재작성해줘. "
                        "오직 재작성된 프롬프트 내용만 깔끔하게 출력해."
                    )},
                    {"role": "user", "content": f"사용자 원본 프롬프트: {raw_prompt}"}
                ],
                max_tokens=400,
                temperature=0.4
            )
            tuned_prompt = tuning_res.choices[0].message.content

            # (3) 튜닝된 프롬프트로 고품질 답변 생성
            tuned_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "너는 분야 최고의 전문가야. 주어진 정교한 프롬프트 지시사항을 100% 준수하여 완벽한 서식과 표, 불릿으로 답변을 제공해."},
                    {"role": "user", "content": tuned_prompt}
                ],
                max_tokens=800,
                temperature=0.5
            )
            tuned_answer = tuned_res.choices[0].message.content

            # (4) Mentor Persona Agent: 멘토 스타일 맞춤 총평 (메모리 반영)
            mem_note = ""
            if user_memory and user_memory.get("weakness_history"):
                mem_note = f"참고: 이 훈련생의 취약점 기록은 다음과 같다: {user_memory['weakness_history']}. 필요하면 츤데레/칭찬/교관 톤으로 살짝 언급해라."

            mentor_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"{mentor['system_prompt']}\n{mem_note}"},
                    {"role": "user", "content": (
                        f"훈련생의 원본 질문: '{raw_prompt}'\n"
                        f"개선된 프롬프트: '{tuned_prompt}'\n"
                        f"이 두 가지를 비교했을 때 어떤 점(역할, 형식, 조건 등)이 좋아졌는지 "
                        f"당신의 고유한 캐릭터 말투로 2~3줄 이내의 날카롭고 임팩트 있는 총평 코칭을 해줘."
                    )}
                ],
                max_tokens=300,
                temperature=0.7
            )
            mentor_feedback = mentor_res.choices[0].message.content

            return {
                "raw_prompt": raw_prompt,
                "raw_answer": raw_answer,
                "tuned_prompt": tuned_prompt,
                "tuned_answer": tuned_answer,
                "mentor_feedback": mentor_feedback,
                "mode": "live"
            }

        except Exception as e:
            # API 호출 중 오류 발생 시에도 사용자 경험을 위해 스마트 시뮬레이션으로 폴백
            print(f"API Error: {e}, falling back to mock")

    # 2. API 키가 없거나 호출 실패 시: 스마트 시뮬레이션 모드 (프리셋 & 규칙 기반 엔진)
    return generate_mock_comparison(raw_prompt, mentor)

def generate_mock_comparison(raw_prompt: str, mentor: dict) -> dict:
    """스마트 시뮬레이션: API 키 없이도 즉시 직관적인 비포/애프터를 체감할 수 있는 엔진"""
    mentor_id = mentor["id"]
    
    # 튜닝 프롬프트 템플릿화
    tuned_prompt = (
        f"[역할 부여] 너는 해당 분야 10년 차 수석 컨설턴트야.\n"
        f"[맥락 및 대상] 왕초보도 이해하기 쉽게 핵심 위주로 설명해줘.\n"
        f"[핵심 요청] '{raw_prompt}'에 대해 체계적으로 분석해줘.\n"
        f"[제약 및 출력 형식] \n"
        f"1. 서론-본론-결론 3단계 구성\n"
        f"2. 핵심 실행 단계는 마크다운 표(Table)로 [단계 | 주요내용 | 팁] 정리\n"
        f"3. 주의사항 3가지를 체크리스트 형태로 제공"
    )

    raw_answer = (
        f"'{raw_prompt}'에 대한 일반적인 답변입니다.\n\n"
        "관련해서 여러 가지 방법이 있을 수 있습니다. 우선 기본적인 개념을 이해하는 것이 중요하며, "
        "인터넷 자료나 관련 서적을 찾아보시면 도움이 됩니다. 꾸준히 계획을 세워 실천하시고, "
        "필요한 경우 전문가의 조언을 구하는 것도 좋은 방법입니다. 더 궁금한 점이 있으면 물어보세요."
    )

    tuned_answer = (
        f"### 🎯 전문가 맞춤 솔루션: '{raw_prompt}'\n\n"
        "**1. 핵심 요약**\n"
        "효율적인 목표 달성을 위해 체계적인 3단계 프로세스를 제안합니다.\n\n"
        "**2. 단계별 실행 가이드 (마크다운 표)**\n\n"
        "| 단계 | 핵심 액션 | 예상 소요시간 | 실전 꿀팁 |\n"
        "| :--- | :--- | :---: | :--- |\n"
        "| **Step 1** | 현재 상태 진단 및 명확한 목표 설정 | 1일 | 세부 수치 목표 작성 |\n"
        "| **Step 2** | 우선순위 Top 3 선별 및 집중 실행 | 1~2주 | 뽀모도로 기법 활용 |\n"
        "| **Step 3** | 결과 피드백 및 루틴 최적화 | 주 1회 | 주간 회고 작성 |\n\n"
        "**3. 주의해야 할 체크리스트 (Fail-Safe)**\n"
        "- [ ] 처음부터 무리한 계획을 세우지 않았는가?\n"
        "- [ ] 검증되지 않은 정보에 의존하지 않는가?\n"
        "- [ ] 일일 진행 상황을 기록하고 있는가?"
    )

    if mentor_id == "dohyuk":
        mentor_feedback = (
            f"흥, 봐라. 네가 처음 던진 '{raw_prompt}'는 AI한테 그냥 아무 소리나 지껄이라는 거랑 똑같았어. "
            "내가 [10년 차 전문가 역할]을 심고, [표 형식]으로 강제하니까 답변 수준이 3배는 올라갔잖아? "
            "앞으로 질문할 땐 원하는 결과물 틀(Format)을 꼭 먼저 정해둬."
        )
    elif mentor_id == "harin":
        mentor_feedback = (
            f"우와아! 훈련생님! 원래 쓰셨던 '{raw_prompt}'도 참 좋은 질문이었지만, "
            "이렇게 [역할]과 [표 정리] 조건을 마법처럼 쏙 더하니까 진짜 전문가 보고서처럼 바뀌었죠?! "
            "이 감각을 기억하시면 다음엔 혼자서도 100점짜리 질문을 척척 만드실 수 있어요! 힘내요! 💖"
        )
    else:  # taesan
        mentor_feedback = (
            f"훈련생, 주목! '{raw_prompt}'라는 밋밋한 지시에서 벗어나 [역할-맥락-제약-출력형식]의 "
            "4단 편제를 갖추니 결과물이 완벽히 정렬되었다! 실전에서는 이런 명확한 명령만이 "
            "시간을 아끼고 승리를 가져오는 법이다! 이 튜닝 공식을 머리에 새겨라! 악!"
        )

    return {
        "raw_prompt": raw_prompt,
        "raw_answer": raw_answer,
        "tuned_prompt": tuned_prompt,
        "tuned_answer": tuned_answer,
        "mentor_feedback": mentor_feedback,
        "mode": "mock"
    }
