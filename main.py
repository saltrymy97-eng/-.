import streamlit as st
from groq import Groq
from PIL import Image
import pytesseract

# --- 1. CORE CONFIGURATION ---
try:
    # Ensure your Secret key in Streamlit is a single line
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    API_KEY = "YOUR_LOCAL_KEY"

client = Groq(api_key=API_KEY)

# --- 2. PAGE SETTINGS ---
st.set_page_config(
    page_title="The Accounting Play | AI Auditor", 
    page_icon="🎭", 
    layout="wide"
)

# Professional Styling
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { 
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); 
        color: white; border-radius: 10px; height: 3.5em; font-weight: bold; width: 100%;
    }
    .audit-section { padding: 20px; border-radius: 15px; background-color: white; border-left: 5px solid #1e3a8a; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .tutor-note { background-color: #f0fdf4; border-left: 5px solid #16a34a; padding: 15px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎭 The Accounting Play")
st.subheader("University of the Holy Quran and Islamic Sciences")
st.info("Interactive AI Auditor & Academic Tutor Simulation")

# --- 3. INPUT PHASE ---
col_img, col_form = st.columns([1, 1.5], gap="large")

with col_img:
    st.markdown("### 📷 Phase 1: Document Capture")
    uploaded_file = st.file_uploader("Upload Invoice/Receipt", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Evidence Document", use_container_width=True)
        try:
            # OCR Extraction
            extracted_data = pytesseract.image_to_string(img)
        except:
            extracted_data = "Manual Audit Mode Active"

with col_form:
    st.markdown("### 📜 Phase 2: Multi-Entry Simulation")
    if uploaded_file:
        # State management for multiple rows
        if 'entry_rows' not in st.session_state:
            st.session_state.entry_rows = 1
        
        journal_entries = []
        
        with st.container():
            st.markdown("<div class='audit-section'>", unsafe_allow_html=True)
            for i in range(st.session_state.entry_rows):
                st.markdown(f"**Journal Entry Line #{i+1}**")
                r_col1, r_col2, r_col3 = st.columns([2, 2, 1])
                with r_col1:
                    dr = st.text_input(f"Debit (Dr) Account", key=f"dr_{i}", placeholder="e.g. Office Equipment")
                with r_col2:
                    cr = st.text_input(f"Credit (Cr) Account", key=f"cr_{i}", placeholder="e.g. Cash")
                with r_col3:
                    val = st.number_input(f"Amount", key=f"val_{i}", min_value=0.0, step=0.01)
                journal_entries.append({"Line": i+1, "Debit": dr, "Credit": cr, "Amount": val})
            
            # Buttons to add/remove rows
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button("➕ Add Entry Line"):
                    st.session_state.entry_rows += 1
                    st.rerun()
            with b_col2:
                if st.button("🗑️ Reset Rows") and st.session_state.entry_rows > 1:
                    st.session_state.entry_rows = 1
                    st.rerun()

            logic = st.text_area("Accounting Rationale:", placeholder="Explain your professional reasoning here...")
            
            if st.button("🚀 INITIATE AI AUDIT & TUTORING"):
                # Comprehensive System Prompt for Tutoring & Auditing
                system_prompt = """
                You are a Senior University Professor and Chief Auditor. 
                Your role is to:
                1. Audit the student's journal entries against the uploaded invoice data.
                2. If the entries are incorrect, provide the correct Standard Journal Entry.
                3. EVALUATE: Provide a score out of 10.
                4. TUTOR: Explain the 'Why'. If the student made a mistake, teach them the specific accounting principle (e.g., Matching Principle, Revenue Recognition, etc.).
                5. Encourage the student and provide one 'Saleem Excellence Tip'.
                6. Use professional, academic, yet supportive English.
                """
                
                student_submission = f"""
                Invoice Metadata: {extracted_data}
                Student Entries: {journal_entries}
                Student Logic: {logic}
                """
                
                with st.spinner("Auditor is reviewing and preparing the lesson..."):
                    try:
                        response = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": student_submission}
                            ],
                            model="llama-3.3-70b-versatile",
                        )
                        st.markdown("### 📝 Auditor's Feedback & Academic Lesson")
                        st.success(response.choices[0].message.content)
                        st.balloons()
                    except Exception as e:
                        st.error(f"System Error: {str(e)}")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Please upload a document to start the professional simulation.")

# --- 4. FOOTER ---
st.markdown("---")
st.caption("Developed by: Saleem Al-Tureimi | AI Accounting Implementation")
