import streamlit as st
import pandas as pd
from groq import Groq
import base64
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="University of the Holy Quran AI", layout="wide")

# 2. Session State: This is the fix! 
# It keeps the API key stored even if the page reloads or is translated.
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

# 3. Header
st.title("🏛️ University of the Holy Quran and Islamic Sciences")
st.subheader("Financial Department - AI Accounting Assistant")
st.markdown("---")

# 4. Sidebar: Authentication
with st.sidebar:
    st.header("Authentication")
    # We use a temporary variable to capture input
    temp_key = st.text_input("Enter Groq API Key", type="password", value=st.session_state['api_key'])
    
    # Update session state only if a new key is entered
    if temp_key:
        st.session_state['api_key'] = temp_key
        st.success("API Key Locked ✅")
    else:
        st.warning("Key Required 🔑")

# 5. Main Content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Document Input")
    uploaded_file = st.file_uploader("Upload Invoice/Receipt", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        st.image(uploaded_file, caption="Preview", use_container_width=True)

with col2:
    st.header("🤖 AI Analysis")
    
    # Only run if both File and Key exist in memory
    if uploaded_file and st.session_state['api_key']:
        if st.button("Run Financial Analysis"):
            try:
                client = Groq(api_key=st.session_state['api_key'])
                
                # Process image
                image_bytes = uploaded_file.getvalue()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')

                with st.spinner("University AI is processing..."):
                    response = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Extract: Date, Vendor, Total, and Accounting Entry for this University document."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                ]
                            }
                        ],
                        model="llama-3.2-11b-vision-preview",
                    )
                    
                    st.success("Done!")
                    st.markdown("### 📊 Accounting Report")
                    st.info(response.choices[0].message.content)
            
            except Exception as e:
                st.error(f"Error: {e}")
                
    elif not st.session_state['api_key']:
        st.error("⚠️ Authentication Missing: Please enter the API key in the sidebar.")
    else:
        st.info("💡 Ready: Please upload a document to begin.")

st.markdown("---")
st.caption("© 2026 University of the Holy Quran and Islamic Sciences | Financial Module")
        
