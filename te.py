import requests
import json
API_KEY = "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"
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {API_KEY} ",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "mistralai/mistral-small-3.1-24b-instruct:free",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "What is in this image?"
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
            }
          }
        ]
      }
    ],
    
  })
)

# Print response
print("Status Code:", response.status_code)
try:
    response_data = response.json()
    print(json.dumps(response_data, indent=4))
except json.JSONDecodeError:
    print("Invalid JSON response:", response.text)