from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=GEMINI_API_KEY)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="Your name is Luke Shawket, a sarcastic AI clone..."
            ),
            contents=[types.Content(parts=[types.Part(text=user_input)])]
        )

        # Safely extract reply
        reply = (
            response.candidates[0].content.parts[0].text
            if response.candidates and response.candidates[0].content.parts
            else "Luke is speechless. Try again."
        )

    except Exception as e:
        print("Gemini error:", e)
        reply = "Luke crashed. Probably your fault."

    return {"reply": reply}