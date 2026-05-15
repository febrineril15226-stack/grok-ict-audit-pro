import streamlit as st
from PIL import Image
import requests
import io
import base64
from datetime import datetime

st.set_page_config(
    page_title="Grok ICT Institutional Audit Pro",
    page_icon="🏛️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0B0F19; color: white; }
    .result-box {
        background: #131722; 
        border-left: 5px solid #00ff9d;
        border-radius: 12px; 
        padding: 25px; 
        margin: 15px 0;
    }
    .signal-buy { background: #0d2b1a; color: #00ff9d; padding: 18px; border-radius: 10px; font-size: 1.3rem; text-align: center; font-weight: bold; }
    .signal-sell { background: #2b0d0d; color: #ff4d4d; padding: 18px; border-radius: 10px; font-size: 1.3rem; text-align: center; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🏛️ Grok ICT Institutional Audit Pro")
st.caption("Powered by Grok (xAI) • Smart Money Concept & ICT Methodology")
st.markdown("---")

with st.sidebar:
    st.header("🔑 Settings")
    xai_api_key = st.text_input("xAI API Key", type="password", value="")
    pair = st.text_input("Pair", value="XAUUSD")
    tf = st.selectbox("Timeframe", ["M15", "H1", "H4", "D1", "W1"])
    mode = st.selectbox("Mode Analisa", [
        "Full Institutional Audit",
        "Entry Setup Presisi",
        "Market Structure + Bias",
        "Liquidity & Order Block"
    ])

uploaded_files = st.file_uploader("📸 Upload Chart Screenshot", 
                                 type=["png", "jpg", "jpeg"], 
                                 accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.image(Image.open(file), caption=file.name, use_column_width=True)

    if st.button("🚀 Analisa dengan Grok", type="primary", use_container_width=True):
        if not xai_api_key:
            st.error("❌ Masukkan xAI API Key di sidebar!")
            st.stop()

        with st.spinner("Grok sedang menganalisa chart..."):
            try:
                images_data = []
                for file in uploaded_files:
                    img = Image.open(file)
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=85)
                    img_bytes = buf.getvalue()
                    images_data.append(base64.b64encode(img_bytes).decode())

                prompt = f"""Anda adalah Grok ICT Institutional Auditor Pro.
Analisis chart ini menggunakan Smart Money Concept dan ICT Methodology secara mendalam.

Pair: {pair} | Timeframe: {tf} | Mode: {mode}

Berikan analisa dalam Bahasa Indonesia dengan struktur:
1. Market Structure
2. Bias Saat Ini
3. Key Levels (OB, FVG, Liquidity)
4. Trading Setup (Entry, SL, TP)
5. Risk Management
6. Kesimpulan"""

                url = "https://api.x.ai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {xai_api_key}",
                    "Content-Type": "application/json"
                }

                content = [{"type": "text", "text": prompt}]
                for b64 in images_data:
                    content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})

                payload = {
                    "model": "grok-2-vision-latest",
                    "messages": [{"role": "user", "content": content}],
                    "max_tokens": 1800,
                    "temperature": 0.7
                }

                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    st.success("✅ Analisa Selesai!")
                    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error: {response.status_code}")

            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")

st.caption("Grok ICT Pro • Febrin")
