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
