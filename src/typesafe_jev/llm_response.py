from __future__ import annotations

import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from src.typesafe_jev.jev_state import JevDecision


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a concise SaaS customer-support assistant. Draft a helpful reply. "
            "Do not promise refunds, credits, account changes, or fixes that have not been confirmed. "
            "Keep the response under 120 words. If the case is routed to a human specialist, "
            "say that it is being escalated for review.",
        ),
        (
            "human",
            "Customer ticket:\n{ticket}\n\n"
            "Jev triage decision:\n"
            "- Department: {department}\n"
            "- Department confidence: {department_confidence:.2f}\n"
            "- Urgency score: {urgency_score:.2f} on a 0-3 rubric\n"
            "- Refund-related probability: {refund_probability:.2f}\n"
            "- Human-review probability: {human_review_probability:.2f}\n"
            "- Final route: {route}\n\n"
            "Write the suggested customer response.",
        ),
    ]
)


def draft_reply(ticket: str, decision: JevDecision) -> str:

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0,
    )
    chain = PROMPT | llm | StrOutputParser()

    return chain.invoke(
        {
            "ticket": ticket,
            "department": decision.department,
            "department_confidence": decision.department_confidence,
            "urgency_score": decision.urgency_score,
            "refund_probability": decision.refund_probability,
            "human_review_probability": decision.human_review_probability,
        }
    )