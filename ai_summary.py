import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(products):
    if not products:
        return "No products found."

    prompt = """Given this list of product data:

Title | Price | Rating | Platform
"""
    for p in products:
        prompt += f"{p['title']} | {p['price']} | {p['rating']} | {p['platform']}\n"
    prompt += "\nGive a short summary of which platform has the best deal and why."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"
