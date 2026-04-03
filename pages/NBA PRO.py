import streamlit as st
import pandas as pd
import numpy as np
import requests
from scipy.stats import norm
from datetime import timedelta

# --- 1. CONFIG ---
st.set_page_config(page_title="Omni_Predict NBA Basketball", layout="wide", page_icon="🏀")

# --- 2. ELITE CSS STYLING ---
SLIDES = {
    "lebron": "https://www.vmcdn.ca/f/files/shared/feeds/cp/2025/06/d09609a450ddd4f8fec113034ee2a4ad8c91377e611f6af1afd71cb57c60190a.jpg;w=960",
    "lamelo": "https://sports.inquirer.net/files/2026/01/AP26023094809854-2048x1365.jpg",
    "ja_morant": "https://s.yimg.com/ny/api/res/1.2/VZhOUL6hM3nClXMwjIFyXw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTE0Mzk7Y2Y9Z3dlYnA--/https://media.zenfs.com/en/ny_post_sports_articles_389/2ac6667811020c2375b006ec736d819c",
    "luka": "https://heavy.com/wp-content/uploads/2026/03/IMG_5940-e1774491383472.jpeg?quality=65&strip=all&w=782",
    "giannis": "https://static01.nyt.com/images/2016/12/03/sports/03BUCKS/03BUCKS1-superJumbo.jpg?quality=75&auto=webp",
    "edwards": "https://cdn.britannica.com/58/258358-050-E786E676/gabe-vincent-of-miami-heat-draws-foul-against-anthony-edwards-during-basketball-game-2021.jpg?w=300",
    "shai": "https://platform.sbnation.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/25932976/2206592990.jpg?quality=90&strip=all&crop=0%2C13.930844293594%2C100%2C44.444444444444&w=1080"
}

OKC_COURT_URL = "https://images.unsplash.com/photo-1504450758481-7338eba7524a?q=80&w=2000"

st.markdown(f"""
    <style>
    /* Main App Background */
    .stApp {{ 
        background-image: linear-gradient(rgba(14, 17, 23, 0.8), rgba(14, 17, 23, 0.8)), url("{OKC_COURT_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff; 
    }}
    
    /* SLIDESHOW KEYFRAMES */
    @keyframes sidebar-fade {{
        0%, 14% {{ background-image: url("{SLIDES['lebron']}"); }}
        15%, 29% {{ background-image: url("{SLIDES['lamelo']}"); }}
        30%, 44% {{ background-image: url("{SLIDES['ja_morant']}"); }}
        45%, 59% {{ background-image: url("{SLIDES['luka']}"); }}
        60%, 74% {{ background-image: url("{SLIDES['giannis']}"); }}
        75%, 89% {{ background-image: url("{SLIDES['edwards']}"); }}
        90%, 100% {{ background-image: url("{SLIDES['shai']}"); }}
    }}

    /* SIDEBAR READABILITY UPGRADE */
    [data-testid="stSidebar"] {{
        animation: sidebar-fade 35s infinite;
        background-size: cover;
        background-position: center;
        border-right: 2px solid #00ffcc;
    }}
    /* 1. Darken the sidebar overlay even more */
    [data-testid="stSidebar"] > div:first-child {{
        background-color: rgba(0, 0, 0, 0.95) !important;
        backdrop-filter: blur(15px);
    }}

    /* 2. Fix the "Home Team" / "Away Team" Labels */
    [data-testid="stWidgetLabel"] p {{
        color: #00ffcc !important; /* Neon Cyan */
        font-weight: 900 !important; /* Extra Bold */
        font-size: 1.1rem !important;
        
       
    }}

    /* 3. Fix the Sidebar Title (GLOBAL CONTROL) */
    [data-testid="stSidebar"] h1 {{
        color: #00ffcc !important;
        font-weight: 900 !important;
    }}

    /* 4. Fix Slider numbers and small captions */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] span {{
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px #000 !important;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background-color: rgba(10, 12, 16, 0.6) !important;
        height: 100%;
        backdrop-filter: blur(3px); 
    }}

    /* --- SIDEBAR NAVIGATION BUTTONS --- */
    [data-testid="stSidebarNav"] li {{
        background-color: rgba(14, 17, 23, 0.9) !important;
        border: 1px solid rgba(0, 255, 204, 0.5);
        margin: 6px 12px;
        border-radius: 10px;
    }}

    [data-testid="stSidebarNav"] span {{
        color: #ffffff !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px #000;
    }}

    /* --- RESULTS CARD VISIBILITY UPGRADE --- */
    .results-card {{
        background-color: rgba(10, 12, 16, 0.95) !important; /* Much darker background for text contrast */
        padding: 30px;
        border-radius: 20px;
        border: 2px solid rgba(0, 255, 204, 0.6);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(8px);
        margin-top: 20px;
    }}

    /* Metric Labels (e.g., "Proj. Total", "Win %") */
    [data-testid="stMetricLabel"] {{
        color: #ffffff !important;
        font-weight: 900 !important;
        text-shadow: 3px 3px 6px #000000 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
    }}

    /* Metric Values (The numbers) */
    [data-testid="stMetricValue"] {{ 
        color: #00ffcc !important; 
        font-weight: 900 !important; 
        text-shadow: 3px 3px 8px #000000 !important;
        font-size: 2.5rem !important;
    }}

    /* --- FOOTER & HEADERS --- */
    h1, h2, h3 {{
        color: #00ffcc !important;
        text-shadow: 4px 4px 10px #000;
    }}

    .footer-warning {{
        padding: 20px;
        background: rgba(0, 0, 0, 0.8);
        border: 1px solid #ff4b4b;
        border-radius: 12px;
        margin-top: 25px;
        color: #ff9999;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA & ENGINE ---
NBA_MOCK_DB = {
    "CELTICS": [122.4, 9.9, 9.6], "THUNDER": [121.8, 9.8, 9.4], "NUGGETS": [118.2, 9.5, 8.7],      
    "TIMBERWOLVES": [114.1, 8.6, 9.8], "MAVERICKS": [119.5, 9.7, 8.3], "KNICKS": [114.2, 8.8, 9.7],        
    "SPURS": [116.4, 9.1, 9.2], "PACERS": [124.1, 10.0, 7.6], "76ERS": [115.8, 9.2, 8.8],        
    "BUCKS": [117.4, 9.3, 8.0], "CAVALIERS": [113.5, 8.7, 9.5], "SUNS": [115.9, 9.4, 7.9],          
    "ROCKETS": [116.2, 8.9, 9.1], "MAGIC": [111.8, 8.4, 9.8], "LAKERS": [116.7, 9.0, 8.1],        
    "WARRIORS": [115.2, 8.9, 8.2], "GRIZZLIES": [113.8, 8.8, 9.3], "KINGS": [117.1, 9.2, 7.7],        
    "PELICANS": [114.6, 8.8, 8.9], "HEAT": [110.8, 8.3, 9.4], "CLIPPERS": [113.4, 8.6, 8.5],      
    "BULLS": [112.5, 8.4, 7.9], "HAWKS": [119.1, 9.3, 7.2], "RAPTORS": [114.8, 8.6, 8.1],      
    "NETS": [109.5, 7.9, 8.3], "JAZZ": [116.3, 8.7, 7.0], "HORNETS": [112.2, 8.5, 7.4],      
    "TRAIL BLAZERS": [110.1, 8.1, 7.8], "PISTONS": [111.4, 8.2, 7.9], "WIZARDS": [115.0, 8.6, 6.5]       
}

def get_elite_stats(team_name):
    name_up = team_name.upper()
    for key in NBA_MOCK_DB:
        if key in name_up: return NBA_MOCK_DB[key]
    return [114.0, 8.5, 8.5]

def simulate_elite_hoops(h_stats, a_stats, hca_value):
    n = 10000
    h_adj = (h_stats[1] - a_stats[2]) * 1.5 
    a_adj = (a_stats[1] - h_stats[2]) * 1.5
    h_mu, a_mu = h_stats[0] + h_adj + hca_value, a_stats[0] + a_adj
    h_sim = np.random.normal(h_mu, 11.2, n)
    a_sim = np.random.normal(a_mu, 11.2, n)
    return h_sim, a_sim

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://blog.logomyway.com/wp-content/uploads/2017/01/nba-logo-design.jpg", width=80)
    st.title("GLOBAL CONTROL")
    st.markdown("---")
    t1_name = st.text_input("Home Team", "Hornets")
    t2_name = st.text_input("Away Team", "Pacers")
    hca_slider = st.slider("Home Court Advantage (Pts)", 0.0, 7.0, 2.5, 0.5)
    target_line = st.number_input("Total O/U Line", value=220.5)
    run_btn = st.button("🔥 RUN ELITE ANALYTICS", use_container_width=True)

# --- 5. MAIN UI ---
st.markdown("<h1 style='font-size:3.8rem;'>Omni_Predict Elite V1</h1>", unsafe_allow_html=True)

if run_btn:
    with st.spinner("Crunching 10,000 Iterations..."):
        h_s, a_s = get_elite_stats(t1_name), get_elite_stats(t2_name)
        h_sim, a_sim = simulate_elite_hoops(h_s, a_s, hca_slider)
        
        st.markdown('<div class="results-card">', unsafe_allow_html=True)
        st.subheader("🏆 Elite Probability Distribution")
        m = st.columns(4)
        m[0].metric(f"{t1_name} Win", f"{np.mean(h_sim > a_sim):.1%}")
        m[1].metric(f"{t2_name} Win", f"{np.mean(a_sim > h_sim):.1%}")
        m[2].metric("Proj. Total", f"{np.mean(h_sim + a_sim):.1f}")
        m[3].metric(f"Over {target_line}", f"{np.mean((h_sim + a_sim) > target_line):.1%}")

        st.subheader("📈 Spread Probability Matrix")
        spreads = [-11.5, -7.5, -3.5, 3.5, 7.5, 11.5]
        s_cols = st.columns(len(spreads))
        for i, s in enumerate(spreads):
            prob = np.mean((h_sim + s) > a_sim)
            s_cols[i].metric(f"Home {s}", f"{prob:.1%}")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👈 Use the control panel to start the simulation.")

# --- FOOTER ---
st.markdown('<div class="footer-warning">⚠️ <b>RESPONSIBLE GAMING WARNING:</b> This tool provides mathematical probabilities based on historical averages and 2026 projections. It does not guarantee results. Please gamble responsibly and only with money you can afford to lose.</div>', unsafe_allow_html=True)
st.caption("Omni NBA Predictor | 2026 Engine")