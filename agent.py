import os
import streamlit as st
from google import genai


@st.cache_resource
def get_agent_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in Streamlit secrets."
        )

    return genai.Client(api_key=api_key)


def run_agent(prompt: str) -> str:

    client = get_agent_client()

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "temperature": 0.7,
            "max_output_tokens": 1000,
        },
    )

    if not response.text:
        return "TASKORA did not receive a response from Gemini."

    return response.text