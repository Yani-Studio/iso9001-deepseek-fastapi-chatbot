"""Mac 로컬 전용 Streamlit 채팅 앱 (서버 API 연동)"""
import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="NEON ISO 9001", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stApp {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif !important;
}
/* Neon Title Effect */
h1 {
    color: #dfbfff !important;
    text-shadow: 0 0 10px #b57bf9, 0 0 20px #8b3dff, 0 0 40px #8b3dff !important;
    font-weight: 800 !important;
    letter-spacing: 1px;
}
/* Subtle glow for sidebar titles */
h2 {
    color: #b57bf9 !important;
    text-shadow: 0 0 5px #8b3dff;
}
/* Glowing accents for the chat interface */
.stTextInput > div > div > input {
    box-shadow: 0 0 10px rgba(181, 123, 249, 0.2);
    border: 1px solid #b57bf9 !important;
}
</style>
""", unsafe_allow_html=True)

SERVER_URL = "http://192.168.0.34:8000"

st.title("🔮 ISO 9001 Chatbot Expert")

# 상태 초기화
if "models" not in st.session_state:
    st.session_state.models = []
if "current_model" not in st.session_state:
    st.session_state.current_model = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 모델 목록 불러오기
def fetch_models():
    try:
        res = requests.get(f"{SERVER_URL}/models", timeout=10)
        if res.status_code == 200:
            data = res.json()
            st.session_state.models = data["models"]
            st.session_state.current_model = data["current_loaded"]
            return True
    except:
        pass
    return False

# 사이드바
with st.sidebar:
    st.header("⚙️ 시스템 제어")
    if st.button("🔄 서버 상태 새로고침"):
        if fetch_models():
            st.success("서버와 연결되었습니다.")
        else:
            st.error("서버 연결 실패. (API 서버가 실행 중인지 확인하세요)")
    
    st.divider()
    
    if st.session_state.models:
        model_names = {m["name"]: m["id"] for m in st.session_state.models}
        
        # 현재 로드된 모델을 기본값으로 선택
        idx = 0
        if st.session_state.current_model:
            for i, m in enumerate(st.session_state.models):
                if m["id"] == st.session_state.current_model:
                    idx = i
                    
        selected_name = st.selectbox("🤖 모델 스위칭 (VRAM 다이나믹 로드)", list(model_names.keys()), index=idx)
        selected_id = model_names[selected_name]
        
        if selected_id != st.session_state.current_model:
            if st.button("🚀 이 모델로 전환하기"):
                with st.spinner("기존 모델 언로드 및 새 모델 로드 중... (10~20초 소요)"):
                    try:
                        res = requests.post(f"{SERVER_URL}/load", json={"model_id": selected_id}, timeout=600)
                        if res.status_code == 200:
                            st.session_state.current_model = selected_id
                            st.success(f"✅ {selected_name} 로드 완료!")
                            st.session_state.messages = [] # 대화 초기화
                        else:
                            st.error(f"로드 실패: {res.text}")
                    except Exception as e:
                        st.error(f"통신 에러: {e}")
    else:
        st.warning("서버에서 불러온 모델이 없습니다. 먼저 '새로고침'을 누르세요.")

st.divider()

# 채팅 인터페이스
if st.session_state.current_model:
    st.caption(f"현재 연결된 모델: **{st.session_state.current_model}**")
    
    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🔮"
        with st.chat_message(msg["role"], avatar=avatar):
            if msg.get("thinking"):
                with st.expander("🤔 AI 추론 과정 (Chain of Thought)"):
                    st.markdown(f"```text\n{msg['thinking']}\n```")
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("ISO 9001에 관해 무엇이든 물어보세요!"):
        # 유저 메시지 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
            
        # 봇 응답 (API 요청)
        with st.chat_message("assistant", avatar="🔮"):
            with st.spinner("AI가 답변을 생성 중입니다..."):
                try:
                    res = requests.post(
                        f"{SERVER_URL}/chat_stream", 
                        json={"model_id": st.session_state.current_model, "message": prompt},
                        stream=True,
                        timeout=600
                    )
                    if res.status_code == 200:
                        status_box = None
                        answer_placeholder = st.empty()
                        
                        raw_buffer = ""
                        context = ""
                        has_think_tag = False
                        is_thinking = False
                        thinking_content = ""
                        answer_content = ""
                        
                        for line in res.iter_lines():
                            if line:
                                decoded_line = line.decode('utf-8')
                                if decoded_line.startswith("data: "):
                                    data_str = decoded_line[6:]
                                    if data_str == "[DONE]":
                                        break
                                    try:
                                        data = json.loads(data_str)
                                    except:
                                        continue
                                        
                                    if "context_used" in data:
                                        context = data["context_used"]
                                    if "token" in data:
                                        raw_buffer += data["token"]
                                        
                                        # On-the-fly Parser
                                        if not has_think_tag:
                                            if "<think>" in raw_buffer or "Here's a thinking process:" in raw_buffer:
                                                has_think_tag = True
                                                is_thinking = True
                                                status_box = st.status("💭 AI가 심도 있게 추론 중입니다...", expanded=False)
                                                
                                        if is_thinking:
                                            if "</think>" in raw_buffer:
                                                is_thinking = False
                                                parts = raw_buffer.split("</think>", 1)
                                                thinking_content = parts[0].replace("<think>", "").replace("Here's a thinking process:", "").strip()
                                                answer_content = parts[1].lstrip()
                                                
                                                if status_box:
                                                    status_box.update(label="✅ 추론 완료", state="complete", expanded=False)
                                                    with status_box:
                                                        st.markdown(f"```text\n{thinking_content}\n```")
                                                        
                                                answer_placeholder.markdown(answer_content + "▌")
                                        else:
                                            if has_think_tag:
                                                parts = raw_buffer.split("</think>", 1)
                                                if len(parts) > 1:
                                                    answer_content = parts[1].lstrip()
                                            else:
                                                answer_content = raw_buffer.lstrip()
                                                
                                            answer_placeholder.markdown(answer_content + "▌")
                                            
                        # Final render without cursor
                        if not answer_content and raw_buffer:
                            answer_content = "⚠️ (AI가 너무 깊게 생각하다가 답변이 끊겼습니다. 조금 더 구체적으로 질문해주세요.)"
                            if not has_think_tag:
                                answer_content = raw_buffer
                        answer_placeholder.markdown(answer_content)
                        
                        if context:
                            with st.expander("참조된 ISO 9001 문서(RAG)"):
                                st.text(context)
                                
                        st.session_state.messages.append({"role": "assistant", "content": answer_content, "thinking": thinking_content})
                    else:
                        st.error(f"API 에러: {res.text}")
                except Exception as e:
                    st.error(f"통신 에러: {e}")
else:
    st.info("👈 사이드바에서 먼저 통신할 AI 모델을 로드해주세요.")
