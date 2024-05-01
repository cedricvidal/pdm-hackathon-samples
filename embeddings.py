import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

MODEL_NAME = "text-embedding-ada-002"

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["OPENAI_API_VERSION"],
)

MESSAGES = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {
        "role": "assistant",
        "content": "The Los Angeles Dodgers won the World Series in 2020.",
    },
    {"role": "user", "content": "Where was it played?"},
]

def generate_embeddings(text, model=MODEL_NAME): # model = "deployment_name"
    return client.embeddings.create(input = [text], model=model).data[0].embedding

print(generate_embeddings("Hello Azure OpenAI"))
