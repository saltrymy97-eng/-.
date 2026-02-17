import streamlit as st
from groq import Groq
from PIL import Image
import pytesseract
import os

# --- 1. ACCESS SETTINGS ---
# Using the API Key you provided
API_KEY = "Gsk_2o12G2zbRRwemdSJBalJWGdyb3FYzlEqMKuNjEDlkuoOxy5zWIIe"
client = Groq(api_key=API_KEY)

# --- 2. OCR ENGINE CONFIGURATION (For Windows Users) ---
# If you are on Windows, uncomment the line below and point it to your Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- 3. PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Accounting Mentor", page_icon="🤖", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #007bff; color: white; border-radius: 5px; width: 100%; }
    .stHeader { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Accounting Mentor | Saleem's Workshop")
st.markdown("---")

# --- 4. MAIN INTERFACE ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("📸 Step 1: Document Capture")
    input_method = st.radio("Choose input method:", ["Camera", "Upload Image File"])
    
    if input_method == "Camera":
        image_file = st.camera_input("Take a photo of the real invoice")
    else:
        image_file = st.file_uploader("Upload invoice image", type=['png', 'jpg', 'jpeg'])

    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="Captured Invoice", width=400)
        
        with st.spinner("🔍 Extracting data from image..."):
            try:
                # Extract text using OCR
                extracted_text = pytesseract.image_to_string(img)
                st.success("Data extracted successfully!")
                with st.expander("View Extracted Text (OCR Metadata)"):
                    st.write(extracted_text)
            except Exception as e:
                st.error(f"OCR Error: {e}. Make sure Tesseract OCR is installed on your system.")
                extracted_text = "No text extracted."

with col2:
    st.header("🧠 Step 2: Professional Analysis")
    if image_file:
        st.write("Record the accounting entry based on the invoice above:")
        
        debit = st.text_input("Debit Account (Dr):", placeholder="e.g., Cash or Purchases")
        credit = st.text_input("Credit Account (Cr):", placeholder="e.g., Sales or Accounts Payable")
        amount = st.number_input("Transaction Amount:", min_value=0.0)
        logic = st.text_area("Explain your accounting logic:", placeholder="Why did you choose these accounts?")
        
        if st.button("Verify with AI Mentor"):
            if not debit or not credit:
                st.warning("Please enter both Debit and Credit accounts.")
            else:
                # Constructing the Prompt for Groq
                system_prompt = "You are a senior accounting professor and mentor. You are professional, precise, and encouraging. Your goal is to evaluate students based on real invoices."
                user_prompt = f"""
                Invoice Data Extracted: {extracted_text}
                Student's Entry: {debit} (Debit), {credit} (Credit), for the amount of {amount}.
                Student's Reasoning: {logic}
                
                Task:
                1. Is the entry correct based on the invoice? Provide the correct entry if it's wrong.
                2. Score the student's performance out of 10.
                3. Analyze their strengths and weaknesses (e.g., understanding of assets, timing of revenue, etc.).
                4. Give one professional 'Saleem Tip' to help them reach a 97% grade.
                Respond in professional English.
                """
                
                with st.spinner("AI Mentor is analyzing your entry..."):
                    try:
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_prompt}
                            ],
                            model="llama3-8b-8192", # Ultra-fast model for live workshops
                        )
                        st.divider()
                        st.subheader("📝 Mentor's Feedback:")
                        st.write(chat_completion.choices[0].message.content)
                        st.balloons()
                    except Exception as e:
                        st.error(f"Groq API Error: {e}")
    else:
        st.info("Awaiting invoice capture to begin simulation...")

# --- 5. FOOTER ---
st.markdown("---")
st.caption("Developed by: Saleem Al-Tureimi | Accounting Representative | AI Specialist")
        
