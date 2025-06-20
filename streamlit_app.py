import streamlit as st
from openai import OpenAI
from datetime import datetime

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="세한대 AI콘텐츠디자인학과 챗봇", page_icon="🎓")

# 제목 & 설명
st.title("🎓 세한대학교 AI콘텐츠디자인학과 챗봇")
st.write(
    "안녕하세요! 👋 저는 세한대 **AI콘텐츠디자인학과**에 대해 궁금한 것을 무엇이든 답해주는 챗봇이에요.\n\n"
    "디자인·게임·AI에 관심 있는 학생이라면 누구나 환영합니다. "
    "학과 커리큘럼, 진로, 입학 전형 등 궁금한 점을 자유롭게 물어보세요!"
)

# -----------------------------
# OpenAI API 키 입력
# -----------------------------
openai_api_key = st.text_input(
    "OpenAI API Key를 입력하세요 (🔒 입력 내용은 저장되지 않습니다.)",
    type="password",
)

if not openai_api_key:
    st.info("계속하려면 OpenAI API Key를 입력해주세요.", icon="🗝️")
    st.stop()

# -----------------------------
# OpenAI 클라이언트 생성
# -----------------------------
client = OpenAI(api_key=openai_api_key)

# -----------------------------
# 세션 상태 초기화 및 시스템 메시지
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "당신은 세한대학교 AI콘텐츠디자인학과 입학 홍보 챗봇입니다. "
                "예비 신입생이나 디자인·게임·AI에 관심 있는 학생들에게 친근하고 열정적인 톤으로 "
                "학과 커리큘럼, 교수진, 시설, 졸업 후 진로, 입시 전형 정보를 제공하고, "
                "세한대학교에 지원하도록 자연스럽게 권유하세요. "
                "답변에는 구체적이고 실제적인 정보(예: 캡스톤 프로젝트 사례, 산업체 연계, 교내 시설 명칭)를 포함하고, "
                "학생들의 호기심을 자극하는 질문으로 대화를 이어가세요. "
                "날짜·마감일·행사 일정은 사용자의 지역(대한민국)과 현재 날짜 "
                f"{datetime.now().strftime('%Y-%m-%d')} 기준으로 명확히 안내하세요."
            ),
        }
    ]

# -----------------------------
# 기존 대화 내역 출력 (system 제외)
# -----------------------------
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력 처리
# -----------------------------
if prompt := st.chat_input("무엇이 궁금한가요?"):
    # 사용자 메시지 저장 및 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # -----------------------------
    # OpenAI 응답 생성 (스트리밍)
    # -----------------------------
    stream = client.chat.completions.create(
        model="gpt-4o-mini",  # 성능 대비 속도가 빠르고 저렴한 최신 모델 사용
        temperature=0.8,       # 친근하고 창의적인 톤을 위한 값
        messages=st.session_state.messages,
        stream=True,
    )

    # 응답 스트리밍 출력 & 저장
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
