import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv('NVIDIA_API_KEY')

)

def model_1_1(context):

    completion = client.chat.completions.create(
        model="meta/llama-3.1-405b-instruct",
        messages=[
                    {"role": "system", "content": 'user will provide a inappropriate/hate-speech sentence and you need to convert it into the good positive version, which is just one sentence long. Make sure the same pronoun is preserved.'},
                    {"role": "user", "content": context}
        ],
        temperature=0,
        top_p=1,
        max_tokens=100,
    )
    result = completion.choices[0].message.content

    return result

def model_1_2(context):
    completion = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[
                    {"role": "system", "content": 'user will provide a inappropriate/hate-speech sentence and you need to convert it into the good positive version, which is just one sentence long. Make sure the same pronoun is preserved.I do not want any other context, just give me the positive version.'},
                    {"role": "user", "content": context}
        ],
        temperature=0,
        top_p=1,
        max_tokens=100,
    )
    result = completion.choices[0].message.content

    return result

def model_2_1(context):
    completion = client.chat.completions.create(
        model="ibm/granite-3.0-8b-instruct",
        messages=[
                    {"role": "system", "content": 'You summarize the content provided by the user into a very short paragraph.'},
                    {"role": "user", "content": context}
        ],
        temperature=0,
        top_p=0.7,
        max_tokens=100,
    )
    result = completion.choices[0].message.content

    return result

def model_2_2(context):
    completion = client.chat.completions.create(
        model="google/gemma-2b",
        messages=[
                    {"role": "system", "content": 'You summarize the content provided by the user into a very short paragraph.'},
                    {"role": "user", "content": context}
        ],
        temperature=0,
        top_p=0.7,
        max_tokens=100
    )
    result = completion.choices[0].message.content
    
    return result