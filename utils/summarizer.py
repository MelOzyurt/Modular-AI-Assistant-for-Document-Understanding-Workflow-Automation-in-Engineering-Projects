# utils/summarizer.py

import os
import openai

# Load API key from environment variable (set this in Streamlit secrets or your environment)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(text: str) -> str:
    """
    Generate a summary of the input text using OpenAI GPT model.

    Args:
        text (str): The raw text to summarize.

    Returns:
        str: The generated summary text.
    """
    if not text.strip():
        return "No text provided to summarize."

    prompt = f"Please provide a concise summary for the following document:\n\n{text}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300,
        )
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"Error generating summary: {e}"
