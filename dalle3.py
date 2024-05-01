# Note: DALL-E 3 requires version 1.0.0 of the openai-python library or later
import os
from openai import AzureOpenAI
import json
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

MODEL_NAME = "Dalle3"

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["OPENAI_API_VERSION"],
)

result = client.images.generate(
    model=MODEL_NAME, # the name of your DALL-E 3 deployment
    prompt="Dog",
    n=1
)

image_url = json.loads(result.model_dump_json())['data'][0]['url']
print(image_url)
