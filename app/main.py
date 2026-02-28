from fastapi import FastAPI
from .gmail_service import authenticate_gmail, fetch_latest_email
from .agent import process_email
from .memory import store_email

app = FastAPI()

@app.get("/run-agent")
def run_agent():

    service = authenticate_gmail()
    email = fetch_latest_email(service)

    if not email:
        return {"message": "No email found"}

    summary, reply = process_email(email)

    store_email(email, summary, reply)

    return {
        "summary": summary,
        "suggested_reply": reply
    }
