import json

base_topics = [
    "4.1 조직과 그 상황의 이해", "4.2 이해관계자의 니즈와 기대 이해", "4.3 품질경영시스템 적용범위 결정",
    "5.1 리더십과 의지표명", "5.2 품질방침", "5.3 조직의 역할, 책임 및 권한",
    "6.1 리스크와 기회를 다루는 조치", "6.2 품질목표와 목표달성 기획", "6.3 변경의 기획",
    "7.1 자원", "7.2 적격성", "7.3 인식", "7.4 의사소통", "7.5 문서화된 정보",
    "8.1 운용 기획 및 관리", "8.2 제품 및 서비스에 대한 요구사항", "8.3 제품 및 서비스의 설계와 개발",
    "8.4 외부에서 제공되는 프로세스, 제품 및 서비스의 관리", "8.5 생산 및 서비스 제공", "8.6 제품 및 서비스의 불출", "8.7 부적합 출력물의 관리",
    "9.1 모니터링, 측정, 분석 및 평가", "9.2 내부심사", "9.3 경영검토",
    "10.1 일반사항", "10.2 부적합 및 시정조치", "10.3 지속적 개선"
]

scenarios = [
    "제조업", "IT/소프트웨어", "건설업", "서비스업", "의료기기 생산", "식품 가공업",
    "물류/유통", "자동차 부품", "항공우주", "화학 플랜트"
]

types = [
    "실무 적용 사례를 들어 설명해주세요.",
    "내부 심사 시 주로 지적되는 부적합 사례를 2가지 제시하세요.",
    "매뉴얼 작성 시 반드시 포함되어야 할 핵심 요소를 나열하세요.",
    "이 요구사항을 위반했을 때 조직이 겪을 수 있는 리스크는 무엇인가요?",
    "경영진이 이 조항을 어떻게 지원해야 하는지 설명하세요."
]

questions = []
for i in range(1000):
    topic = base_topics[i % len(base_topics)]
    scenario = scenarios[(i // len(base_topics)) % len(scenarios)]
    q_type = types[(i // (len(base_topics) * len(scenarios))) % len(types)]
    
    q_text = f"[{scenario} 산업] ISO 9001:2015 규격의 '{topic}' 요구사항에 관하여 질문드립니다. {q_type} (문항 {i+1})"
    questions.append(q_text)

with open("benchmark_1000_questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Generated {len(questions)} questions.")
