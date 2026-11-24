from dataclasses import dataclass
import os
import httpx
from dotenv import load_dotenv
import json
from langchain_ollama import ChatOllama

load_dotenv()  # reads your .env filepython-dotenv

@dataclass
class JevDecision:
    department: str
    department_confidence: float
    urgency_score: float
    urgency_confidence: float
    refund_probability: float
    human_review_probability: float
    model: str | None = None

def analyze_ticket(ticket):
    # 1. Get the settings
    api_key = os.getenv("TYPESAFE_API_KEY")
    model = os.getenv("TYPESAFE_MODEL", "jev-latest")
    url = "https://api.typesafe.ai/v1/systemone"

    if not api_key:
        raise RuntimeError("Add TYPESAFE_API_KEY to your .env file")

    # 2. Build the request: the text to judge + the questions to ask
    payload = {
        "model": llm,
        "state": f"Customer support triage.\nCustomer ticket: {ticket}",
        "questions": {
            "department": {
                "type": "choice",
                "instructions": "Which support team should own this ticket?",
                "criteria": {
                    "billing": "Charges, invoices, payments, refunds",
                    "technical": "Bugs, errors, login failures",
                    "account": "Profile, access, permissions",
                    "general": "Anything else",
                },
            },
            "urgency": {
                "type": "score",
                "instructions": "How urgent is this request?",
                "criteria": [
                    "Low: no time pressure",
                    "Medium: customer is inconvenienced",
                    "High: business impact",
                    "Critical: severe ongoing impact",
                ],
            },
            "refund_related": {
                "type": "noul",
                "instructions": "The customer is asking about a refund.",
            },
            "human_review": {
                "type": "noul",
                "instructions": "A human should review this before any automated action.",
            },
        },
    }

    # 3. Send it
    headers = {"Authorization": f"Bearer {api_key}"}
    response = httpx.post(url, headers=headers, json=payload, timeout=30)

    if response.status_code >= 400:
        raise RuntimeError(f"Error {response.status_code}: {response.text}")

    # 4. Read the answers
    answers = response.json()["answers"]

    return {
        "department": answers["department"]["choice"],
        "department_confidence": answers["department"]["confidence"],
        "urgency": answers["urgency"]["score"],
        "refund_probability": answers["refund_related"]["noul"],
        "human_review_probability": answers["human_review"]["noul"],
    }


if __name__ == "__main__":
    result = analyze_ticket("I was charged twice and I want my money back today!")
    print(result)