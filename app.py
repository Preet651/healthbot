from fastapi import FastAPI
from pydantic import BaseModel
import json, re

app = FastAPI()

with open("data/health_data.json") as f:
    KB = json.load(f)

class Message(BaseModel):
    message: str

def find_symptom(text):
    text = text.lower()
    for key, v in KB.items():
        for kw in v.get("keywords", []) + [key]:
            if re.search(r"\b" + re.escape(kw) + r"\b", text):
                return key
    return None

@app.post("/chat")
async def chat(msg: Message):
    text = msg.message

    if any(word in text.lower() for word in ["chest pain","unconscious","breathing difficulty","severe bleeding"]):
        return {"response":"Emergency symptoms detected. Seek immediate medical attention."}

    sym = find_symptom(text)
    if not sym:
        return {"response":"I couldn't identify a symptom. Please describe in simple words."}

    entry = KB[sym]

    return {
        "symptom": sym,
        "causes": entry["causes"],
        "precautions": entry["precautions"],
        "prevention": entry["prevention"],
        "home_remedies": entry["home_remedies"],
        "disclaimer": "This is general advice, not a medical diagnosis."
    }
