import streamlit as st
import pandas as pd
import base64
import requests
from PIL import Image
import io

# 1. Page Configuration
st.set_page_config(page_title="Al-Amqi AI Accountant", layout="wide")

st.title("🏦 Al-Amqi Bank: AI Invoice Processor")
st.markdown("---")

# 2. Sidebar for API Key (Security Best Practice)
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Grok API Key", type="password")
    st.info("The data stays within the local network and Grok's secure API.")

# 3. Image Encoding Function
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# 4. Grok Vision Integration
def analyze_with_grok(image_base64, key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    
    prompt = """
    Act as a senior accountant at Al-Amqi Bank. Analyze this invoice and extract:
    1. Date of invoice.
    2. Supplier name.
    3. Total amount.
    4. Debit Account (e.g., Fuel, Stationery, Utilities).
    5. Credit Account (usually Cash or Accounts Payable).
    6. Reasoning: Briefly explain why you chose these accounts.
    Return the result in a clean format.
    """

    payload = {
        "model": "grok-1.5-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
    }

    response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.text}"

# 5. Main UI Logic
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload Invoice")
    uploaded_file = st.file_uploader("Drop invoice image here (JPG, PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Document", use_column_width=True)

with col2:
    st.subheader("🤖 AI Accounting Analysis")
    if uploaded_file and api_key:
        if st.button("Analyze with Grok"):
            with st.spinner("Grok is thinking..."):
                # Process image
                img_b64 = encode_image(uploaded_file)
                # Get AI result
                result = analyze_with_grok(img_b64, api_key)
                st.markdown(result)
                
                # Option to Export (Simulated)
                st.download_button("📥 Export to Excel (Onyx Ready)", 
                                   data="Sample Data", 
                                   file_name="entry.csv")
    elif not api_key:
        st.warning("Please enter the API Key in the sidebar to start.")

