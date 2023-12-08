from openai import OpenAI
import os


def get_llm_response(model: str, content: str) -> str:
    client = OpenAI(base_url=os.getenv('LLM_URL'), api_key=os.getenv('API_KEY'))

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": content},
        ],
        max_tokens=512,
    )

    return completion.choices[0].message.content
    