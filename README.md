# AI-First CRM – HCP Interaction Module

## Overview
This project demonstrates an AI-powered CRM module designed for life science field representatives to log interactions with Healthcare Professionals (HCPs).

Users can log interactions through:
1. A structured form
2. An AI assistant that converts natural language into CRM data.

---

## Tech Stack
Frontend: React  
Backend: FastAPI  
AI Processing: Groq API (conceptual LangGraph tools)

---

## Features
• Log interactions with doctors  
• AI assistant converts text into structured CRM data  
• Sentiment detection  
• Follow-up action suggestions  
• Clean CRM-style interface  

---

## Example AI Input

User writes:

Met Dr Sharma and discussed diabetes drug GlucoX.  
Doctor seemed interested.  
Follow up next week.

AI extracts:

Doctor Name: Dr Sharma  
Sentiment: Positive  
Topics: Diabetes drug discussion  
Follow-up: Schedule next meeting

---

## Architecture

User → React Frontend → FastAPI Backend → AI Processing → Structured CRM Data

---

## AI Tools Implemented

1. Log Interaction  
Stores interaction details in the CRM system.

2. Edit Interaction  
Allows modification of interaction data.

3. Search HCP History  
Retrieves previous interactions with doctors.

4. Suggest Follow-up  
AI suggests next engagement steps.

5. Summarize Interaction  
Converts meeting notes into structured CRM fields.