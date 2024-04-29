# Example: reuse your existing OpenAI setup
from openai import OpenAI



def ai_response(message) :
  # Message example:
  # messages=[
  #     {"role": "system", "content": "Always answer in rhymes."},
  #     {"role": "user", "content": "Tell me a joke about data scientists."}
  #   ],

  # Point to the local server
  client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

  # response = input("What would you like translated? ")

  completion = client.chat.completions.create(
    model="TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
    messages=message,
    temperature=0.7,
  )
  return completion.choices[0].message.content