from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.typesafe_jev.jev_state import analyze_ticket
from src.typesafe_jev.llm_response import draft_reply

app=FastAPI(title="Typesafe Jev API", description="API for Typesafe Jev", version="1.0.0")

class TicketRequest(BaseModel):
    ticket: str

@app.post("/response")
def predict(data:TicketRequest):

    answer=analyze_ticket(data.ticket)
    reply=draft_reply(data.ticket, answer)
    return JSONResponse(status_code=200, content={"department":answer.department, "urgency_score":answer.urgency_score, "refund_probability":answer.refund_probability, "human_review_probability":answer.human_review_probability, "reply":reply})