import streamlit as st
import pandas as pd
from groq import Groq
import base64
from PIL import Image
import io

# --- Page Setup ---
st.set_page_config(page_title="University of the Holy Quran AI", layout="wide")

# --- UI Header ---
st.title("🏛️ University of the Holy Quran and Islamic Sciences")
st.subheader("Financial Department - AI Accounting Assistant")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Enter Groq API Key", type="password")
    st.info("System Version: 2.0 (Latest Groq Model)")
    st.caption("Secure Connection: SSL Active")

# --- Main Layout ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Document Input")
    uploaded_file = st.file_uploader("Upload Invoice or Receipt", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Document Preview", use_container_width=True)

with col2:
    st.header("🤖 AI Analysis")
    if uploaded_file and api_key:
        if st.button("Start AI Processing"):
            try:
                # Initialize Client
                client = Groq(api_key=api_key)
                
                # Convert Image to Base64
                image_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(image_data).decode('utf-8')

                with st.spinner("AI is analyzing the University document..."):
                    # Groq API Call (Using Llama 3.2 Vision)
                    response = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "As the University Accountant, extract the date, vendor, total amount, and explain the accounting entry for this document."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                    
                    # Display Results
                    st.success("Analysis Complete!")
                    st.markdown("### 📋 Financial Report")
                    st.write(response.choices[0].message.content)
            
            except Exception as e:
                st.error(f"Error: {e}")
    elif not api_key:
        st.warning("Please enter your API Key in the sidebar.")

st.markdown("---")
st.caption("© 2026 University of the Holy Quran and Islamic Sciences")
