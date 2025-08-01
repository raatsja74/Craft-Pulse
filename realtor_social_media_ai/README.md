# Realtor Social Media AI Backend

This example FastAPI project implements basic endpoints for a real estate focused content engine.

## Features
- **User profile setup** with five onboarding questions.
- **AI content generation** via OpenAI.
- **Scheduling** posts up to 60 days in advance using APScheduler.

## Running
```bash
pip install -r requirements.txt
uvicorn realtor_social_media_ai.app.main:app --reload
```
