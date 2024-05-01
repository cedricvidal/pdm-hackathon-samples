import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

load_dotenv()  # take environment variables from .env.

MODEL_NAME = "gpt-35-turbo"

def get_current_weather(location, unit = "fahrenheit"):
    """
    Hard coded function that always returns the same temperature
    Replace by an API call
    """
    return "70"

functions = [
     {
      "name": "get_current_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
          }
        },
        "required": ["location"]
      }
    } 
  ]

available_functions = {
    "get_current_weather": get_current_weather,
}

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["OPENAI_API_VERSION"],
)

def run_conversation(content):
  messages = [
    {"role": "user", "content": content},
    ]
  # Step 1: send the conversation and available functions to GPT
  response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages,
    functions=functions
  )
  response_message = response.choices[0].message

  # extend conversation with assistant's reply
  if(response_message.content):
    messages.append({
        "role": response_message.role,
        "content": response_message.content
        })

  # Step 2: check if GPT wanted to call a function
  while response_message.function_call:
    # Step 3: call the function
    # Note: the JSON response may not always be valid; be sure to handle errors
    function_name = response_message.function_call.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(response_message.function_call.arguments)
    function_response = function_to_call(**function_args)

    # Step 4: send the info on the function call and function response to GPT
    # extend conversation with function response
    messages.append({ "role": "function", "name": function_name, "content": function_response })

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
    )  # get a new response from GPT where it can see the function response
    response_message = response.choices[0].message
    if(response_message.content):
        messages.append({
            "role": response_message.role,
            "content": response_message.content
            })

  for message in messages:
    if "content" in message:
      print(message["role"] + ": " + message["content"])
    if "function_call" in message:
      print(" -> calling function " + message.function_call.name + " with arguments " + json.dumps(message.function_call.arguments))

run_conversation("What is the weather like in Boston?")
