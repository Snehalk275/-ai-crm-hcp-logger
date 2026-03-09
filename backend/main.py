from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from langgraph.graph import StateGraph, END
from typing import TypedDict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import json

DATABASE_URL = "mysql+mysqlconnector://root:snehalk275@localhost/crm_ai"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Groq client
client = Groq(api_key="YOUR_GROQ_API")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class InteractionDB(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcpName = Column(String(255))
    interactionType = Column(String(255))
    topics = Column(String(500))
    sentiment = Column(String(100))
    followUp = Column(String(500))

Base.metadata.create_all(bind=engine)

class Interaction(BaseModel):
    text: str

class EditInteraction(BaseModel):
    id: int
    hcpName: str
    interactionType: str
    topics: str
    sentiment: str
    followUp: str

# Graph state
class AgentState(TypedDict):
    text: str
    hcpName: str
    interactionType: str
    topics: str
    sentiment: str
    followUp: str


# -------------------------
# TOOL 1: Extract HCP Name
# -------------------------

def extract_hcp(state: AgentState):
    text = state["text"]

    prompt = f"""
Extract the doctor's name from the text.

Text:
{text}

Return only the doctor's name.
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    state["hcpName"] = completion.choices[0].message.content.strip()

    return state

@app.put("/edit-interaction")
def edit_interaction(data: EditInteraction):

    db = SessionLocal()

    interaction = db.query(InteractionDB).filter(InteractionDB.id == data.id).first()

    if not interaction:
        return {"error": "Interaction not found"}

    interaction.hcpName = data.hcpName
    interaction.interactionType = data.interactionType
    interaction.topics = data.topics
    interaction.sentiment = data.sentiment
    interaction.followUp = data.followUp

    db.commit()

    return {"message": "Interaction updated successfully"}
# -------------------------
# TOOL 2: Detect interaction type
# -------------------------

def detect_interaction(state: AgentState):

    text = state["text"]

    prompt = f"""
Determine the interaction type.

Options:
Meeting
Call
Email

Text:
{text}

Return only one word.
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    state["interactionType"] = completion.choices[0].message.content.strip()

    return state


# -------------------------
# TOOL 3: Extract topics
# -------------------------

def extract_topics(state: AgentState):

    text = state["text"]

    prompt = f"""
Summarize the main topic discussed in this interaction.

Text:
{text}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    state["topics"] = completion.choices[0].message.content.strip()

    return state


# -------------------------
# TOOL 4: Sentiment analysis
# -------------------------

def analyze_sentiment(state: AgentState):

    text = state["text"]

    prompt = f"""
Analyze the doctor's sentiment.

Options:
Positive
Neutral
Negative

Text:
{text}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    state["sentiment"] = completion.choices[0].message.content.strip()

    return state


# -------------------------
# TOOL 5: Follow up suggestion
# -------------------------

def follow_up(state: AgentState):

    text = state["text"]

    prompt = f"""
Suggest a follow-up action based on the interaction.

Text:
{text}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    state["followUp"] = completion.choices[0].message.content.strip()

    return state


# -------------------------
# Build LangGraph
# -------------------------

workflow = StateGraph(AgentState)

workflow.add_node("extract_hcp", extract_hcp)
workflow.add_node("detect_interaction", detect_interaction)
workflow.add_node("extract_topics", extract_topics)
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("follow_up", follow_up)

workflow.set_entry_point("extract_hcp")

workflow.add_edge("extract_hcp", "detect_interaction")
workflow.add_edge("detect_interaction", "extract_topics")
workflow.add_edge("extract_topics", "analyze_sentiment")
workflow.add_edge("analyze_sentiment", "follow_up")
workflow.add_edge("follow_up", END)

graph = workflow.compile()

# API endpoint
@app.post("/ai-log")
def ai_log(interaction: Interaction):

    result = graph.invoke({
        "text": interaction.text,
        "hcpName": "",
        "interactionType": "",
        "topics": "",
        "sentiment": "",
        "followUp": ""
    })
    
    db = SessionLocal()

    interaction_record = InteractionDB(
        hcpName=result["hcpName"],
        interactionType=result["interactionType"],
        topics=result["topics"],
        sentiment=result["sentiment"],
        followUp=result["followUp"]
    )

    db.add(interaction_record)
    db.commit()
    db.close()

    return result


@app.get("/")
def home():
    return {"message": "LangGraph CRM Agent Running"}