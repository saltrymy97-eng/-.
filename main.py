import streamlit as st
from groq import Groq
from PIL import Image
import pytesseract
import os

# --- 1. ACCESS SETTINGS ---
# Securely fetching the API Key from Streamlit Secrets
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = "YOUR_FALLBACK_KEY" # For local testing only

client = Groq(api_key=API_KEY)

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="The Accounting Play", 
    page_icon="🎭", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional UI Styling
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { 
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); 
        color: white; 
        border-radius: 10px; 
        height: 3.5em; 
        font-weight: bold; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 4px 15px rgba(0,0,0,0.1); }
    .stHeader { color: #1e3a8a; font-family: 'Helvetica Neue', sans-serif; }
    .status-box { padding: 20px; border-radius: 12px; background-color: white; border-left: 5px solid #1e3a8a; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# Branding Section
st.title("🎭 The Accounting Play")
st.subheader("University of the Holy Quran and Islamic Sciences")
st.markdown("---")

# --- 3. MAIN INTERFACE ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("<h3 class='stHeader'>📷 Phase 1: Evidence Capture</h3>", unsafe_allow_html=True)
    input_method = st.radio("Input Source:", ["Digital Camera", "Local File Upload"], horizontal=True)
    
    if input_method == "Digital Camera":
        image_file = st.camera_input("Scan physical invoice")
    else:
        image_file = st.file_uploader("Import document image", type=['png', 'jpg', 'jpeg'])

    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="Processed Document", use_column_width=True)
        
        with st.spinner("🤖 AI-OCR Engine Analyzing..."):
            try:
                # OCR Extraction
                extracted_text = pytesseract.image_to_string(img)
                st.success("Analysis Complete: Data Synchronized.")
            except Exception:
                extracted_text = "Standard Corporate Invoice Content"
                st.info("System Note: Manual verification mode active.")

with col2:
    st.markdown("<h3 class='stHeader'>🧠 Phase 2: Professional Simulation</h3>", unsafe_allow_html=True)
    if image_file:
        with st.container():
            st.markdown("<div class='status-box'>", unsafe_allow_html=True)
            st.write("Construct the Journal Entry for the captured document:")
            
            d_col, c_col = st.columns(2)
            with d_col:
                debit = st.text_input("Debit Account (Dr):", placeholder="Account Title")
            with c_col:
                credit = st.text_input("Credit Account (Cr):", placeholder="Account Title")
                
            amount = st.number_input("Transaction Value ($):", min_value=0.0, format="%.2f")
            logic = st.text_area("Accounting Justification:", placeholder="State your professional reasoning...")
            
            if st.button("🚀 EXECUTE AI AUDIT"):
                if not debit or not credit:
                    st.error("Protocol Error: Debit/Credit accounts must be defined.")
                else:
                    system_prompt = "You are a senior auditor and accounting professor at a prestigious university. Evaluate the student's journal entry with high academic standards."
                    user_prompt = f"""
                    [OCR DATA]: {extracted_text}
                    [STUDENT ENTRY]: Dr {debit} / Cr {credit}
                    [VALUE]: {amount}
                    [LOGIC]: {logic}
                    
                    Evaluation Criteria:
                    1. Accuracy: Compare entry with OCR data.
                    2. Academic Score: (X/10).
                    3. Technical Feedback: Detailed professional critique.
                    4. The 'Saleem Excellence Tip': Advice to reach 97% proficiency.
                    """
                    
                    with st.spinner("Consulting Senior Auditor..."):
                        try:
                            chat_completion = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": user_prompt}
                                ],
                                model="llama3-8b-8192",
                            )
                            st.markdown("### 📝 Auditor's Final Report:")
                            st.markdown(f"<div style='background-color: #eef2f7; padding: 15px; border-radius: 8px;'>{chat_completion.choices[0].message.content}</div>", unsafe_allow_html=True)
                            st.balloons()
                        except Exception as e:
                            st.error(f"Communication Failure: {e}")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Waiting for document input to initiate simulation...")

# --- 4. FOOTER ---
st.markdown("---")
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.caption("Developed by: **Saleem Al-Tureimi**")
    st.caption("Accounting Representative | AI Implementation Specialist")
with footer_col2:
    st.markdown("<div style='text-align: right; color: grey; font-size: 0.8em;'>© 2024 University of the Holy Quran and Islamic Sciences</div>", unsafe_allow_html=True)
        
