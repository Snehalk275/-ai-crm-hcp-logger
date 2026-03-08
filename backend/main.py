from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import json

# ---- Put your Groq API key here ----
client = Groq(api_key="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")

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Interaction(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Backend running successfully"}


@app.post("/ai-log")
def ai_log(interaction: Interaction):

    prompt = f"""
You are a CRM assistant.

Extract the following information from the interaction text:

hcpName
interactionType
topics
sentiment
followUp

Respond ONLY with valid JSON.

Example:

{{
"hcpName": "Dr Sharma",
"interactionType": "Meeting",
"topics": "discussion about diabetes drug",
"sentiment": "Positive",
"followUp": "Follow up next week"
}}

Text:
{interaction.text}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result = completion.choices[0].message.content

    # Convert AI response to JSON
    try:
        data = json.loads(result)
    except:
        data = {
            "hcpName": "Unknown",
            "interactionType": "Meeting",
            "topics": interaction.text,
            "sentiment": "Neutral",
            "followUp": ""
        }

    return data