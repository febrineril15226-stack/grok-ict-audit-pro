import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="ICT Audit Pro", layout="wide", page_icon="🏛️")

st.title("🏛️ ICT Institutional Audit Pro")
st.caption("Powered by Gemini 1.5 Flash • Gratis")

with st.sidebar:
    st.header("Settings")
    gemini_key = st.text_input("Gemini API Key", type="password")
    pair = st.text_input("Pair", value="EURUSD")
    tf = st.selectbox("Timeframe", ["M15", "H1", "H4", "D1"])
    mode = st.selectbox("Mode Analisa", ["Full Audit", "Entry Setup"])

uploaded_files = st.file_uploader("📸 Upload Chart Screenshot", 
                                 type=["png", "jpg", "jpeg"], 
                                 accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.image(file, use_column_width=True)

    if st.button("🚀 Analisa dengan Gemini", type="primary"):
        if not gemini_key:
            st.error("Masukkan Gemini API Key!")
            st.stop()

        with st.spinner("Gemini sedang menganalisa chart..."):
            try:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')

                prompt = f"""Kamu adalah expert ICT dan Smart Money Concept.
Analisa chart forex ini secara mendalam dan profesional.

Pair: {pair}
Timeframe: {tf}
Mode: {mode}

Jawab dalam Bahasa Indonesia dengan struktur jelas:
1. Market Structure
2. Bias Saat Ini
3. Key Levels Penting
4. Trading Setup (Entry, SL, TP)
5. Risk Management
6. Kesimpulan"""

                images = [Image.open(f) for f in uploaded_files]
                
                response = model.generate_content([prompt] + images)
                result = response.text

                st.success("✅ Analisa Selesai!")
                st.markdown(result)

            except Exception as e:
                st.error(f"Error: {str(e)}")

st.caption("Versi Gratis - ICT Pro")
