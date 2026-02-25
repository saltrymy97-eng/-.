import streamlit as st
import pandas as pd
from groq import Groq
import base64
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="University of the Holy Quran AI", layout="wide")

# 2. Connection Bridge (Session State)
# This ensures the API key stays linked and doesn't reset
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ""

# 3. Main Header (University Identity)
st.title("🏛️ University of the Holy Quran and Islamic Sciences")
st.subheader("AI-Powered Financial Accounting System")
st.markdown("---")

# 4. Sidebar for Secure Access
with st.sidebar:
    st.header("Authentication")
    # Capturing the key and locking it into the session memory
    user_input = st.text_input("Enter Groq API Key", type="password", value=st.session_state['api_key'])
    
    if user_input:
        st.session_state['api_key'] = user_input
        st.success("Connection Linked! ✅")
    else:
        st.warning("Key Required to Start 🔑")
    
    st.divider()
    st.info("Authorized Personnel Only")

# 5. Document Processing Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Document Upload")
    uploaded_file = st.file_uploader("Upload Invoice, Receipt, or Voucher", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Document Preview", use_container_width=True)

with col2:
    st.header("🤖 AI Financial Analysis")
    
    # Checking if the system is linked to the key and a file is present
    if uploaded_file and st.session_state['api_key']:
        if st.button("Process & Generate Entry"):
            try:
                client = Groq(api_key=st.session_state['api_key'])
                
                with st.spinner("Analyzing document for the University..."):
                    # Encode image
                    image_bytes = uploaded_file.getvalue()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')

                    # Call Groq Llama-3 Vision Model
                    completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text", 
                                        "text": "Analyze this document for the University's accounting department. Extract the Date, Vendor, Total Amount, and provide a professional Accounting Entry explanation."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                    },
                                ],
                            }
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )

                    st.success("Analysis Complete!")
                    st.markdown("### 📋 Accounting Report")
                    st.info(completion.choices[0].message.content)
            
            except Exception as e:
                st.error(f"Link Error: {str(e)}")
    
    elif not st.session_state['api_key']:
        st.error("⚠️ Authentication Missing: Please enter the API key in the sidebar and press Enter.")
    else:
        st.info("Ready: Please upload a document to begin the analysis.")

# 6. Footer
st.markdown("---")
st.caption("© 2026 University of the Holy Quran and Islamic Sciences | Financial AI Module")
                 
