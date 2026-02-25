import streamlit as st
import pandas as pd
from groq import Groq
import base64
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="University of the Holy Quran AI", layout="wide")

# 2. Main Header (University Identity)
st.title("🏛️ University of the Holy Quran and Islamic Sciences")
st.subheader("AI-Powered Financial Accounting System")
st.markdown("---")

# 3. Sidebar for Secure Access
with st.sidebar:
    st.header("Authentication")
    groq_api_key = st.text_input("Enter Groq API Key", type="password", help="Enter your secret xAI or Groq key here.")
    st.divider()
    st.info("System Status: Operational 🟢")
    st.caption("Developed for the University Financial Department")

# 4. Main Interface Logic
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Document Upload")
    uploaded_file = st.file_uploader("Upload Invoice, Receipt, or Voucher", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        # Preview the uploaded document
        image = Image.open(uploaded_file)
        st.image(image, caption="Document Preview", use_container_width=True)

with col2:
    st.header("🤖 AI Financial Analysis")
    
    if uploaded_file and groq_api_key:
        if st.button("Analyze & Generate Entry"):
            try:
                client = Groq(api_key=groq_api_key)
                
                with st.spinner("Analyzing document structure..."):
                    # Encode image to base64
                    image_bytes = uploaded_file.getvalue()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')

                    # Call Groq Llama-3 Vision Model
                    # We tell the AI it's working for the University
                    completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text", 
                                        "text": "You are the AI Accountant for the University of the Holy Quran. "
                                                "Extract the following from this document: "
                                                "1. Date, 2. Vendor/Supplier, 3. Total Amount, "
                                                "4. Suggested Debit/Credit Accounts (based on University fund accounting), "
                                                "5. Professional Explanation of the entry."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                    },
                                ],
                            }
                        ],
                        model="llama-3.2-11b-vision-preview",
                        temperature=0.1 # Low temperature for high accuracy
                    )

                    # Display the AI result
                    analysis_result = completion.choices[0].message.content
                    st.success("Analysis Completed Successfully!")
                    st.markdown("### 📋 Accounting Report")
                    st.write(analysis_result)
                    
                    # Simulated Export to Excel/System
                    st.download_button(
                        label="📥 Export Entry to Excel",
                        data=analysis_result,
                        file_name=f"University_Entry_{uploaded_file.name}.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    elif not groq_api_key:
        st.warning("⚠️ Please enter your API Key in the sidebar to begin.")
    else:
        st.info("Please upload a document to see the analysis.")

# 5. Footer
st.markdown("---")
st.caption("© 2026 University of the Holy Quran and Islamic Sciences | Financial AI Module")
