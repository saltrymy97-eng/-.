import streamlit as st
import pandas as pd
import os
from groq import Groq # Make sure to add 'groq' to requirements.txt
import base64

# 1. Dashboard UI
st.set_page_config(page_title="Amqi Bank AI", layout="wide")
st.title("🏦 Al-Amqi Bank - Groq AI Processor")

# 2. Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    groq_api_key = st.text_input("Enter Groq API Key", type="password")

# 3. Image Processing
uploaded_file = st.file_uploader("Upload Invoice Image", type=['jpg', 'png', 'jpeg'])

if uploaded_file and groq_api_key:
    # Initialize Groq Client
    client = Groq(api_key=groq_api_key)
    
    # Display Image
    st.image(uploaded_file, caption="Processing...", width=400)
    
    if st.button("Generate Accounting Entry"):
        with st.spinner("Groq is analyzing at lightning speed..."):
            # Convert image to base64
            image_content = uploaded_file.getvalue()
            base64_image = base64.b64encode(image_content).decode('utf-8')

            # 4. Call Groq Llama-3 Vision Model
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract Date, Supplier, Total Amount, and suggest Debit/Credit accounts for this invoice at Al-Amqi Bank. Explain why."},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
                model="llama-3.2-11b-vision-preview", # Fast and smart vision model
            )

            # 5. Show Results
            result = chat_completion.choices[0].message.content
            st.success("Analysis Complete!")
            st.markdown("### AI Reasoning & Entry Details:")
            st.info(result)

            # Optional: Download Button for Excel
            st.download_button("Download for Onyx Pro", "CSV Data here", "entry.csv")

elif not groq_api_key:
    st.warning("Please enter your Groq API Key to proceed.")
            
