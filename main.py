import base64
import requests
import pandas as pd

# 1. Setup Grok API Key
API_KEY = "YOUR_GROK_API_KEY"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ask_grok(image_path):
    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # The Prompt: Telling Grok to act as an Accountant at Al-Amqi Bank
    prompt_text = (
        "You are a professional accountant at Al-Amqi Bank. "
        "Analyze this invoice image and return a JSON object with: "
        "1. Date, 2. Supplier Name, 3. Total Amount, "
        "4. Debit Account, 5. Credit Account, "
        "6. Explanation (Why you chose this entry)."
    )

    payload = {
        "model": "grok-1.5-vision-preview", # Update to the latest vision model
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "temperature": 0
    }

    response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# --- Execution ---
# result = ask_grok("invoice_001.jpg")
# print(result)
