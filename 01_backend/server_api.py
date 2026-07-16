"""서버용 FastAPI 백엔드 (모델 동적 로딩 및 추론)"""
import os
os.environ["HF_HUB_OFFLINE"] = "1"
import gc
import json
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from config import MODELS, MODEL_DIR, DATA_DIR
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

app = FastAPI(title="ISO 9001 Model Server")

# 전역 상태 (현재 VRAM에 올라가 있는 모델)
current_model_id = None
model = None
tokenizer = None

def get_model_info(model_id):
    for m in MODELS:
        if m["id"] == model_id:
            return m
    return None

class LoadRequest(BaseModel):
    model_id: str

class ChatRequest(BaseModel):
    model_id: str
    message: str

@app.get("/models")
def list_models():
    """사용 가능한 파인튜닝 모델 목록 반환"""
    available_models = []
    for m in MODELS:
        adapter_path = MODEL_DIR / f"lora_{m['id']}"
        if adapter_path.exists():
            available_models.append({
                "id": m["id"],
                "name": m["name"],
                "status": "loaded" if current_model_id == m["id"] else "standby"
            })
    return {"models": available_models, "current_loaded": current_model_id}

@app.post("/load")
def load_model(req: LoadRequest):
    global current_model_id, model, tokenizer
    
    model_info = get_model_info(req.model_id)
    if not model_info:
        raise HTTPException(status_code=404, detail="Model not found in config")
        
    adapter_path = MODEL_DIR / f"lora_{req.model_id}"
    if not adapter_path.exists():
        raise HTTPException(status_code=404, detail="LoRA adapter not found. Is training complete?")
        
    if current_model_id == req.model_id:
        return {"status": "success", "message": "Model already loaded"}
        
    # 기존 모델 메모리 해제
    if model is not None:
        print(f"Unloading model {current_model_id} from VRAM...")
        del model
        del tokenizer
        model = None
        tokenizer = None
        torch.cuda.empty_cache()
        gc.collect()
        
    print(f"Loading {req.model_id} into VRAM (16-bit unquantized, SDPA)...")
    try:
        from transformers import BitsAndBytesConfig
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            model_info["repo"], 
            quantization_config=bnb_config,
            device_map={"": 0}, 
            attn_implementation="sdpa",
            trust_remote_code=True
        )
        model = PeftModel.from_pretrained(base_model, str(adapter_path))
        tokenizer = AutoTokenizer.from_pretrained(str(adapter_path), trust_remote_code=True)
        current_model_id = req.model_id
        return {"status": "success", "message": f"{req.model_id} loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# RAG 전역 초기화 (매 요청마다 로드하는 병목 방지)
embedder = None
chroma_client = None
collection = None
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    print("Loading RAG Embedder (BAAI/bge-m3)...")
    embedder = SentenceTransformer("BAAI/bge-m3")
    chroma_client = chromadb.PersistentClient(path=str(DATA_DIR / "chroma_db"))
    collection = chroma_client.get_collection(name="iso9001")
    print("RAG Embedder Loaded!")
except Exception as e:
    print("Failed to initialize RAG components globally:", e)

@app.post("/chat_stream")
def chat_stream(req: ChatRequest):
    global model, tokenizer, current_model_id
    if current_model_id != req.model_id:
        raise HTTPException(status_code=400, detail="Requested model is not loaded. Call /load first.")
        
    if not req.message:
        raise HTTPException(status_code=400, detail="Empty message")
        
    # 1. RAG 기반 문맥 검색
    context = "No context found."
    try:
        if collection and embedder:
            query_emb = embedder.encode(req.message).tolist()
            results = collection.query(query_embeddings=[query_emb], n_results=3)
            
            if results['documents'] and results['documents'][0]:
                context = "\n\n".join(results['documents'][0])
    except Exception as e:
        print("RAG Search Error:", e)
        
    if "gemma" in req.model_id.lower() or "gemma4" in req.model_id.lower():
        messages = [
            {"role": "user", "content": f"You are a helpful and professional ISO 9001 expert assistant. Answer directly in Korean. Do not use internal thoughts or reasoning blocks.\n\nContext:\n{context}\n\nQuestion:\n{req.message}"}
        ]
    else:
        messages = [
            {"role": "system", "content": f"You are a helpful and professional ISO 9001 expert assistant. Answer directly in Korean. Do not use internal thoughts or reasoning blocks.\n\nContext:\n{context}"},
            {"role": "user", "content": req.message}
        ]
    
    try:
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    except ValueError:
        prompt = ""
        for msg in messages:
            prompt += f"<start_of_turn>{msg['role']}\n{msg['content']}<end_of_turn>\n"
        prompt += "<start_of_turn>model\n"
        
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    # eos_token_id 설정
    eos_token_id = tokenizer.eos_token_id
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        tokenizer.convert_tokens_to_ids("<|im_end|>"),
        tokenizer.convert_tokens_to_ids("<end_of_turn>"),
        tokenizer.convert_tokens_to_ids("<|EOT|>"),
        tokenizer.convert_tokens_to_ids("<｜end of sentence｜>"),
        107
    ]
    terminators = [t for t in terminators if t is not None]
            
    import threading
    from transformers import TextIteratorStreamer
    import json
    from fastapi.responses import StreamingResponse
    
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    
    is_deepseek = "deepseek" in req.model_id.lower()
    penalty = 1.15 if is_deepseek else 1.05
    temp = 0.7 if is_deepseek else 0.3
    
    generation_kwargs = dict(
        **inputs, 
        streamer=streamer,
        max_new_tokens=2048,
        do_sample=True,
        temperature=temp,
        top_p=0.9,
        repetition_penalty=penalty,
        pad_token_id=tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id,
        eos_token_id=terminators
    )
    
    def generate_wrapper():
        try:
            with torch.inference_mode():
                model.generate(**generation_kwargs)
        except Exception as e:
            print(f"Generation Thread Error: {e}", flush=True)
            streamer.end()
        finally:
            import gc
            gc.collect()
            torch.cuda.empty_cache()

    thread = threading.Thread(target=generate_wrapper)
    thread.start()
    
    def generate():
        try:
            # 먼저 RAG 문맥 전송
            yield f"data: {json.dumps({'context_used': context})}\n\n"
            
            # 생성되는 토큰 스트리밍
            for new_text in streamer:
                if new_text:
                    yield f"data: {json.dumps({'token': new_text})}\n\n"
                    
            yield "data: [DONE]\n\n"
        finally:
            torch.cuda.empty_cache()
        
    return StreamingResponse(generate(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
