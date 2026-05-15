import streamlit as st
from PIL import Image
import requests
import io
import base64

st.set_page_config(
    page_title="Grok ICT Institutional Audit Pro",
    page_icon="🏛️",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .stApp { background-color: #0B0F19; color: white; }
    .result-box {
        background: #131722; 
        border-left: 5px solid #00ff9d;
        border-radius: 12px; 
        padding: 20px; 
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏛️ Grok ICT Institutional Audit Pro")
st.caption("Powered by Grok (xAI) • Smart Money Concept & ICT Methodology")
st.markdown("---")

with st.sidebar:
    st.header("🔑 Settings")
    api_key = st.text_input("xAI API Key", type="password")
    pair = st.text_input("Pair", value="XAUUSD")
    tf = st.selectbox("Timeframe", ["M5", "M15", "H1", "H4", "D1", "W1"])
    mode = st.selectbox("Mode Analisa", [
        "Full Institutional Audit",
        "Entry Setup Presisi",
        "Market Structure + Bias"
    ])

uploaded_files = st.file_uploader(
    "📸 Upload Chart Screenshot", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        st.image(file, use_column_width=True)

    if st.button("🚀 Analisa dengan Grok", type="primary", use_container_width=True):
        if not api_key:
            st.error("❌ Masukkan xAI API Key di sidebar!")
            st.stop()

        with st.spinner("Grok sedang menganalisa chart..."):
            try:
                # Prepare images
                images = []
                for file in uploaded_files:
                    img = Image.open(file)
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG", quality=85)
                    b64 = base64.b64encode(buf.getvalue()).decode()
                    images.append(b64)

                prompt = f"""Kamu adalah Grok ICT Institutional Auditor Pro.
Analisa chart ini secara profesional menggunakan Smart Money Concept dan ICT Methodology.

Pair: {pair}
Timeframe: {tf}
Mode: {mode}

Berikan analisa dalam Bahasa Indonesia yang jelas dan actionable dengan format:
1. **Market Structure**
2. **Bias Saat Ini** (Bullish/Bearish)
3. **Key Levels** (Order Block, FVG, Liquidity, BOS/CHOCH)
4. **Trading Setup** (Entry, SL, TP1, TP2)
5. **Risk Management**
6. **Kesimpulan**"""

                url = "https://api.x.ai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                content = [{"type": "text", "text": prompt}]
                for b64_img in images:
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64_img}"}
                    })

                data = {
                    "model": "grok-2-vision-latest",   # Model terbaik saat ini
                    "messages": [{"role": "user", "content": content}],
                    "max_tokens": 1800,
                    "temperature": 0.7
                }

                response = requests.post(url, headers=headers, json=data, timeout=60)

                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    st.success("✅ Analisa Selesai!")
                    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Error {response.status_code}: {response.text[:300]}")

            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")

st.caption("Grok ICT Pro • Febrin")
