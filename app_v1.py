import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Set page config
st.set_page_config(
    page_title="F1 Race Predictor",
    page_icon="🏎️",
    layout="centered"
)

# Premium Custom CSS for Racing Theme
st.markdown("""
<style>
    /* Styling base page */
    .stApp {
        background: radial-gradient(circle at top left, #1e1e24, #0f0f12);
        color: #f5f5f7;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    
    /* Header Container */
    .header-container {
        background: linear-gradient(135deg, #e10600, #960000);
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(225, 6, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    .header-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(45deg, rgba(0,0,0,0.05), rgba(0,0,0,0.05) 10px, transparent 10px, transparent 20px);
    }
    .header-title {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 1.5px;
        position: relative;
        z-index: 1;
    }
    .header-subtitle {
        color: #ffb3b1;
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
        margin-bottom: 0;
        letter-spacing: 0.5px;
        position: relative;
        z-index: 1;
    }
    
    /* Card Container */
    .glass-card {
        background: rgba(30, 30, 40, 0.45);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Prediction Glow Cards */
    .prediction-card {
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        border-left: 6px solid #e10600;
    }
    
    .podium-card {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 215, 0, 0.02));
        border-left: 6px solid #ffd700;
        box-shadow: 0 8px 30px rgba(255, 215, 0, 0.15);
    }
    .points-card {
        background: linear-gradient(135deg, rgba(0, 230, 118, 0.15), rgba(0, 230, 118, 0.02));
        border-left: 6px solid #00e676;
        box-shadow: 0 8px 30px rgba(0, 230, 118, 0.1);
    }
    .outside-card {
        background: linear-gradient(135deg, rgba(255, 61, 0, 0.15), rgba(255, 61, 0, 0.02));
        border-left: 6px solid #ff3d00;
        box-shadow: 0 8px 30px rgba(255, 61, 0, 0.1);
    }
    
    /* Probability Bar container */
    .prob-bar-bg {
        background: rgba(255,255,255,0.06);
        border-radius: 8px;
        height: 12px;
        width: 100%;
        margin-top: 6px;
        overflow: hidden;
    }
    .prob-bar-fill-podium {
        background: linear-gradient(90deg, #ffb300, #ffd700);
        height: 100%;
        border-radius: 8px;
    }
    .prob-bar-fill-points {
        background: linear-gradient(90deg, #00b0ff, #00e676);
        height: 100%;
        border-radius: 8px;
    }
    .prob-bar-fill-outside {
        background: linear-gradient(90deg, #ff1744, #ff3d00);
        height: 100%;
        border-radius: 8px;
    }
    
    /* Input design tweaks */
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
    
    /* Custom button */
    .stButton>button {
        background: linear-gradient(135deg, #e10600, #ff3c35);
        color: white;
        font-weight: 700;
        letter-spacing: 1px;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        box-shadow: 0 4px 15px rgba(225, 6, 0, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #ff3c35, #e10600);
        box-shadow: 0 6px 20px rgba(225, 6, 0, 0.6);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏎️ F1 RACE PREDICTOR</h1>
    <p class="header-subtitle">Predicting outcomes using Qualifying Grid, Team, and Track data (Version 1)</p>
</div>
""", unsafe_allow_html=True)

# Check for model and dataset files
data_file = 'f1_v1_data.csv'
model_file = 'f1_model_v1.pkl'

if not os.path.exists(data_file) or not os.path.exists(model_file):
    st.markdown("""
    <div class="glass-card" style="border-left: 6px solid #e10600;">
        <h3 style="color: #ff3d00; margin-top:0;">⚠️ Files Missing!</h3>
        <p>Before you can make predictions, you need to collect the F1 dataset and train the model.</p>
        <p><strong>Steps to execute in terminal:</strong></p>
        <ol>
            <li>Run data collection: <code>python fetch_data_v1.py</code></li>
            <li>Train model: <code>python train_v1.py</code></li>
        </ol>
        <p>Once both scripts complete successfully, this dashboard will be fully operational.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Load dataset
    df = pd.read_csv(data_file)
    
    # Load model pipeline
    model = joblib.load(model_file)
    
    # Sidebar or input card
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🏁 Race Input Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Season selection
        seasons = sorted(df['season'].unique().tolist(), reverse=True)
        selected_season = st.selectbox("Season", seasons)
        
        # Team selection
        teams = sorted(df['team'].unique().tolist())
        selected_team = st.selectbox("Constructor / Team", teams)
        
    with col2:
        # Circuit selection
        circuits = sorted(df['circuit'].unique().tolist())
        selected_circuit = st.selectbox("Circuit / Grand Prix", circuits)
        
        # Grid position selection
        grid_pos = st.slider("Starting Grid Position", min_value=1, max_value=20, value=1)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Predict button
    if st.button("🔮 PREDICT OUTCOME"):
        # Create input df
        input_data = pd.DataFrame([{
            'season': selected_season,
            'circuit': selected_circuit,
            'team': selected_team,
            'grid_position': grid_pos
        }])
        
        # Get predictions
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        prob_podium = probabilities[0]
        prob_points = probabilities[1]
        prob_outside = probabilities[2]
        
        # Display Prediction Result Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🏆 Model Prediction")
        
        if prediction == 0:
            card_class = "podium-card"
            badge = "🏆 TOP 3 (PODIUM)"
            desc = "Model predicts a podium finish! High chance of a trophy."
        elif prediction == 1:
            card_class = "points-card"
            badge = "🏁 TOP 10 (POINTS)"
            desc = "Model predicts a top-10 finish. Scoring points for the championship!"
        else:
            card_class = "outside-card"
            badge = "❌ OUTSIDE TOP 10"
            desc = "Model predicts finishing outside the points (P11-P20)."
            
        st.markdown(f"""
        <div class="prediction-card {card_class}">
            <h2 style="margin: 0; font-size: 1.8rem; color: white;">{badge}</h2>
            <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 0.95rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Detailed Probability Bars
        st.markdown("<h4 style='margin-top: 2rem;'>Probability Breakdown</h4>", unsafe_allow_html=True)
        
        # Podium probability
        st.markdown(f"**Top 3 (Podium):** {prob_podium*100:.1f}%", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="prob-bar-bg">
            <div class="prob-bar-fill-podium" style="width: {prob_podium*100}%;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Points probability
        st.markdown(f"<div style='margin-top: 1rem;'>**Top 10 (Points):** {prob_points*100:.1f}%</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="prob-bar-bg">
            <div class="prob-bar-fill-points" style="width: {prob_points*100}%;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Outside Top 10 probability
        st.markdown(f"<div style='margin-top: 1rem;'>**Outside Top 10:** {prob_outside*100:.1f}%</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="prob-bar-bg">
            <div class="prob-bar-fill-outside" style="width: {prob_outside*100}%;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
