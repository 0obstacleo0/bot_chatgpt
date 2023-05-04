import openai
import os

openai.api_key = os.environ["API_KEY"]


def inquire_gpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
    )
    return response["choices"][0]["message"]["content"]
