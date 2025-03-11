from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Инициализация FastAPI
app = FastAPI()

# ✅ Добавлен GET / и HEAD /, чтобы Render не давал 404
@app.get("/", include_in_schema=False)
def root():
    return {"status": "API is alive"}

@app.head("/", include_in_schema=False)
def root_head():
    return

# 🔹 Модель запроса
class CleanRequest(BaseModel):
    name: str
    website: str = ""

# 🔹 Подключение Gemini API (замени на свой ключ в Render Variables)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat_session = model.start_chat()

# 🔹 Основной эндпоинт
@app.post("/clean-name")
async def clean_name(request: CleanRequest):
    message = f"Исходное название: {request.name}\tСайт: {request.website}\tОчищенное название:"
    
    print("🟢 Incoming request:", message)

    response = chat_session.send_message(message)

    print("🧠 Gemini response:", response.text)

    return {"cleaned": response.text.strip()}
