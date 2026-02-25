import streamlit as st
import pandas as pd
from groq import Groq
import base64
from PIL import Image
import io

# --- 1. Page Configuration ---
st.set_page_config(page_title="University of the Holy Quran AI", layout="wide")

# --- 2. Session State Initialization ---
# This part ensures the key is remembered by the system
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

# --- 3. UI Header ---
st.title("🏛️ University of the Holy Quran and Islamic Sciences")
st.subheader("Financial Department - AI Accounting Assistant")
st.markdown("---")

# --- 4. Sidebar for Authentication ---
with st.sidebar:
    st.header("Authentication")
    # Store key in session state directly
    api_key_input = st.text_input("Enter Groq API Key", type="password", value=st.session_state['api_key'])
    
    if api_key_input:
        st.session_state['api_key'] = api_key_input
        st.success("Key accepted! ✅")
    else:
        st.warning("Please enter your API key to activate the system.")

# --- 5. Main Content Logic ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Document Input")
    uploaded_file = st.file_uploader("Upload Invoice or Receipt", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Document Preview", use_container_width=True)

with col2:
    st.header("🤖 AI Analysis")
    # Check if both file and key are present
    if uploaded_file and st.session_state['api_key']:
        if st.button("Start AI Processing"):
            try:
                # Initialize Groq Client using the stored key
                client = Groq(api_key=st.session_state['api_key'])
                
                # Convert Image to Base64
                image_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(image_data).decode('utf-8')

                with st.spinner("AI is analyzing the University document..."):
                    # Groq API Call
                    response = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "As the Accountant for the University of the Holy Quran, extract: Date, Vendor, Total Amount, and Account Entry Explanation."},
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
                st.error(f"Authentication Error: Please check if your API key is valid. (Details: {e})")
    
    elif not st.session_state['api_key']:
        st.info("ℹ️ Enter the API key in the sidebar to enable processing.")

st.markdown("---")
st.caption("© 2026 University of the Holy Quran and Islamic Sciences")
    
