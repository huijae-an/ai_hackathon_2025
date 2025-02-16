from openai import OpenAI
from app.config import OPENAI_API_KEY, DEFAULT_OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

# Make sure to install openai via pip (in requirements.txt)

def openai_chat_completion(prompt):
    """
    A simple wrapper to call OpenAI GPT (chat-completion).
    We return the 'content' from the first choice.
    """

    # We can call the ChatCompletion endpoint if we want the chat style:
    response = client.chat.completions.create(model=DEFAULT_OPENAI_MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.85,
    max_tokens=500)

    return response.choices[0].message.content
