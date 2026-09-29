import os
from pathlib import Path
from datetime import datetime

import streamlit as st
from google import genai
from google.genai import types


# ============================================================
# TASKORA AI - CLOUD IMAGE GENERATOR
# ============================================================
# Uses Gemini Image Generation API
#
# Works with:
#   - Local development
#   - Streamlit Community Cloud
#
# API key:
#   - Streamlit Cloud -> st.secrets["GEMINI_API_KEY"]
#   - Local development -> GEMINI_API_KEY environment variable
#
# ============================================================


# ------------------------------------------------------------
# GEMINI IMAGE MODEL
# ------------------------------------------------------------

MODEL_NAME = "gemini-3.1-flash-image"


# ------------------------------------------------------------
# GET API KEY
# ------------------------------------------------------------

def get_api_key():
    """
    Get Gemini API key.

    Priority:
    1. Streamlit Secrets
    2. Environment variable
    """

    # --------------------------------------------------------
    # Streamlit Cloud
    # --------------------------------------------------------

    try:
        if "GEMINI_API_KEY" in st.secrets:

            key = st.secrets["GEMINI_API_KEY"]

            if key:
                return str(key).strip()

    except Exception:
        pass

    # --------------------------------------------------------
    # Local development
    # --------------------------------------------------------

    key = os.getenv("GEMINI_API_KEY")

    if key:
        return key.strip()

    return None


# ------------------------------------------------------------
# CREATE GEMINI CLIENT
# ------------------------------------------------------------

def get_client():
    """
    Create and return Gemini API client.
    """

    api_key = get_api_key()

    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured.\n\n"
            "For Streamlit Cloud:\n"
            "Add GEMINI_API_KEY to Streamlit Secrets.\n\n"
            "For local development:\n"
            "Set the GEMINI_API_KEY environment variable."
        )

    return genai.Client(
        api_key=api_key
    )


# ------------------------------------------------------------
# GENERATE IMAGE
# ------------------------------------------------------------

def generate_image(prompt):
    """
    Generate an image from a text prompt.

    Returns:
        str: Path to generated PNG image.
    """

    # --------------------------------------------------------
    # Validate prompt
    # --------------------------------------------------------

    if not prompt or not prompt.strip():

        raise ValueError(
            "Please enter an image description."
        )

    prompt = prompt.strip()

    # --------------------------------------------------------
    # Create Gemini client
    # --------------------------------------------------------

    client = get_client()

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    base_dir = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    generated_dir = (
        base_dir
        / "generated"
        / "images"
    )

    generated_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Generate image
    # --------------------------------------------------------

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"]
        )
    )

    # --------------------------------------------------------
    # Extract generated image
    # --------------------------------------------------------

    image_data = None

    if response.parts:

        for part in response.parts:

            # Gemini image response
            if getattr(part, "inline_data", None):

                image_data = part.inline_data.data

                if image_data:
                    break

    # --------------------------------------------------------
    # Make sure an image was returned
    # --------------------------------------------------------

    if image_data is None:

        raise RuntimeError(
            "Gemini did not return an image.\n\n"
            "The API request completed, but no image "
            "data was returned.\n\n"
            "Please try a different prompt."
        )

    # --------------------------------------------------------
    # Create unique filename
    # --------------------------------------------------------

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    image_path = (
        generated_dir
        / f"taskora_image_{timestamp}.png"
    )

    # --------------------------------------------------------
    # Save image
    # --------------------------------------------------------

    with open(
        image_path,
        "wb"
    ) as file:

        file.write(image_data)

    return str(image_path)


# ------------------------------------------------------------
# TEST FUNCTION
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("TASKORA AI - IMAGE GENERATOR TEST")
    print("=" * 60)

    print()
    print(f"Model: {MODEL_NAME}")
    print()

    test_prompt = (
        "A futuristic AI assistant helping a college student "
        "organize tasks in a modern digital workspace, "
        "purple and blue neon lighting, cinematic lighting, "
        "highly detailed, professional digital art"
    )

    try:

        result = generate_image(
            test_prompt
        )

        print()
        print("SUCCESS!")
        print()
        print("Image created:")
        print(result)

    except Exception as error:

        print()
        print("IMAGE GENERATION FAILED")
        print()
        print("Error:")
        print(error)