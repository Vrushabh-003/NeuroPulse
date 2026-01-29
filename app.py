import streamlit as st
import joblib
import numpy as np

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="NeuroPulse",
    page_icon="🧠",
    layout="centered"
)

# --------------------------------------------------
# CLEANED PREMIUM iOS CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* Dynamic Abstract Background */
html, body, [data-testid="stAppViewContainer"] {
    background-image: 
        linear-gradient(rgba(11, 15, 23, 0.8), rgba(11, 15, 23, 0.8)),
        url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop');
    background-size: cover;
    background-attachment: scroll;
    font-family: 'Inter', sans-serif;
}

/* Glass Card Component */
.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    border-radius: 24px;
    padding: 26px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 20px 45px rgba(0,0,0,0.55);
    margin-bottom: 26px;
}

/* Tightened Input Card */
.input-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

.title {
    font-size: 40px;
    font-weight: 700;
    color: white;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #9ba3af;
    font-size: 15px;
    margin-top: 6px;
}

.meter-container {
    display: flex;
    justify-content: center;
    margin-top: 26px;
}

.circle {
    width: 170px;
    height: 170px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: smoothFill 1.8s ease-out;
    box-shadow: 0 0 35px rgba(255,255,255,0.15);
}

.pulse {
    animation: pulseGlow 1.6s infinite;
}

.inner-circle {
    width: 135px;
    height: 135px;
    background: rgba(0,0,0,0.78);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 24px;
    font-weight: 700;
}

@keyframes smoothFill {
    from { transform: scale(0.85); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

@keyframes pulseGlow {
    0%   { box-shadow: 0 0 18px rgba(255,59,48,0.4); }
    50%  { box-shadow: 0 0 45px rgba(255,59,48,0.9); }
    100% { box-shadow: 0 0 18px rgba(255,59,48,0.4); }
}

button[kind="primary"] {
    background: linear-gradient(135deg, #ff3b30, #ff6b6b);
    border-radius: 18px;
    font-size: 16px;
    font-weight: 600;
    padding: 0.8em 1.4em;
    width: 100%;
}

@media (max-width: 600px) {
    .circle { width: 150px; height: 150px; }
    .inner-circle { width: 120px; height: 120px; font-size: 22px; }
    .title { font-size: 34px; }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------
model = joblib.load("anxiety_model_5f.pkl")
scaler = joblib.load("scaler_5f.pkl")

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div class="glass">
    <div class="title"> NeuroPulse</div>
    
""", unsafe_allow_html=True)

# --------------------------------------------------
# Description
# --------------------------------------------------
st.markdown("""
<div class="glass" style="text-align:center;">
<div style="
    font-size:20px;
    color:#d1d5db;
    line-height:1.2;
    max-width:680px;
    margin:5px;
    class="input-card"
">
    NeuroPulse analyzes <b>lifestyle</b> and <b>physiological signals</b> to
    estimate social anxiety levels and promote early awareness.
</div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INPUTS (COLUMNS)
# --------------------------------------------------
# st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    sleep = st.slider("🛌 Sleep Hours", 3.0, 10.0, 6.5)
    stress = st.slider("😰 Stress Level (1–10)", 1, 10, 5)
    caffeine = st.slider("☕ Caffeine Intake (mg/day)", 0, 500, 150)
with col2:
    activity = st.slider("🏃 Physical Activity (hrs/week)", 0.0, 10.0, 2.5)
    heart_rate = st.slider("❤️ Heart Rate (bpm)", 60, 120, 80)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------
if st.button("🔮 Predict Anxiety Level", type="primary"):
    X = np.array([[sleep, activity, stress, heart_rate, caffeine]])
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]
    
    # Clamp for safety
    val = max(0, min(10, prediction))
    percent = int((val / 10) * 100)

    if val < 3:
        label, color, pulse = "Low Anxiety", "#34c759", ""
    elif val < 6:
        label, color, pulse = "Moderate Anxiety", "#ffcc00", ""
    else:
        label, color, pulse = "High Anxiety", "#ff3b30", "pulse"

    st.markdown(f"""
<div class="glass">
    <div style="text-align:center; font-size:22px; font-weight:600; color:white;">Anxiety Meter</div>
    <div class="meter-container">
        <div class="circle {pulse}" style="background: conic-gradient({color} {percent}%, rgba(255,255,255,0.1) 0%);">
            <div class="inner-circle">{val:.2f}/10</div>
        </div>
    </div>
    <div style="text-align:center; margin-top:18px; color:#d1d5db; font-size:16px;">
        Risk Category: <b style="color:{color};">{label}</b>
    </div>
</div>
""", unsafe_allow_html=True)

st.caption("⚠️ Educational purpose only. Not a medical diagnosis.")