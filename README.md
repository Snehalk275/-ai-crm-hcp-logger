# AI-Powered CRM HCP Interaction Logger

## Overview

This project is an AI-powered CRM interaction logging system designed for healthcare sales representatives.  
The system allows users to log interactions with healthcare professionals (HCPs) either through a structured form or using a conversational AI interface.

The AI agent automatically extracts structured information such as doctor name, interaction type, topics discussed, sentiment, and follow-up actions from natural language text.

---

## Tech Stack

Frontend:
- React
- Redux

Backend:
- Python
- FastAPI

AI Agent Framework:
- LangGraph

LLM:
- Groq LLM (llama-3.3-70b-versatile)

Database:
- MySQL

Font:
- Google Inter

---

## System Architecture

User → React Frontend → FastAPI Backend → LangGraph Agent → Groq LLM → MySQL Database

---

## Features

- Log HCP interactions using structured form
- Conversational AI assistant for interaction logging
- Automatic extraction of interaction details
- Sentiment analysis of doctor feedback
- Follow-up action suggestions
- Edit previously logged interactions
- MySQL database storage

---

## LangGraph AI Tools

The AI agent uses multiple tools to process interaction text:

1. Extract HCP Name  
2. Detect Interaction Type  
3. Extract Discussion Topics  
4. Sentiment Analysis  
5. Follow-up Recommendation

These tools run sequentially in a LangGraph workflow.

---

## API Endpoints

### POST /ai-log
Processes interaction text using the AI agent and stores structured data.

Example request:

```json
{
"text": "Met Dr Sharma today. He liked the diabetes drug and asked for samples."
}
