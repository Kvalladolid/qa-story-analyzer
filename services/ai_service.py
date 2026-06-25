import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from config.prompts import QA_PROMPT

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_story(story):

    # Reemplaza el marcador <<STORY>> por la historia del usuario
    prompt = QA_PROMPT.replace(
        "<<STORY>>",
        story
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )