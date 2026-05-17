import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# 1. Page Configuration & Professional Theme
st.set_page_config(
    page_title="ExamParser AI - Smart PDF to Excel Converter", 
    page_icon="💼", 
    layout="wide"
)

# Custom CSS for Professional SaaS UI
st.markdown("""
    <style>
    .main-title { font-size: 40px; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 10px; }
    .sub-title { font-size: 18px; color: #4B5563; text-align: center; margin-bottom: 30px; }
    .feature-box { background-color: #F3F4F6; padding: 20px; border-radius: 10px; border-left: 5px solid #1E3A8A; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🚀 ExamParser AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced AI-Powered PDF Content Ingestion Platform. Convert your exam PDFs (Hindi, English, or Bilingual) into database-ready Excel/CSV sheets instantly.</div>', unsafe_allow_html=True)

# 2. Enterprise Console Sidebar Setup
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2618/2618580.png", width=100)
st.sidebar.markdown("### 🏢 Enterprise Console")
st.sidebar.write("This tool reduces data entry costs by 90% for coaching institutes and test series publishers.")

st.sidebar.write("---")
# Security Activation via Gemini API Key
api_key = st.sidebar.text_input("Enterprise Activation (Enter Gemini API Key):", type="password")
st.sidebar.write("---")
st.sidebar.info("🤖 Powered by Gemini 1.5 Pro - Enterprise Tier")

if api_key:
    genai.configure(api_key=api_key)
    
    # Main Workspace split into two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ 1. Configure Settings")
        exam_name = st.text_input("Exam Name (e.g., SSC CGL 2026, UPSC 2026)", placeholder="UPSC 2026")
        target_subject = st.text_input("Default Subject (If single subject PDF)", placeholder="History")
        
        # Dropdown to guide AI on script/language
        language_mode = st.selectbox(
            "Select Question Language Mode:",
            ["Bilingual (Hindi + English)", "Pure English", "Pure Hindi (Devanagari)"]
        )
        
        st.write("")
        st.markdown("<div class='feature-box'><b>💡 Enterprise Benefit:</b> Zero manual typing errors, 10x faster ingestion, and direct Firebase-compatible structural output.</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### 📁 2. Upload Source File")
        uploaded_file = st.file_uploader("Upload Answer Key or Question Paper (PDF Format)", type=["pdf"])
        
        if uploaded_file is not None and exam_name:
            st.success(f"✓ {uploaded_file.name} is ready for processing.")
            
            if st.button("Start AI Data Extraction ⚡", use_container_width=True):
                with st.spinner("AI Engine is parsing the PDF... Please wait 10-30 seconds."):
                    try:
                        bytes_data = uploaded_file.read()
                        
                        # Master Enterprise Prompt supporting multi-language processing
                        prompt = f"""
                        You are a premium enterprise data parser for educational institutions.
                        Analyze the attached exam PDF and extract all questions with extreme structural accuracy.
                        
                        Language Mode Context: The questions in the PDF are in {language_mode}. 
                        If Bilingual, capture both Hindi and English texts perfectly inside the Question_Text and Options fields.
                        If Pure Hindi, keep the text strictly in Devanagari script.
                        
                        Strict Format Rule: Return ONLY a valid JSON array of objects. Do not wrap it inside markdown blocks like ```json ... 
```. Just return raw JSON text output.
                        
                        Each JSON object must follow this template perfectly:
                        {{
                            "Subject": "{target_subject if target_subject else 'Extract automatically from question context'}",
                            "Topic": "Identify the sub-topic automatically",
                            "Exam_Name": "{exam_name}",
                            "Question_Text": "The complete question text exactly as given in the PDF",
                            "Option_A": "Text for Option A",
                            "Option_B": "Text for Option B",
                            "Option_C": "Text for Option C",
                            "Option_D": "Text for Option D",
                            "Correct_Answer": "Strictly single character 'A', 'B', 'C', or 'D'"
                        }}
                        """
                        
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        response = model.generate_content([
                            {'mime_type': 'application/pdf', 'data': bytes_data},
                            prompt
                        ])
                        
                        # Clean and validate response text
                        clean_text = response.text.strip()
                        clean_text = clean_text.replace("```json", "").replace("```", "").strip()
                            
                        data_json = json.loads(clean_text)
                        df = pd.DataFrame(data_json)
                        
                        st.markdown("### 📊 3. Extracted Data Preview (Client Review)")
                        st.dataframe(df, use_container_width=True)
                        
                        # Dynamic CSV Generation and Download Button
                        csv_data = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Your Database-Ready CSV/Excel Sheet",
                            data=csv_data,
                            file_name=f"{exam_name.lower().replace(' ', '_')}_database.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                    except Exception as e:
                        st.error(f"System Error: {e}")
        elif not exam_name and uploaded_file:
            st.warning("⚠️ Please enter the 'Exam Name' before starting AI extraction.")
else:
    st.info("👋 Welcome to ExamParser AI. Please enter your Gemini API Key in the sidebar to activate this commercial console.")
