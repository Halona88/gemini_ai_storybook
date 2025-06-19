from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API key 입력
api_key = "AIzaSyDHVpmobppxKAbBH8wpwsUrSSYrymJ0XC4"
client = genai.Client(api_key=api_key)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
@app.head("/")
def root():
    return{"message": "서버가 정상 작동 중입니다"}

@app.post("/generate")
async def generate_image(req: PromptRequest):
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=req.prompt,
        config=types.GenerateContentConfig(response_modalities=["TEXT","IMAGE"])
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            b64 = base64.b64encode(part.inline_data.data).decode("utf-8")
            return {"image_base64": b64}
    return {"error": "No image returned"}

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import base64

# FastAPI 앱 선언
app = FastAPI()

# CORS 설정: 외부 접근 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (보안 설정이 필요하면 제한 가능)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google Gemini API 키 등록
api_key = "AIzaSyDHVpmobppxKAbBH8wpwsUrSSYrymJ0XC4"
client = genai.Client(api_key=api_key)

# POST 요청 시 사용할 데이터 모델 정의
class PromptRequest(BaseModel):
    prompt: str

# 루트 경로 응답 (브라우저 GET 확인용)
@app.get("/")
@app.head("/")
def root():
    return {"message": "서버가 정상 작동 중입니다."}

# POST 요청 - 실제 이미지 생성 처리
@app.post("/generate")
async def generate_image(req: PromptRequest):
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=req.prompt,
        config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
    )
    # 이미지 응답 처리
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            b64 = base64.b64encode(part.inline_data.data).decode("utf-8")
            return {"image_base64": b64}
    return {"error": "No image returned"}

# GET 요청 - 테스트용 안내 메시지
@app.get("/generate")
def generate_get():
    return {
        "message": "이 엔드포인트는 POST 방식으로만 이미지를 생성할 수 있습니다. POST 요청을 보내주세요.",
        "사용예시": {
            "method": "POST",
            "url": "/generate",
            "body": {
                "prompt": "A futuristic robot walking through a neon city"
            }
        }
    }
