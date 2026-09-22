"""실사용자 피드백 수집 및 저장 모듈
파이널 프로젝트 필수 요건(실사용자 5인 이상 피드백 수집) 지원
"""

import json
import os
from datetime import datetime

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "feedback.json")

def load_feedback() -> list:
    os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_feedback_entry(name: str, role: str, rating: int, helpful_point: str, improvement_point: str) -> bool:
    entries = load_feedback()
    new_entry = {
        "id": len(entries) + 1,
        "name": name if name.strip() else f"테스터 #{len(entries) + 1}",
        "role": role,
        "rating": rating,
        "helpful_point": helpful_point,
        "improvement_point": improvement_point,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    entries.append(new_entry)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    return True
