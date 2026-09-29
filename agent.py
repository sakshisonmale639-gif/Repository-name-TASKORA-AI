import os
import streamlit as st
import google.generativeai as genai

@st.cache_resource
def get_agent_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment secrets.")
    
    genai.configure(api_key=api_key)
    # Use gemini-1.5-flash for significantly faster responses and lower memory footprint
    return genai.GenerativeModel("gemini-1.5-flash")

def run_agent(prompt: str) -> str:
    model = get_agent_model()
    
    # Stream the output or generate directly
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 1000,  # Cap response length to avoid timeouts
        }
    )
    return response.text