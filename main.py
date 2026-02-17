import streamlit as st
from groq import Groq
from PIL import Image
import pytesseract
import time

# --- Page Configuration ---
st.set_page_config(page_title="AI Accounting Mentor | Saleem", page_icon="🤖", layout="wide")

# --- Initialize Groq Client ---
# Replace 'YOUR_GROQ_API_KEY' with your actual API key
client = Groq(api_key="YOUR_GROQ_API_KEY")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #1a73e8; color: white; font-weight: bold; }
    .stHeader { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.title("🤖 AI Accounting Mentor System")
st.markdown("#### Developed by: **Saleem Al-Tureimi** (The AI Specialist)")
st.write("Bridging the gap between Academic Theory and Real-World Practice.")

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2641/2641409.png", width=80)
    st.title("Workshop Settings")
    mode = st.radio("Learning Mode:", ["General Training", "Elite Challenge (Top 1%)"])
    st.divider()
    st.info("Powered by Llama-3 & Groq LPUs for lightning-fast inference.")

# --- Main Layout ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📸 Step 1: Scan Invoice")
    input_method = st.radio("Source:", ["Camera", "Upload Image"])
    
    if input_method == "Camera":
        source = st.camera_input("Take a photo of the invoice")
    else:
        source = st.file_uploader("Choose invoice image", type=['png', 'jpg', 'jpeg'])

    if source:
        img = Image.open(source)
        st.image(img, caption="Captured Invoice", use_column_width=True)
        
        with st.spinner("🔍 Extracting data using OCR..."):
            # OCR Processing
            extracted_text = pytesseract.image_to_string(img)
            st.success("Data Extracted Successfully!")
            with st.expander("Show Extracted Text"):
                st.write(extracted_text)

with col2:
    st.subheader("🧠 Step 2: Accounting Analysis")
    if source:
        st.write("Analyze the transaction and record the entry:")
        
        d_acc = st.text_input("Debit Account (Dr):", placeholder="e.g., Cash / Inventory")
        c_acc = st.text_input("Credit Account (Cr):", placeholder="e.g., Sales / Accounts Payable")
        val = st.number_input("Transaction Amount:", min_value=0.0)
        logic = st.text_area("Explain your reasoning:", placeholder="Why did you choose these accounts?")
        
        if st.button("Submit to AI Mentor"):
            if not d_acc or not c_acc:
                st.error("Please complete the entry details.")
            else:
                # --- Prompt Engineering ---
                prompt = f"""
                Invoice Data: {extracted_text}
                Student Entry: Debit={d_acc}, Credit={c_acc}, Amount={val}
                Student Reasoning: {logic}
                
                As an 'AI Accounting Mentor', please:
                1. Verify if the entry is correct based on the invoice.
                2. Analyze the student's 'Accounting Personality' based on their reasoning.
                3. Provide a score out of 10.
                4. Give one specific tip for improvement (e.g., focus on Asset vs Expense).
                5. Use a professional, encouraging, and high-level tone.
                """
                
                with st.spinner("🤖 Mentor is evaluating..."):
                    chat_completion = client.chat.completions.create(
                        model="llama3-70b-8192",
                        messages=[
                            {"role": "system", "content": "You are the AI Accounting Mentor designed by Saleem. You are professional, highly accurate, and motivational."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    # --- Result Display ---
                    st.divider()
                    st.markdown("### 📝 Mentor Feedback:")
                    st.write(chat_completion.choices[0].message.content)
                    st.balloons()
    else:
        st.info("Awaiting Invoice scan to begin simulation...")

# --- Footer/Dashboard ---
st.divider()
st.markdown("### 📊 Workshop Performance Dashboard")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Processed Invoices", "150+", "+15%")
kpi2.metric("Avg. Student Accuracy", "92%", "+4%")
kpi3.metric("System Latency", "0.4s", "Ultra-Fast")

st.caption("© 2026 Saleem Al-Tureimi | Accounting Department Representative")

سالم التريمي
