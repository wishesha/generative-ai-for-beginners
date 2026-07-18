import os
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
load_dotenv()

#validate data inside .env file

# The Responses API is served from the Azure OpenAI (Microsoft Foundry) v1 endpoint,
# so we point the OpenAI client at <your-endpoint>/openai/v1/ (no api_version needed).
endpoint = os.environ['AZURE_OPENAI_ENDPOINT']
client = OpenAI(
  api_key=os.environ['AZURE_OPENAI_API_KEY'],
  base_url=f"{endpoint.rstrip('/')}/openai/v1/",
  )

# Select the deployment name configured in your .env file
model = os.environ['AZURE_OPENAI_DEPLOYMENT']

def search_local_data(prompt):
    context = []
    with open("07-building-chat-applications/python/f1_data.txt") as file:
        for line in file:
            words = prompt.lower().split()
            for word in words:
                if len(word) > 2:
                    if word in line.lower():
                        context.append(line.strip())
                        break
    return "\n".join(context)

print("Chatbot active, type 'quit' to exit\n")

while True:
    prompt = input("Your Prompt: ")
    if prompt.lower() == "quit":
        break
    
    local_context = search_local_data(prompt)

    system_instructions = "You are an strict Formula 1 assistant. You must only answer the user's question " \
    "using the data and information provided in the 'Verified Local Data section below. If the answer cannot be found " \
    "entirely using the data given, answer simply with 'Answer cannot be found using local data.'"
    response = client.responses.create(
        model=model,
        input = [{"role":"system", "content":"You are a helpful assistant."},
               {"role":"user","content":prompt},],
        store=False,)        
    print(f"AI: {response.output_text}\n")