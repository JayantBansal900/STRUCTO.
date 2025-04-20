# bots/knowledge_bot.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_knowledge_response(question: str) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_KNOWLEDGE_KEY')}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",  # You can use other models like "anthropic/claude-3-haiku" or "mistralai/mixtral-8x7b"
            "messages": [
                {"role": "user", "content": question}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Error: {str(e)}"
