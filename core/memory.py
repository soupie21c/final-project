"""Long-term Memory 모듈
사용자의 학습 이력, 획득 배지, 사관학교 입교 여부, 반복되는 취약점 패턴 영속화
"""

import json
import os

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "memory.json")

DEFAULT_PROFILE = {
    "user_name": "훈련생",
    "selected_mentor": "harin",
    "camp_passed": False,
    "academy_passed": False,
    "score": 0,
    "badges": [],
    "solved_quests": [],
    "weakness_history": {},  # e.g., {"출력 형식(Format) 누락": 2}
    "total_tunes": 0
}

def load_memory() -> dict:
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        save_memory(DEFAULT_PROFILE)
        return DEFAULT_PROFILE.copy()
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # 기본 키 누락 방지
            for k, v in DEFAULT_PROFILE.items():
                if k not in data:
                    data[k] = v
            return data
    except Exception:
        return DEFAULT_PROFILE.copy()

def save_memory(data: dict):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def record_quest_success(quest_id: str, badge: str, points: int = 20) -> dict:
    mem = load_memory()
    if quest_id not in mem["solved_quests"]:
        mem["solved_quests"].append(quest_id)
        mem["score"] += points
    if badge and badge not in mem["badges"]:
        mem["badges"].append(badge)
    
    # 부트캠프 통과 여부 검사 (camp_01, camp_02, camp_03 모두 클리어 시)
    camp_ids = ["camp_01", "camp_02", "camp_03"]
    if all(cid in mem["solved_quests"] for cid in camp_ids):
        mem["camp_passed"] = True

    # 사관학교 통과 여부 검사 (academy_01, academy_02)
    academy_ids = ["academy_01", "academy_02"]
    if all(aid in mem["solved_quests"] for aid in academy_ids):
        mem["academy_passed"] = True

    save_memory(mem)
    return mem

def record_weakness(miss_tag: str) -> dict:
    mem = load_memory()
    mem["weakness_history"][miss_tag] = mem["weakness_history"].get(miss_tag, 0) + 1
    save_memory(mem)
    return mem

def get_weakness_summary(mem: dict) -> str:
    history = mem.get("weakness_history", {})
    if not history:
        return "아직 기록된 취약점이 없습니다. 완벽한 흐름을 유지하고 계십니다!"
    
    # 가장 많이 발생한 취약점 찾기
    sorted_weak = sorted(history.items(), key=lambda x: x[1], reverse=True)
    top_tag, top_count = sorted_weak[0]
    return f"가장 자주 놓치는 요소는 **'{top_tag}'** ({top_count}회)입니다. 질문 시 이 점을 한 번 더 점검하세요!"
