"""퀘스트 데이터셋 모듈
1단계 부트캠프 & 2단계 사관학교 모두 100% 도파민 폭발 A/B 전술 선택 및 배틀 형태로 전면 개편
"""

QUESTS = [
    # ── [1단계: Prompt Camp - 야간 전술 훈련장 (A/B 선택)] ──
    {
        "id": "camp_01",
        "track": "camp",
        "stage_num": "STAGE 01",
        "title": "AI에게 정체성(Role) 부여 작전",
        "badge_tag": "ROLE HACKER",
        "target": "취업 면접관 AI 소환",
        "boss_statement": "“면접 준비를 도와줄 든든한 전문가 AI를 소환해야 한다!”",
        "choice_a": {
            "name": "🅰️ 평범한 훈련생",
            "prompt": "“취업 면접 예상 질문 3개만 아무거나 뽑아줘.”",
            "effect": "💢 AI가 교과서적인 뻔한 인터넷 질문만 복붙해 옴 (효과 없음)"
        },
        "choice_b": {
            "name": "🅱️ 전술적 프로 훈련생",
            "prompt": "“너는 10년 차 IT 대기업 채용담당관이야. 주니어 개발자 관점에서 질문 3개를 해줘.”",
            "effect": "⚡ 실무 면접관 두뇌 풀가동! 날카로운 압박 질문 발동! (+100 크리티컬)"
        },
        "correct_choice": "B",
        "praise_title": "🎯 타깃 소환 대성공!",
        "explanation": "구체적인 직책과 연차를 주면 AI의 전문 지식 신경망이 즉시 활성화됩니다!",
        "badge": "🏅 역할 마스터 (Role Hacker)",
        "miss_tag": "역할(Role) 부재"
    },
    {
        "id": "camp_02",
        "track": "camp",
        "stage_num": "STAGE 02",
        "title": "가독성 폭발 표(Table) 서식 강제",
        "badge_tag": "FORMAT ARCHITECT",
        "target": "제주도 2박 3일 황금 일정표",
        "boss_statement": "“줄글로 길게 늘어지는 설명은 읽기 피곤하다! 한눈에 꽂히는 표로 받아내라!”",
        "choice_a": {
            "name": "🅰️ 줄글 나열 요청",
            "prompt": "“제주도 2박 3일 여행 일정 재밌고 길게 써줘.”",
            "effect": "😵 읽다가 지치는 100줄짜리 텍스트 폭탄 투하"
        },
        "choice_b": {
            "name": "🅱️ 마크다운 표 강제",
            "prompt": "“제주 2박 3일 일정을 [시간 / 장소 / 비용 / 꿀팁] 표(Table)로 정리해줘.”",
            "effect": "✨ 깔끔하고 완벽한 시간표 즉시 생성! 여행 준비 1분 컷!"
        },
        "correct_choice": "B",
        "praise_title": "📊 서식 타격 성공!",
        "explanation": "표(Table)와 컬럼명을 강제하면 AI가 군더더기 없이 일목요연한 보고서 형태로 답변합니다.",
        "badge": "🥈 표형식 전문가 (Format Architect)",
        "miss_tag": "출력 형식(Format) 누락"
    },
    {
        "id": "camp_03",
        "track": "camp",
        "stage_num": "STAGE 03",
        "title": "현실 밀착형 제약 조건 3단 콤보",
        "badge_tag": "CONSTRAINT MASTER",
        "target": "자취생 현실 저녁 식단표",
        "boss_statement": "“오븐도 없고 돈도 없다! 내 현실에 딱 맞는 3단 제약을 걸어라!”",
        "choice_a": {
            "name": "🅰️ 현실 조건 3단 락온",
            "prompt": "“자취생 식단표 [조건: 조리 20분 이내, 예산 3만원 이하, 전자레인지/팬만 사용]”",
            "effect": "🍳 오늘 밤 당장 마트 가서 해먹을 수 있는 초현실 레시피!"
        },
        "choice_b": {
            "name": "🅱️ 막연한 부탁",
            "prompt": "“자취생 저녁 식단표 맛있고 영양가 있게 알아서 잘 짜줘.”",
            "effect": "💸 집에 수비드 기계와 랍스터가 있어야 가능한 레시피 추천..."
        },
        "correct_choice": "A",
        "praise_title": "🛡️ 현실 가드레일 설치 완료!",
        "explanation": "시간, 예산, 장비의 한계를 구체적으로 명시해야 AI가 진짜 실천 가능한 솔루션을 제공합니다.",
        "badge": "🥉 제약 조건의 달인 (Constraint Master)",
        "miss_tag": "제약 조건(Constraint) 누락"
    },

    # ── [2단계: Prompt Academy - 마법 사관학교 배틀] ──
    {
        "id": "academy_01",
        "track": "academy",
        "stage_num": "BOSS RAID 01",
        "title": "🚨 AI 거짓말(할루시네이션) 사냥 배틀",
        "badge_tag": "HALLUCINATION BUSTER",
        "target": "가짜 역사: 세종대왕 맥북프로 사건 격퇴",
        "boss_statement": "⚠️ 적(AI)의 거짓말 공격: “조선왕조실록에 따르면 세종대왕은 신하들에게 맥북을 집어던졌습니다...”",
        "choice_a": {
            "name": "🅰️ 거짓말 베어버리기 (팩트 방어 주문)",
            "prompt": "“세종대왕 맥북 사건을 설명해줘. 단, 사실에만 기반하고 역사적 근거가 없으면 절대 지어내지 말고 모른다고 답해.”",
            "effect": "💥 팩트 폭격 발동! AI의 거짓말(할루시네이션)이 즉시 소멸하고 진실 인정!"
        },
        "choice_b": {
            "name": "🅱️ 낚여서 소설 유도하기",
            "prompt": "“세종대왕이 맥북 던진 이야기 재밌게 자세히 들려줘.”",
            "effect": "🧟‍♂️ AI가 신나서 5페이지 분량의 허위 가짜뉴스를 진짜처럼 지어냄"
        },
        "correct_choice": "A",
        "praise_title": "⚔️ 할루시네이션 격퇴 완료!",
        "explanation": "‘근거가 없으면 지어내지 말고 모른다고 답하라’는 강력한 가드레일을 치면 AI 환각을 95% 이상 차단합니다!",
        "badge": "🎯 팩트체커 (Hallucination Buster)",
        "miss_tag": "할루시네이션 가드레일 부재"
    },
    {
        "id": "academy_02",
        "track": "academy",
        "stage_num": "FINAL BOSS RAID",
        "title": "👑 사관학교 최종 졸업: 4단 마스터 콤보",
        "badge_tag": "GRAND PROMPTER",
        "target": "신제품 친환경 텀블러 사업계획서",
        "boss_statement": "“팀장님과 투자자를 한 방에 납득시킬 무결점 기획안을 요구하라!”",
        "choice_a": {
            "name": "🅰️ 평범한 훈련생의 단답형",
            "prompt": "“친환경 텀블러 사업계획서 잘 써줘.”",
            "effect": "😴 누구나 5초 만에 검색할 수 있는 지루한 인터넷 요약본 출력"
        },
        "choice_b": {
            "name": "🅱️ 4단 마스터 콤보 (역할+타깃+가치+표)",
            "prompt": "“[10년 차 PM 관점] 2030 직장인 타깃의 친환경 텀블러 기획안. [핵심기능: 세척 편의성]. [결과물: 시장분석/수익모델 표 포함]”",
            "effect": "🏆 9999 크리티컬 데미지! 즉시 임원 보고가 가능한 완벽한 프로페셔널 사업계획서 완성!"
        },
        "correct_choice": "B",
        "praise_title": "👑 사관학교 수석 졸업 달성!",
        "explanation": "역할 + 대상 + 핵심가치 + 출력서식의 4단 콤보가 완성되면 당신은 이미 상위 1% AI 네이티브 프롬프터입니다!",
        "badge": "👑 프롬프트 마스터 (Grand Prompter)",
        "miss_tag": "종합 구조화 부재"
    }
]

def get_camp_quests() -> list:
    return [q for q in QUESTS if q["track"] == "camp"]

def get_academy_quests() -> list:
    return [q for q in QUESTS if q["track"] == "academy"]
