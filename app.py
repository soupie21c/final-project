"""Prompt Camp to Academy - Codyssey 에디션
코디세이(Codyssey) LMS 플랫폼 스타일 디자인 & 1단계 완료 시 2단계 자동 화면 전환 탑재
"""

import streamlit as st
import streamlit.components.v1 as components
import time
import os
from core.mentors import MENTORS, get_mentor
from core.quests import get_camp_quests, get_academy_quests
from core.memory import (
    load_memory, save_memory, record_quest_success, 
    record_weakness, get_weakness_summary
)
from core.agents import tune_and_compare_prompt
from core.feedback import load_feedback, save_feedback_entry

def scroll_to_element(element_id: str):
    """지정된 HTML ID 위치로 부드럽게 자동 스크롤 이동"""
    if not element_id:
        return
    js_code = f"""
    <script>
        setTimeout(function() {{
            try {{
                var target = window.parent.document.getElementById('{element_id}');
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                }}
            }} catch(e) {{}}
        }}, 250);
    </script>
    """
    components.html(js_code, height=0, width=0)

# ── 1. 페이지 설정 ──
st.set_page_config(
    page_title="Codyssey AI Native | Prompt Camp to Academy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 2. 세션 메모리 & 네비게이션 상태 초기화 ──
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()
mem = st.session_state.memory

# 기본 네비게이션 탭 (1단계 -> 2단계 자동 전환을 지원하는 스테이트)
if "current_nav" not in st.session_state:
    # 이미 캠프를 수료했으면 사관학교, 아니면 캠프로 시작
    st.session_state.current_nav = "academy" if mem.get("camp_passed") else "camp"

# ── 3. 코디세이(Codyssey) LMS 프리미엄 테마 CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800;900&display=swap');
    
    * { font-family: 'Pretendard', -apple-system, sans-serif; }

    /* 코디세이 다크 블루 & 슬레이트 테마 */
    .stApp {
        background: #0B1120 !important;
        color: #F1F5F9 !important;
    }

    /* 사이드바 가독성 완벽 개선 */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stTextInput label {
        color: #E2E8F0 !important;
        font-weight: 700 !important;
    }

    /* 모든 버튼 텍스트 가독성 100% 보장 */
    .stButton > button {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }
    .stButton > button:hover {
        background-color: #334155 !important;
        color: #38BDF8 !important;
        border-color: #38BDF8 !important;
    }
    /* Primary 활성 버튼 (선택된 탭) */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 2px solid #60A5FA !important;
        font-weight: 900 !important;
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.5) !important;
    }

    /* A안 버튼 (블루 테마) */
    button[key*="camp_a_"], button[key*="acad_a_"] {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
        border: 1px solid #60A5FA !important;
        font-weight: 800 !important;
    }
    /* B안 버튼 (핑크 테마) */
    button[key*="camp_b_"], button[key*="acad_b_"] {
        background-color: #BE185D !important;
        color: #FFFFFF !important;
        border: 1px solid #F472B6 !important;
        font-weight: 800 !important;
    }

    /* 코디세이 학습 대시보드 카드 */
    .lms-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }

    /* 시네마틱 배너 */
    .hero-banner-camp {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.3) 0%, rgba(15, 23, 42, 0.95) 100%), url('assets/bg_camp.jpg');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 2.2rem;
        border: 1px solid #334155;
        margin-bottom: 1.8rem;
    }
    .hero-banner-academy {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.25) 0%, rgba(15, 23, 42, 0.95) 100%), url('assets/bg_academy.jpg');
        background-size: cover;
        background-position: center;
        border-radius: 16px;
        padding: 2.2rem;
        border: 1px solid #4F46E5;
        margin-bottom: 1.8rem;
    }

    /* A/B 선택 카드 (코디세이 클린 스타일) */
    .quest-choice-card {
        background: #111827;
        border: 2px solid #334155;
        border-radius: 14px;
        padding: 1.4rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .quest-choice-card-a {
        border-top: 4px solid #3B82F6;
    }
    .quest-choice-card-b {
        border-top: 4px solid #EC4899;
    }
    .quest-prompt-box {
        background: #0B0F19;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 1rem;
        font-size: 1.0rem;
        font-weight: 600;
        color: #F8FAFC;
        margin: 12px 0;
        line-height: 1.5;
    }

    /* 멘토 피드백 버블 */
    .mentor-msg-box {
        display: flex;
        align-items: center;
        gap: 14px;
        background: #1E293B;
        border-radius: 12px;
        padding: 14px 18px;
        margin-top: 1rem;
    }

    /* 1:1 연구소 좌우 비교 카드 */
    .lab-display-card {
        background: #111827;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1.4rem;
        min-height: 380px;
    }
</style>
""", unsafe_allow_html=True)

# ── 4. 사이드바 (코디세이 멘토 & 학습 프로필) ──
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:1rem;">
        <span style="font-size:1.6rem;">🧭</span>
        <div>
            <div style="font-weight:900; font-size:1.1rem; color:#FFF;">Codyssey AI</div>
            <div style="font-size:0.75rem; color:#94A3B8;">AI 네이티브 파이널 프로젝트</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    mentor_options = {
        "harin": "✨ 유하린 (아이돌 센터 / 무한칭찬)",
        "dohyuk": "🕶️ 차도혁 (천재선배 / 츤데레첨삭)",
        "taesan": "🔥 강태산 (에이스교관 / 불꽃카리스마)"
    }
    
    current_key = mem.get("selected_mentor", "harin")
    selected_key = st.selectbox(
        "나의 전담 AI 스타 멘토",
        options=list(mentor_options.keys()),
        format_func=lambda k: mentor_options[k],
        index=list(mentor_options.keys()).index(current_key) if current_key in mentor_options else 0
    )

    if selected_key != mem.get("selected_mentor"):
        mem["selected_mentor"] = selected_key
        save_memory(mem)
        st.rerun()

    mentor = get_mentor(selected_key)
    img_path = mentor.get("image", "")

    # 멘토 사진 출력
    if img_path and os.path.exists(img_path):
        st.image(img_path, use_container_width=True)

    st.markdown(f"""
    <div style="background:#1E293B; border-radius:10px; padding:12px; border-left:3px solid {mentor['color']}; margin-top:8px;">
        <div style="font-weight:800; color:#FFF; font-size:1.05rem;">{mentor['avatar']} {mentor['name']}</div>
        <div style="color:{mentor['color']}; font-size:0.8rem; font-weight:700;">{mentor['title']}</div>
        <div style="font-size:0.85rem; color:#CBD5E1; margin-top:6px; font-style:italic;">"{mentor['greeting']}"</div>
    </div>
    """, unsafe_allow_html=True)

    # 코디세이 수강생 진도 현황
    st.markdown("---")
    st.markdown("#### 📊 코디세이 학습 진도")
    solved_count = len(mem.get("solved_quests", []))
    progress_rate = int((solved_count / 5) * 100)
    
    st.progress(progress_rate / 100)
    col_p1, col_p2 = st.columns(2)
    col_p1.metric("총 진도율", f"{progress_rate}%")
    col_p2.metric("획득 점수", f"{mem.get('score', 0)} 점")

    # 취약점 분석 노트
    weak_txt = get_weakness_summary(mem)
    st.info(f"💡 **AI 학습 코칭 노트**\n\n{weak_txt}")

    # 획득 배지
    if mem.get("badges"):
        st.markdown("**보유 인증 배지:**")
        for b in mem.get("badges"):
            st.markdown(f"<span style='background:#0F172A; border:1px solid #334155; padding:2px 8px; border-radius:10px; font-size:0.75rem; margin-right:3px; display:inline-block; margin-bottom:3px;'>{b}</span>", unsafe_allow_html=True)

    # API 설정
    st.markdown("---")
    api_key_input = st.text_input("OpenAI API Key (선택)", type="password", placeholder="sk-...", help="Key가 없어도 자체 스마트 시뮬레이션으로 모든 기능을 즉시 체험할 수 있습니다.")
    
    if st.button("🔄 학습 이력 초기화"):
        from core.memory import DEFAULT_PROFILE
        save_memory(DEFAULT_PROFILE.copy())
        st.session_state.memory = DEFAULT_PROFILE.copy()
        st.session_state.current_nav = "camp"
        st.rerun()

# ── 5. 코디세이 상단 GNB 바 ──
status_label = "사관학교 정식 생도" if mem.get("camp_passed") else "부트캠프 입문생"
st.markdown(f"""
<div class="codyssey-gnb">
    <div class="codyssey-logo">
        <span style="color:#3B82F6;">Codyssey</span> AI Native LMS
        <span class="codyssey-badge">FINAL PROJECT</span>
    </div>
    <div style="display:flex; align-items:center; gap:20px;">
        <span style="color:#94A3B8; font-size:0.9rem;">학습자: <b>{mem.get('user_name', '훈련생')}</b> ({status_label})</span>
        <span style="background:#2563EB; color:#FFF; padding:4px 12px; border-radius:20px; font-size:0.85rem; font-weight:700;">
            STAGE {2 if mem.get('camp_passed') else 1} 진행 중
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 6. 네비게이션 탭 (1단계 완료 시 자동 전환을 지원하는 버튼 그룹) ──
nav_cols = st.columns(4)
nav_items = [
    ("camp", "⛺ 1단계: Prompt Camp (입문)"),
    ("academy", "🏛️ 2단계: Prompt Academy (사관학교)"),
    ("lab", "🔬 1:1 프롬프트 연구소"),
    ("feedback", "💬 실사용자 평가 피드백")
]

for i, (key, label) in enumerate(nav_items):
    is_active = (st.session_state.current_nav == key)
    btn_type = "primary" if is_active else "secondary"
    if nav_cols[i].button(label, key=f"nav_btn_{key}", type=btn_type, use_container_width=True):
        st.session_state.current_nav = key
        st.rerun()

current_tab = st.session_state.current_nav

# ── [STAGE 1] Prompt Camp (부트캠프) ──
if current_tab == "camp":
    st.markdown("""
    <div class="hero-banner-camp">
        <span style="background:#EA580C; color:#FFF; font-weight:800; font-size:0.8rem; padding:4px 10px; border-radius:6px;">BASIC TRACK 01</span>
        <h1 style="color:#FFF; font-weight:900; margin:0.3rem 0; font-size:2.0rem;">⛺ Prompt Camp: 기초 프롬프트 훈련소</h1>
        <p style="color:#E2E8F0; font-size:1.0rem; margin:0; line-height:1.5;">
            "긴 줄글 시험은 이제 그만! 코디세이 학습자를 위한 <b>A안 vs B안 밸런스 훈련</b>.<br>
            3개의 필수 기초 미션을 클리어하면 <b>사관학교(STAGE 2)로 자동 진입</b>합니다!"
        </p>
    </div>
    """, unsafe_allow_html=True)

    camp_quests = get_camp_quests()
    all_camp_cleared = all(q["id"] in mem.get("solved_quests", []) for q in camp_quests)

    for idx, q in enumerate(camp_quests):
        is_solved = q["id"] in mem.get("solved_quests", [])
        status_badge = "✅ 수료 완료" if is_solved else "⏳ 미수료"
        badge_color = "#10B981" if is_solved else "#64748B"

        # 자동 스크롤을 위한 고유 앵커 ID
        st.markdown(f'<div id="quest_{q["id"]}" style="margin-top: 10px;"></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin:1.2rem 0 0.5rem 0;">
            <span style="font-weight:800; font-size:1.05rem; color:#FFF;">{q['stage_num']} : {q['title']}</span>
            <span style="color:{badge_color}; font-weight:700; font-size:0.85rem;">{status_badge}</span>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class="quest-choice-card quest-choice-card-a">
                <div>
                    <div style="font-weight:800; color:#60A5FA; font-size:1.05rem;">{q['choice_a']['name']}</div>
                    <div class="quest-prompt-box">{q['choice_a']['prompt']}</div>
                    <div style="font-size:0.85rem; color:#94A3B8;">{q['choice_a']['effect']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            pick_a = st.button("🅰️ A안 선택하기", key=f"camp_a_{q['id']}", use_container_width=True)

        with col_b:
            st.markdown(f"""
            <div class="quest-choice-card quest-choice-card-b">
                <div>
                    <div style="font-weight:800; color:#F472B6; font-size:1.05rem;">{q['choice_b']['name']}</div>
                    <div class="quest-prompt-box">{q['choice_b']['prompt']}</div>
                    <div style="font-size:0.85rem; color:#94A3B8;">{q['choice_b']['effect']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            pick_b = st.button("🅱️ B안 선택하기", key=f"camp_b_{q['id']}", use_container_width=True)

        # 판정 및 다음 문제로 아래 자동 스크롤 로직!
        user_choice = "A" if pick_a else ("B" if pick_b else None)
        if user_choice:
            if user_choice == q["correct_choice"]:
                st.balloons()
                st.success(f"🎉 **정답입니다! {q['praise_title']}**\n\n{q['explanation']}")
                
                # 멘토 메시지
                st.markdown(f"""
                <div class="mentor-msg-box" style="border-left:4px solid {mentor['color']};">
                    <span style="font-size:1.8rem;">{mentor['avatar']}</span>
                    <div>
                        <div style="font-weight:800; color:{mentor['color']}; font-size:0.9rem;">{mentor['name']} 멘토:</div>
                        <div style="color:#FFF; font-size:0.95rem;">"{mentor['praise']}"</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 메모리 저장
                updated_mem = record_quest_success(q["id"], q["badge"], points=20)
                st.session_state.memory = updated_mem

                # 다음 스크롤 대상 결정 (아래로 자동 스크롤)
                if idx + 1 < len(camp_quests):
                    next_quest = camp_quests[idx + 1]
                    st.session_state.scroll_target = f"quest_{next_quest['id']}"
                else:
                    st.session_state.scroll_target = "camp_complete_ticket"

                time.sleep(0.8)
                st.rerun()
            else:
                st.error("❌ 아쉽습니다! 다시 한번 생각해보세요.")
                st.session_state.memory = record_weakness(q["miss_tag"])
                st.markdown(f"""
                <div class="mentor-msg-box" style="border-left:4px solid #EF4444;">
                    <span style="font-size:1.8rem;">{mentor['avatar']}</span>
                    <div>
                        <div style="font-weight:800; color:#EF4444; font-size:0.9rem;">{mentor['name']} 멘토의 조언:</div>
                        <div style="color:#FCA5A5; font-size:0.95rem;">"{mentor['scold']}"</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border:none; border-top:1px solid #1E293B; margin:1.5rem 0;'>", unsafe_allow_html=True)

    # 3개 클리어 시 수료 티켓 및 사관학교 수동 입장 버튼
    if mem.get("camp_passed"):
        st.markdown('<div id="camp_complete_ticket"></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, #1E1B4B, #311042); border:2px dashed #A855F7; border-radius:16px; padding:1.8rem; text-align:center; margin:1.5rem 0;">
            <h2 style="color:#C084FC; margin-bottom:0.4rem;">🎉 PROMPT CAMP 기초 훈련 수료 완료! 🎉</h2>
            <p style="color:#E2E8F0; font-size:1.05rem; line-height:1.6;">
                축하합니다! 필수 3개 기초 프롬프트 훈련을 모두 마쳤습니다.<br>
                충분히 복습하신 후, 아래 버튼을 눌러 <b>'2단계: Prompt Academy 사관학교'</b>로 입장하세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏛️ 2단계: Prompt Academy 사관학교 입장하기 ➡️", type="primary", use_container_width=True):
            st.session_state.current_nav = "academy"
            st.rerun()

    # 스크롤 트리거 실행
    if st.session_state.get("scroll_target"):
        scroll_to_element(st.session_state.scroll_target)
        st.session_state.scroll_target = None

# ── [STAGE 2] Prompt Academy (실전 사관학교) ──
elif current_tab == "academy":
    st.markdown("""
    <div class="hero-banner-academy">
        <span style="background:#4F46E5; color:#FFF; font-weight:800; font-size:0.8rem; padding:4px 10px; border-radius:6px;">ADVANCED TRACK 02</span>
        <h1 style="color:#FFF; font-weight:900; margin:0.3rem 0; font-size:2.0rem;">🏛️ Prompt Academy: 실전 마스터 사관학교</h1>
        <p style="color:#E0E7FF; font-size:1.0rem; margin:0; line-height:1.5;">
            "부트캠프 수료를 축하합니다! 이제 실전 심화 단계에 오신 것을 환영합니다.<br>
            AI의 그럴듯한 거짓말(할루시네이션)을 팩트로 무찌르고, 완벽한 4단 마스터 콤보를 체득하세요!"
        </p>
    </div>
    """, unsafe_allow_html=True)

    if not mem.get("camp_passed"):
        st.warning("⚠️ 아직 부트캠프(1단계) 과정을 모두 통과하지 않았습니다! 먼저 부트캠프 3개 퀘스트를 완료해 주세요.")

    academy_quests = get_academy_quests()
    for idx, q in enumerate(academy_quests):
        is_solved = q["id"] in mem.get("solved_quests", [])
        status_badge = "🏆 정복 완료" if is_solved else "⚔️ 실전 도전 중"
        badge_color = "#10B981" if is_solved else "#F59E0B"

        st.markdown(f'<div id="quest_{q["id"]}" style="margin-top: 10px;"></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#1E1B4B; border:1px solid #4338CA; border-radius:12px; padding:1.2rem; margin:1.2rem 0 0.8rem 0;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:800; color:#FFF; font-size:1.1rem;">{q['stage_num']} : {q['title']}</span>
                <span style="color:{badge_color}; font-weight:700; font-size:0.85rem;">{status_badge}</span>
            </div>
            <div style="color:#CBD5E1; font-size:0.95rem; margin-top:8px;">
                {q['boss_statement']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class="quest-choice-card quest-choice-card-a">
                <div>
                    <div style="font-weight:800; color:#60A5FA; font-size:1.05rem;">{q['choice_a']['name']}</div>
                    <div class="quest-prompt-box">{q['choice_a']['prompt']}</div>
                    <div style="font-size:0.85rem; color:#94A3B8;">{q['choice_a']['effect']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            acad_a = st.button("🅰️ A안으로 격퇴!", key=f"acad_a_{q['id']}", use_container_width=True)

        with col_b:
            st.markdown(f"""
            <div class="quest-choice-card quest-choice-card-b">
                <div>
                    <div style="font-weight:800; color:#F472B6; font-size:1.05rem;">{q['choice_b']['name']}</div>
                    <div class="quest-prompt-box">{q['choice_b']['prompt']}</div>
                    <div style="font-size:0.85rem; color:#94A3B8;">{q['choice_b']['effect']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            acad_b = st.button("🅱️ B안으로 격퇴!", key=f"acad_b_{q['id']}", use_container_width=True)

        user_choice = "A" if acad_a else ("B" if acad_b else None)
        if user_choice:
            if user_choice == q["correct_choice"]:
                st.balloons()
                st.toast(f"🏆 사관학교 미션 정복! {q['badge']} 수여!", icon="👑")
                st.success(f"👑 **{q['praise_title']}**\n\n{q['explanation']}")
                
                st.markdown(f"""
                <div class="mentor-msg-box" style="border-left:4px solid {mentor['color']};">
                    <span style="font-size:1.8rem;">{mentor['avatar']}</span>
                    <div>
                        <div style="font-weight:800; color:{mentor['color']}; font-size:0.9rem;">{mentor['name']} 멘토의 극찬:</div>
                        <div style="color:#FFF; font-size:0.95rem;">"{mentor['praise']}"</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.memory = record_quest_success(q["id"], q["badge"], points=40)

                # 사관학교 다음 문제 아래로 자동 스크롤
                if idx + 1 < len(academy_quests):
                    next_q = academy_quests[idx + 1]
                    st.session_state.scroll_target = f"quest_{next_q['id']}"
                else:
                    st.session_state.scroll_target = "academy_complete_msg"

                time.sleep(0.8)
                st.rerun()
            else:
                st.error("❌ 실전 판정 실패! 거짓말의 덫에 걸렸습니다.")
                st.session_state.memory = record_weakness(q["miss_tag"])
                st.markdown(f"""
                <div class="mentor-msg-box" style="border-left:4px solid #EF4444;">
                    <span style="font-size:1.8rem;">{mentor['avatar']}</span>
                    <div>
                        <div style="font-weight:800; color:#EF4444; font-size:0.9rem;">{mentor['name']} 멘토의 엄격 피드백:</div>
                        <div style="color:#FCA5A5; font-size:0.95rem;">"{mentor['scold']}"</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<hr style='border:none; border-top:1px solid #1E293B; margin:1.5rem 0;'>", unsafe_allow_html=True)

    if mem.get("academy_passed"):
        st.markdown('<div id="academy_complete_msg"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:linear-gradient(135deg, #1E1B4B, #0F172A); border:2px solid #10B981; border-radius:16px; padding:1.8rem; text-align:center; margin:1.5rem 0;">
            <h2 style="color:#34D399; margin-bottom:0.4rem;">👑 사관학교 최고위 프롬프트 마스터 등극! 👑</h2>
            <p style="color:#E2E8F0; font-size:1.05rem;">모든 사관학교 실전 미션을 정복하셨습니다. 이제 1:1 연구소에서 자유자재로 실무 프롬프트를 튜닝하세요!</p>
        </div>
        """, unsafe_allow_html=True)

    # 사관학교 스크롤 트리거 실행
    if st.session_state.get("scroll_target"):
        scroll_to_element(st.session_state.scroll_target)
        st.session_state.scroll_target = None

# ── [STAGE 3] 1:1 프롬프트 연구소 (비포 & 애프터) ──
elif current_tab == "lab":
    st.markdown("""
    <div style="background:#111827; border:1px solid #1E293B; border-radius:14px; padding:1.8rem; margin-bottom:1.5rem;">
        <h2 style="margin:0 0 6px 0; color:#38BDF8; font-weight:800;">🔬 1:1 실시간 프롬프트 튜닝 연구소</h2>
        <p style="color:#94A3B8; margin:0; font-size:0.95rem;">
            내가 평소 쓰던 자유 질문을 입력하면, 전담 멘토가 프로페셔널 프롬프트로 재작성하여 <b>결과의 품질 차이를 좌우로 나란히 비교</b>해 드립니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 추천 예시 버튼 칩
    st.markdown("**⚡ 코디세이 추천 실무 질문 (클릭 시 자동 입력):**")
    c1, c2, c3, c4 = st.columns(4)
    sample_q = ""
    if c1.button("🏝️ 제주도 2박3일 여행", use_container_width=True): sample_q = "제주도 2박 3일 여행 일정 짜줘"
    if c2.button("🍳 자취생 초간단 저녁 메뉴", use_container_width=True): sample_q = "오늘 저녁에 뭐 먹을지 메뉴 추천해줘"
    if c3.button("💻 주니어 개발자 이력서", use_container_width=True): sample_q = "파이썬 주니어 개발자 이력서 어떻게 써야 해?"
    if c4.button("📊 스타트업 사업계획서", use_container_width=True): sample_q = "우리 AI 서비스 사업계획서 작성 양식 알려줘"

    user_query = st.text_area(
        "평소 질문하시던 스타일대로 적어보세요:",
        value=sample_q,
        height=80,
        placeholder="예: 보고서 요약해줘 / 파이썬 공부법 알려줘 / 신제품 텀블러 마케팅 아이디어 알려줘"
    )

    if st.button("🚀 멘토에게 실시간 튜닝 및 비교 요청", type="primary", use_container_width=True):
        if not user_query.strip():
            st.warning("질문을 먼저 입력해 주세요!")
        else:
            with st.spinner(f"{mentor['name']} 멘토가 실시간으로 프롬프트를 튜닝하고 있습니다..."):
                res = tune_and_compare_prompt(user_query, selected_key, api_key_input, mem)
                
                col_left, col_right = st.columns(2)
                with col_left:
                    st.markdown("""
                    <div class="lab-display-card" style="border-top:4px solid #64748B;">
                        <div style="font-weight:800; color:#94A3B8; margin-bottom:8px;">👈 기존 질문 (BEFORE)</div>
                    """, unsafe_allow_html=True)
                    st.code(res["raw_prompt"], language="text")
                    st.markdown(f"<div style='color:#CBD5E1; line-height:1.6; margin-top:10px;'>{res['raw_answer']}</div>", unsafe_allow_html=True)
                    st.markdown("""
                        <div style="color:#64748B; font-size:0.8rem; margin-top:14px;">⚠️ 특징: 두루뭉술하고 평범한 일반 답변</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_right:
                    st.markdown(f"""
                    <div class="lab-display-card" style="border-top:4px solid #10B981;">
                        <div style="font-weight:800; color:#10B981; margin-bottom:8px;">👉 {mentor['name']}의 튜닝 프롬프트 (AFTER)</div>
                    """, unsafe_allow_html=True)
                    st.code(res["tuned_prompt"], language="markdown")
                    st.markdown(f"<div style='color:#FFF; line-height:1.6; margin-top:10px;'>{res['tuned_answer']}</div>", unsafe_allow_html=True)
                    st.markdown("""
                        <div style="color:#34D399; font-size:0.8rem; margin-top:14px;">✨ 특징: 역할 부여 + 표(Table) 서식 + 실행 제약 조건 완벽 충족</div>
                    </div>
                    """, unsafe_allow_html=True)

                # 멘토 메신저 총평
                st.markdown(f"""
                <div class="mentor-msg-box" style="border-left:4px solid {mentor['color']}; margin-top:1.5rem;">
                    <span style="font-size:2.2rem;">{mentor['avatar']}</span>
                    <div>
                        <div style="font-weight:800; color:{mentor['color']}; font-size:1.0rem;">
                            {mentor['name']} ({mentor['title']})의 1:1 현장 코칭 총평:
                        </div>
                        <div style="color:#FFF; font-size:1.0rem; margin-top:4px; line-height:1.5;">
                            "{res['mentor_feedback']}"
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ── [STAGE 4] 실사용자 피드백 (파이널 필수 5인 수집) ──
elif current_tab == "feedback":
    st.markdown("""
    <div style="background:#111827; border:1px solid #1E293B; border-radius:14px; padding:1.8rem; margin-bottom:1.5rem;">
        <h2 style="margin:0 0 6px 0; color:#38BDF8; font-weight:800;">💬 실사용자 테스트 & 피드백 수집</h2>
        <p style="color:#94A3B8; margin:0; font-size:0.95rem;">
            코디세이 Final Project 평가 필수 요건: 실사용자(5인 이상)의 실제 사용 후기 및 평가를 수집하고 서비스 개선에 반영합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    fb_list = load_feedback()
    col_f1, col_f2 = st.columns([1.2, 0.8])
    
    with col_f1:
        with st.form("codyssey_fb_form", clear_on_submit=True):
            name_in = st.text_input("테스터 성함 / 닉네임", placeholder="예: 김코딩 (교육생)")
            role_in = st.selectbox("소속 그룹", ["코디세이 AI 교육생", "대학생/취준생", "현직 직장인", "비개발자/일반인", "기타"])
            rate_in = st.slider("전반적인 학습 만족도 및 도파민 체감", 1, 5, 5)
            help_in = st.text_area("가장 유익했거나 재미있었던 점", placeholder="예: A/B 밸런스 게임처럼 선택하니 1초 만에 차이가 이해되었고, 1단계 끝나고 2단계로 바로 넘어가는 흐름이 좋았어요.")
            imp_in = st.text_area("개선되었으면 하는 점", placeholder="예: 멘토 음성 TTS 기능도 추가되면 좋겠습니다!")
            
            if st.form_submit_button("피드백 등록하기 📝"):
                save_feedback_entry(name_in, role_in, rate_in, help_in, imp_in)
                st.balloons()
                st.success("피드백이 안전하게 등록되었습니다! 감사합니다.")
                time.sleep(1)
                st.rerun()

    with col_f2:
        st.markdown("#### 📊 실시간 피드백 현황")
        total_n = len(fb_list)
        st.metric("누적 피드백 수", f"{total_n} 명", delta="5인 이상 요건 달성 완료 🎉" if total_n >= 5 else f"{5 - total_n}명 필요")
        if fb_list:
            avg_val = sum(x["rating"] for x in fb_list) / total_n
            st.metric("평균 만족도", f"{avg_val:.1f} / 5.0 ⭐")

    st.markdown("---")
    st.markdown("#### 📋 최근 등록된 테스터 평가 내역")
    if fb_list:
        for f in reversed(fb_list[-5:]):
            with st.chat_message("user"):
                st.markdown(f"**{f['name']}** ({f['role']}) | {'⭐' * f['rating']} | *{f['created_at']}*")
                st.markdown(f"👍 **좋았던 점:** {f['helpful_point']}")
                if f.get('improvement_point'):
                    st.caption(f"💡 **개선 건의:** {f['improvement_point']}")

# ── 7. 코디세이 하단 푸터 ──
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#64748B; font-size:0.85rem; padding:10px 0;">
    © 2026 Codyssey AI Native Final Project | Prompt Camp & Academy | Powered by Streamlit & OpenAI
</div>
""", unsafe_allow_html=True)
