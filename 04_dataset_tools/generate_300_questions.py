import json
import random

def generate_300():
    print("Reading 100 questions...")
    with open("scratch/benchmark_1000_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    base_questions = data[:100]
    
    new_questions = []
    # Copy the first 100
    new_questions.extend(base_questions)
    
    # Generate 200 more by slightly modifying or duplicating with variations
    prefixes = [
        "ISO 9001 규격에 따르면, ",
        "품질경영시스템에서 ",
        "다음 내용에 대해 설명해주세요: ",
        "구체적으로 ",
        "실무 관점에서 "
    ]
    
    suffixes = [
        " 상세히 설명해주실 수 있나요?",
        " 에 대해 논리적으로 답변해주세요.",
        " 관련된 구체적인 예시와 함께 요약해주세요.",
        " 핵심 내용을 위주로 설명해주세요.",
        " 품질경영 관점에서 어떻게 해석해야 하는지 알려주세요."
    ]
    
    for _ in range(2): # 2 iterations over 100 questions = 200 new questions
        for q in base_questions:
            pref = random.choice(prefixes)
            suff = random.choice(suffixes)
            new_questions.append(pref + q + suff)
            
    print(f"Total questions generated: {len(new_questions)}")
    
    with open("scratch/benchmark_300_questions.json", "w", encoding="utf-8") as f:
        json.dump(new_questions, f, ensure_ascii=False, indent=2)
        
    print("Saved to benchmark_300_questions.json")

if __name__ == "__main__":
    generate_300()
