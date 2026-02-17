import streamlit as st
from groq import Groq
from PIL import Image
import pytesseract
import os

# --- 1. CORE API CONFIGURATION ---
try:
    # Ensure GROQ_API_KEY is a single continuous line in Streamlit Secrets
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = "LOCAL_TEST_KEY" 

client = Groq(api_key=API_KEY)

# --- 2. THE ACCOUNTING PLAY INTERFACE ---
st.set_page_config(
    page_title="The Accounting Play | U of HQIS", 
    page_icon="🎭", 
    layout="wide"
)

# Professional University Styling
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { 
        background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%); 
        color: white; border-radius: 8px; height: 3.5em; font-weight: bold; border: none; width: 100%;
    }
    .stHeader { color: #1e3a8a; font-family: 'Segoe UI', sans-serif; }
    .audit-card { padding: 25px; border-radius: 15px; background-color: white; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎭 The Accounting Play")
st.subheader("University of the Holy Quran and Islamic Sciences")
st.markdown("---")

# --- 3. WORKFLOW ---
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown("<h3 class='stHeader'>📁 Step 1: Document Ingestion</h3>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Invoice/Receipt Image", type=['png', 'jpg', 'jpeg'])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Document for Audit", use_container_width=True)
        
        with st.spinner("🔍 Extracting Metadata..."):
            try:
                # OCR Logic
                raw_data = pytesseract.image_to_string(img)
                st.success("Data Synchronized Successfully.")
            except:
                raw_data = "Manual Audit Mode: Information extracted from student input."

with right_col:
    st.markdown("<h3 class='stHeader'>📜 Step 2: Journal Entry Simulation</h3>", unsafe_allow_html=True)
    if uploaded_file:
        with st.container():
            st.markdown("<div class='audit-card'>", unsafe_allow_html=True)
            
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                dr_acc = st.text_input("Debit Account (Dr):")
            with row1_col2:
                cr_acc = st.text_input("Credit Account (Cr):")
                
            val = st.number_input("Transaction Value:", min_value=0.0)
            justification = st.text_area("Accounting Rationale:", placeholder="Explain the entry logic...")
            
            if st.button("🚀 RUN AI AUDIT"):
                if not dr_acc or not cr_acc:
                    st.error("Protocol Error: Missing Account Titles.")
                else:
                    sys_msg = "You are a Chief Auditor evaluating university accounting students."
                    user_msg = f"Invoiced Text: {raw_data}\nStudent Entry: Dr {dr_acc} / Cr {cr_acc}\nAmount: {val}\nLogic: {justification}"
                    
                    with st.spinner("AI Auditor is reviewing..."):
                        try:
                            # Using the specific stable model for 2026 deployments
                            response = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": sys_msg},
                                    {"role": "user", "content": user_msg}
                                ],
                                model="llama-3.3-70b-versatile", 
                            )
                            st.markdown("### 📝 Auditor's Final Report:")
                            st.info(response.choices[0].message.content)
                            st.balloons()
                        except Exception as error:
                            st.error(f"System Audit Error: {str(error)}")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("System Ready. Please upload a document to begin the simulation.")

# --- 4. FOOTER ---
st.markdown("---")
st.caption("Developed by: Saleem Al-Tureimi | Accounting Representative & AI Specialist")
    
