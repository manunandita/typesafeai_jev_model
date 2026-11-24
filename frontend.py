import streamlit as st
from dotenv import load_dotenv
import requests

API_URL="http://127.0.0.1:8000/response"

from src.typesafe_jev.jev_state import analyze_ticket

load_dotenv()

st.title("Support Ticket Analyzer")

ticket = st.text_area("Enter the customer ticket")

if st.button("Analyze"):
    if not ticket.strip():
        st.warning("Please type a ticket first.")
    else:
        with st.spinner("Working..."):
            data = {"ticket": ticket}
            try:
                response = requests.post(API_URL, json=data)
                d = response.json()
                
                if response.status_code == 200:
                    st.subheader("Analysis Result")
                    st.write("**Team:**", d["department"])
                    st.write("**Urgency:**", round(d["urgency_score"], 2))
                    st.write("**Refund request:**", "Yes" if d["refund_probability"] >= 0.5 else "No")
                    st.write("**Human review:**", "Yes" if d["human_review_probability"] >= 0.6 else "No")
            
                    st.subheader("Suggested Response")
                    st.info(d["reply"])
                else:
                    st.error(f"API Error: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")