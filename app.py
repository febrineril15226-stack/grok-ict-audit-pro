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

st.title("🏛️ Grok ICT Institutional Audit Pro")
st.caption("Powered by Grok (xAI) • Smart Money Concept & ICT Methodology")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("xAI API Key", type="password")
    pair = st.text_input("Pair", value="XAUUSD")
    tf = st.selectbox("Timeframe", ["M5", "M15", "H1", "H4", "D1"])
    mode = st.selectbox("Mode Analisa", ["Full Institutional Audit", "Entry Setup"])

uploaded_files = st.file_uploader("Upload Chart Screenshot", 
                                 type=["png", "jpg", "jpeg"], 
                                 accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.image(file, use_column_width=True)

    if st.button("🚀 Analisa dengan Grok", type="primary"):
        if not api_key:
            st.error("Masukkan xAI API Key!")
            st.stop()

        with st.spinner("Grok sedang menganalisa chart..."):
            try:
                # Prepare image
                images = []
                for file in uploaded_files:
                    img = Image.open(file)
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG")
                    b64 = base64.b64encode(buf.getvalue()).decode()
                    images.append(b64)

                prompt = f"""Kamu adalah Grok ICT Institutional Auditor Pro.
Analisa chart berikut menggunakan ICT dan Smart Money Concept.

Pair: {pair}
Timeframe: {tf}
Mode: {mode}

Berikan analisa lengkap dalam Bahasa Indonesia:
- Market Structure
- Bias
- Key Levels (Order Block, FVG, Liquidity)
- Trading Setup
- Risk Management"""

                url = "https://api.x.ai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                content = [{"type": "text", "text": prompt}]
                for img_b64 in images:
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
                    })

                data = {
                    "model": "grok-2-vision-1212",   # Model yang lebih stabil
                    "messages": [{"role": "user", "content": content}],
                    "max_tokens": 1500,
                    "temperature": 0.7
                }

                response = requests.post(url, headers=headers, json=data, timeout=60)
                
                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    st.success("✅ Analisa Selesai")
                    st.markdown(result)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")

st.caption("Grok ICT Pro • Febrin")
