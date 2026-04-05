import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson, norm
import streamlit_analytics2 as streamlit_analytics

# This must be the first Streamlit command in every page file
st.set_page_config(page_title="Omni-SubPage", layout="wide")
# --- PAGE SETUP ---
st.set_page_config(page_title="Omni-Predictor v1.0", page_icon="🏆", layout="wide")

# --- 2. ELITE CSS STYLING ---
SLIDES = {
    "gular": "https://static01.nyt.com/athletic/uploads/wp/2024/08/12070633/GettyImages-2164704526-2048x1365.jpg",
    "yamal": "https://i.guim.co.uk/img/media/3f97dcf1fb70319cf5930c93642df4645dc29218/0_153_6000_3600/master/6000.jpg?width=620&dpr=2&s=none&crop=none",
    "downman": "https://www.reuters.com/resizer/v2/T4ICMMPZVZKEPOJ5PS3VKGNSCI.jpg?auth=03582d93be0f0d25e214be882f8e8a594a29aa1ad8ef637011097c311e2eb405&width=1080&quality=80",
    "olise": "https://platform.bavarianfootballworks.com/wp-content/uploads/sites/24/2025/09/gettyimages-2235238360.jpg?quality=90&strip=all&crop=0%2C5.5777081553214%2C100%2C88.844583689357&w=1080",
    "yildiz": "https://i.ytimg.com/vi/O4Ngej7mYik/oardefault.jpg?sqp=-oaymwEYCJUDENAFSFqQAgHyq4qpAwcIARUAAIhC&rs=AOn4CLAe_agXxF-McX6qdv-AjRDWz2njCA&usqp=CCk",
    "jamal": "https://img.fcbayern.com/image/upload/f_auto/q_auto/ar_2:1,c_fill,g_custom,w_1280,dpr_2/v1731174167/cms/public/images/fcbayern-com/homepage/Saison-24-25/Spieler/Musiala/241109-jamal-musiala-ima.jpg",
    "nico": "https://www.idman.biz/media/2026/03/05/1920x1280/niko.webp?v=1772697116"
}

FUT_BCG_URL = "https://www.kellwoodlighting.co.uk/media/uploads/cat-481/stadium-floodlight-design.webp?Width=1024&Height=573"

st.markdown(f"""
    <style>
    /* Main App Background */
    .stApp {{ 
        background-image: linear-gradient(rgba(14, 17, 23, 0.8), rgba(14, 17, 23, 0.6)), url("{FUT_BCG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff; 
    }}
    
    /* SLIDESHOW KEYFRAMES */
    @keyframes sidebar-fade {{
        0%, 14% {{ background-image: url("{SLIDES['gular']}"); }}
        15%, 29% {{ background-image: url("{SLIDES['yamal']}"); }}
        30%, 44% {{ background-image: url("{SLIDES['downman']}"); }}
        45%, 59% {{ background-image: url("{SLIDES['olise']}"); }}
        60%, 74% {{ background-image: url("{SLIDES['yildiz']}"); }}
        75%, 89% {{ background-image: url("{SLIDES['jamal']}"); }}
        90%, 100% {{ background-image: url("{SLIDES['nico']}"); }}
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
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px #000 !important;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background-color: rgba(10, 12, 16, 0.3) !important;
        height: 100%;
        backdrop-filter: blur(1.3px); 
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
        color: #ffffff !important;
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
    [data-testid="stTab"] {{
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



# --- ADVANCED MATH ENGINE ---
def calculate_advanced_prediction(h_mean, a_mean, line, sport_mode):
    if sport_mode == "Football":
        # Full Game (FG) Logic
        win_p, draw_p, loss_p, over_p = 0, 0, 0, 0
        # Half Time (HT) Logic (Weights: 45% of total goals usually happen in 1st half)
        ht_win, ht_draw, ht_loss, ht_over = 0, 0, 0, 0
        ht_line = 0.5 if line < 2.5 else 1.5
        
        h_adj, a_adj = h_mean + 0.2, a_mean - 0.2
        h_ht, a_ht = h_adj * 0.45, a_adj * 0.45

        for h in range(10):
            for a in range(10):
                # FG Calculation
                p_fg = poisson.pmf(h, h_adj) * poisson.pmf(a, a_adj)
                if h > a: win_p += p_fg
                elif h == a: draw_p += p_fg
                else: loss_p += p_fg
                if (h + a) > line: over_p += p_fg
                
                # HT Calculation
                p_ht = poisson.pmf(h, h_ht) * poisson.pmf(a, a_ht)
                if h > a: ht_win += p_ht
                elif h == a: ht_draw += p_ht
                else: ht_loss += p_ht
                if (h + a) > ht_line: ht_over += p_ht
        
        return {
            "type": "football",
            "fg": (win_p, draw_p, loss_p, over_p),
            "ht": (ht_win, ht_draw, ht_loss, ht_over, ht_line),
            "hcp": win_p if h_mean >= a_mean else (1 - loss_p)
        }
    else:
        # Basketball Logic (Normal Distribution for high scores)
        std_dev = 12 
        h_adj, a_adj = h_mean + 1.5, a_mean - 1.5
        # Win Prob
        diff_mean = h_adj - a_adj
        diff_std = np.sqrt(std_dev**2 + std_dev**2)
        win_p = 1 - norm.cdf(0, loc=diff_mean, scale=diff_std)
        # Over/Under
        total_std = np.sqrt(std_dev**2 + std_dev**2)
        over_p = 1 - norm.cdf(line, loc=(h_adj + a_adj), scale=total_std)
        # Quarters (1/4 of game)
        q_line = line / 4
        q_over = 1 - norm.cdf(q_line, loc=((h_adj + a_adj)/4), scale=(total_std/2))
        
        return {
            "type": "basketball",
            "fg": (win_p, 0.0, (1 - win_p), over_p),
            "q": (q_over, q_line),
            "spread": round(h_adj - a_adj, 1)
        }

# --- THE MASSIVE 2026 DATABASE ---
MOK_DB = {
    "Basketball": {
        "nuggets": 120.5, "heat": 119.8, "thunder": 119.5, "cavaliers": 119.4, "timberwolves": 119.2,
        "spurs": 118.0, "jazz": 117.8, "pistons": 117.5, "knicks": 117.2, "hawks": 117.1,
        "76ers": 116.7, "hornets": 116.0, "bulls": 115.7, "lakers": 115.7, "warriors": 115.6,
        "grizzlies": 115.6, "trail blazers": 115.5, "pelicans": 115.0, "magic": 115.0, "celtics": 115.0,
        "rockets": 114.5, "mavericks": 114.4, "raptors": 114.0, "wizards": 112.2, "bucks": 112.1,
        "suns": 112.1, "clippers": 111.7, "pacers": 111.5, "kings": 110.4, "nets": 107.0
    },
    "Football": {
        # ENGLAND
        "man city": 2.15, "arsenal": 2.10, "liverpool": 2.05, "chelsea": 1.95, "tottenham": 1.88,
        "man utd": 1.80, "aston villa": 1.75, "newcastle": 1.72, "brighton": 1.65, "west ham": 1.58,
        "brentford": 1.45, "bournemouth": 1.42, "fulham": 1.38, "crystal palace": 1.35, "wolves": 1.25,
        "nottingham forest": 1.22, "everton": 1.15, "leeds": 1.28, "leicester": 1.20, "southampton": 1.18, "ipswich": 1.10,
        "burnley": 1.65, "sunderland": 1.60, "sheffield utd": 1.55, "luton": 1.52, "middlesbrough": 1.50,
        "coventry": 1.48, "norwich": 1.45, "west brom": 1.42, "hull city": 1.40, "watford": 1.38,
        "bristol city": 1.35, "swansea": 1.32, "cardiff": 1.28, "millwall": 1.25, "qpr": 1.22,
        "sheffield wed": 1.18, "stokes": 1.15, "blackburn": 1.12, "preston": 1.10, "derby": 1.25, "oxford": 1.05,
        # SPAIN
        "real madrid": 2.25, "barcelona": 2.20, "atletico madrid": 1.85, "girona": 1.82, "athletic bilbao": 1.70,
        "real sociedad": 1.65, "real betis": 1.62, "villarreal": 1.60, "valencia": 1.45, "sevilla": 1.42,
        "osasuna": 1.35, "getafe": 1.20, "las palmas": 1.25, "rayo vallecano": 1.22, "celta vigo": 1.30,
        "mallorca": 1.18, "alaves": 1.15, "leganes": 1.10, "valladolid": 1.08, "espanyol": 1.12,
        # ITALY
        "inter milan": 2.10, "ac milan": 1.95, "juventus": 1.85, "napoli": 1.88, "atalanta": 1.92,
        "as roma": 1.70, "lazio": 1.68, "bologna": 1.60, "fiorentina": 1.58, "torino": 1.40,
        "monza": 1.35, "genoa": 1.32, "udinese": 1.28, "cagliari": 1.22, "lecce": 1.15,
        "empoli": 1.12, "parma": 1.30, "como": 1.25, "venezia": 1.18, "verona": 1.10,
        # GERMANY
        "bayern munich": 2.85, "bayer leverkusen": 2.40, "borussia dortmund": 2.25, "rb leipzig": 2.15,
        "vfb stuttgart": 2.10, "eintracht frankfurt": 1.95, "wolfsburg": 1.65, "freiburg": 1.62,
        "hoffenheim": 1.75, "werder bremen": 1.55, "mgladbach": 1.58, "augsburg": 1.45,
        "mainz 05": 1.42, "heidenheim": 1.38, "union berlin": 1.30, "st pauli": 1.25, "holstein kiel": 1.15, "bochum": 1.12,
        # EUROPEAN GIANTS
        "psg": 2.30, "monaco": 1.95, "marseille": 1.90, "lille": 1.85, "lyon": 1.78,
        "psv": 2.50, "feyenoord": 2.15, "ajax": 1.95, "az alkmaar": 1.80,
        "sporting cp": 2.45, "benfica": 2.10, "fc porto": 1.95, "braga": 1.80,
        "galatasaray": 2.20, "fenerbahce": 2.15, "besiktas": 1.90,
        "celtic": 2.35, "rangers": 2.05, "bodø glimt": 2.10, "shakhtar": 1.85,
        
        "DEFAULT": 1.20
    },
}
# --- SIDEBAR ---
with st.sidebar:
    # 1. Define your logo URLs in a list
    # You can add as many as you want here
    logos = [
        "https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/UEFA_Champions_League.svg/500px-UEFA_Champions_League.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/500px-Premier_League_Logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/LaLiga_logo_2023.svg/500px-LaLiga_logo_2023.svg.png?_=20230606084527",
        "https://logolook.net/wp-content/uploads/2024/05/Bundesliga-Logo.png"
        "https://upload.wikimedia.org/wikipedia/en/thumb/a/ab/Serie_A_ENILIVE_logo.svg/330px-Serie_A_ENILIVE_logo.svg.png"
        
    ]

    # 2. OPTIONAL: Add some CSS to center them and add a glow
    st.markdown("""
        <style>
        [data-testid="column"] img {
            border-radius: 10px;
            padding: 4px;
            filter: drop-shadow(0 0 5px rgba(0, 255, 204, 0.4));
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. Create the row of logos
    st.write("### Featured Matchups")
    cols = st.columns(len(logos))

    for i, url in enumerate(logos):
        with cols[i]:
            st.image(url, use_container_width=True)
        
    st.title("🎮 GLOBAL CONTROL")
    sport_mode = st.selectbox("Select Sport", ["Football", "Basketball"])
    st.subheader("⚔️ Matchup")
    t1_in = st.text_input("Home Team", "Real Madrid").lower().strip()
    t2_in = st.text_input("Away Team", "Barcelona").lower().strip()
    
    db = MOK_DB.get(sport_mode, {})
    h_db = db.get(t1_in, 1.1 if sport_mode == "Football" else 114.0)
    a_db = db.get(t2_in, 1.1 if sport_mode == "Football" else 114.0)
    
    h_stat = st.number_input(f"Home {sport_mode} Avg", value=float(h_db))
    a_stat = st.number_input(f"Away {sport_mode} Avg", value=float(a_db))
    m_line = st.number_input("O/U Line", value=2.5 if sport_mode == "Football" else 224.5)
    run_analysis = st.button("🔥 RUN V22.0 ANALYSIS")

# --- MAIN INTERFACE ---
with streamlit_analytics.track():
    st.title("🏆 Omni-Predictor v1.0")
    
    if run_analysis:
        res = calculate_advanced_prediction(h_stat, a_stat, m_line, sport_mode)
        fg_w, fg_d, fg_l, fg_o = res["fg"]
        
        st.success(f"ANALYSIS COMPLETE: {t1_in.upper()} VS {t2_in.upper()}")
        
        # 5-Column Metrics (Updated to include Away Win)
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Home Win", f"{fg_w:.1%}")
        c2.metric("Away Win", f"{fg_l:.1%}")  # Added Away Win Prob
        c3.metric("Over/Under", f"{fg_o:.1%}")
        
        if sport_mode == "Football":
            c4.metric("Draw Prob", f"{fg_d:.1%}")
            c5.metric("Home HCP (-0.5)", f"{res['hcp']:.1%}")
        else:
            c4.metric("Proj. Spread", f"{res['spread']}")
            c5.metric("Qtr O/U Prob", f"{res['q'][0]:.1%}")

        st.divider()

        if sport_mode == "Football":
            t1, t2, t3 = st.tabs(["📊 Score Matrix", "⏱️ Half-Time / 2nd Half", "📈 Handicap Markets"])
            with t1:
                # Using adjusted means for the matrix to match the math engine
                h_adj, a_adj = h_stat + 0.2, a_stat - 0.2
                matrix_data = [[(poisson.pmf(h, h_adj)*poisson.pmf(a, a_adj))*100 for a in range(6)] for h in range(6)]
                df = pd.DataFrame(matrix_data, index=[f"{i}" for i in range(6)], columns=[f"{i}" for i in range(6)])
                fig, ax = plt.subplots(figsize=(10, 4))
                fig.patch.set_facecolor('#0e1117')
                ax.set_facecolor('#0e1117')
                sns.heatmap(df, annot=True, fmt=".1f", cmap="mako", ax=ax, cbar=False, annot_kws={"color": "white"})
                plt.xlabel("Away Goals", color="white")
                plt.ylabel("Home Goals", color="white")
                st.pyplot(fig)
            with t2:
                ht_w, ht_d, ht_l, ht_o, ht_lv = res["ht"]
                st.subheader(f"Half-Time Markets (O/U {ht_lv})")
                st.write(f"HT Home Win: {ht_w:.1%}")
                st.write(f"HT Draw: {ht_d:.1%}")
                st.write(f"HT Away Win: {ht_l:.1%}")
                st.write(f"HT Over Prob: {ht_o:.1%}")
                st.info("Second Half Trend: 2nd half goals are statistically 20% more likely than 1st half.")
        else:
            t1, t2 = st.tabs(["🏀 Quarter Analysis", "📈 Handicap Spread"])
            with t1:
                st.write(f"**Individual Quarter Projection**")
                st.write(f"Avg Points Per Quarter: {(h_stat + a_stat)/4:.1f}")
                st.write(f"Prob Over {res['q'][1]:.1f}: {res['q'][0]:.1%}")

# --- FOOTER & WARNING ---
st.divider()
st.markdown('<div class="footer-warning">⚠️ **RESPONSIBLE GAMING WARNING:** This tool provides mathematical probabilities based on historical averages and Poisson distribution. It does not guarantee results. Betting involves significant risk of financial loss. Please gamble responsibly and only with money you can afford to lose.</div>', unsafe_allow_html=True)
st.caption("v1.0.0 Pro Terminal | Global League Database Loaded | Secure Analytics Active - 2026.")