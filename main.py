from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Инициализация FastAPI
app = FastAPI()

# Пустой ответ для Render (чтобы не падал)
@app.get("/", include_in_schema=False)
def root():
    return {"status": "OK"}

@app.head("/", include_in_schema=False)
def root_head():
    return

# Модель запроса
class CleanRequest(BaseModel):
    name: str
    website: str = ""

# Конфигурация Gemini (замени на свой ключ)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat_session = model.start_chat()

# Основной роут
@app.post("/clean-name")
async def clean_name(request: CleanRequest):
    message = f"Исходное название: {request.name}\tСайт: {request.website}\tОчищенное название:"
    
    print("🟢 Incoming request:", message)

    response = chat_session.send_message(message)

    print("🧠 Gemini response:", response.text)

    return {"cleaned": response.text.strip()}
