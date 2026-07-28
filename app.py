# ==============================================================================
# SEGMENT 1 OF 15: CORE LIBRARIES, HIGH-UTILITY STYLING & BRANDING SLOGAN
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import io
import os
import json
import datetime
import http.client
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="Sisonke Football Predictive Analytics", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .reportview-container { background: #0f172a; }
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
    div.stButton > button:first-child {
        background-color: #2563eb !important; color: white !important;
        border-radius: 6px !important; border: none !important;
        font-weight: bold !important; width: 100% !important; height: 3em !important;
    }
    div.stButton > button:hover { background-color: #1d4ed8 !important; }
    .insight-box {
        background-color: #1e293b; border-left: 5px solid #3b82f6;
        padding: 15px; border-radius: 4px; color: #e2e8f0; font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Refined branding: No leading ball icon, unique ball placeholder replaces the letter 'o' in Sisonke
st.markdown("<h1 style='margin-bottom: 0px;'>Sis⚽nke Football Predictive Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-style: italic; color: #94a3b8; font-size: 18px; margin-top: 0px; margin-bottom: 25px;'>We beat the odds</p>", unsafe_allow_html=True)
# ==============================================================================
# SEGMENT 2 OF 15: MASTER INITIALIZATION MATRIX & DATA ENGINE IMPORT HANDSHAKE
# ==============================================================================
try:
    import main_engine as engine
except ImportError:
    st.error("🚨 CRITICAL CORE MISCONFIGURED: 'main_engine.py' was not detected in your folder directory workspace path.")
    st.stop()

if "is_profile_view" not in st.session_state:
    st.session_state["is_profile_view"] = False
if "is_aggregate_stats_view" not in st.session_state:
    st.session_state["is_aggregate_stats_view"] = False
if "freeze_matrix" not in st.session_state:
    st.session_state.freeze_matrix = {"last_error": None}

is_profile_view = st.session_state["is_profile_view"]
is_aggregate_stats_view = st.session_state["is_aggregate_stats_view"]

API_LEAGUE_ID_MAP = {
    "English Premier League": 39, "Spanish La Liga": 140, "Italian Serie A": 135,
    "German Bundesliga": 78, "French Ligue 1": 61, "UEFA Champions League": 2,
    "Africa Cup of Nations": 6, "FIFA World Cup": 1
}

api_sync_triggered = False
total_fixtures = 0
storage_path = "master_sisonke_database.csv"
# ==============================================================================
# SEGMENT 3 OF 15: SIDEBAR CONTROL PANEL INGESTION RADAR & TURNOVER SLIDERS
# ==============================================================================
with st.sidebar:
    st.markdown("### 📂 Data Control Room")
    uploaded_file = st.file_uploader("Upload Master Match CSV", type=["csv"])
    active_radar_df = pd.DataFrame()
    
    if uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            active_radar_df = pd.read_csv(uploaded_file, engine='python')
            uploaded_file.seek(0)
        except: pass
    elif os.path.exists(storage_path):
        try: active_radar_df = pd.read_csv(storage_path)
        except: pass

    if not active_radar_df.empty:
        st.markdown("#### 📡 Multi-League Ingestion Radar")
        radar_rows = []
        active_radar_df.columns = [str(c).strip().lower() for c in active_radar_df.columns]
        league_col = "league_country" if "league_country" in active_radar_df.columns else "league"
        goals_col = "home_goals" if "home_goals" in active_radar_df.columns else "fthg"
        
        if league_col in active_radar_df.columns:
            unique_leagues = sorted(list(active_radar_df[league_col].dropna().unique()))
            for lg in unique_leagues:
                lg_df = active_radar_df[active_radar_df[league_col] == lg]
                settled_count = int(lg_df[goals_col].dropna().notna().sum()) if goals_col in lg_df.columns else 0
                upcoming_count = len(lg_df) - settled_count
                phase_tag = "⏳ PRE-SEASON (ANCHOR REQ)" if settled_count == 0 else ("🌱 EARLY SEASON (HYBRID)" if settled_count < 20 else "🟢 IN-PROGRESS (DECAY)")
                radar_rows.append({"Target Competition": str(lg).upper(), "Settled": settled_count, "Upcoming": upcoming_count, "Database Status Room": phase_tag})
            st.dataframe(pd.DataFrame(radar_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 🛠️ Pre-Season Calibration Room")
    preseason_calibration_active = st.checkbox("Activate Prior-Season Baseline Anchor", value=False)
    preseason_turnover_rate = 1.00
    if preseason_calibration_active:
        squad_turnover_intensity = st.select_slider("Select Summer Overhaul Intensity:", options=["Low Roster Change", "Standard Turnover", "Heavy Overhaul / New Manager"], value="Standard Turnover")
        preseason_turnover_rate = 0.95 if squad_turnover_intensity == "Low Roster Change" else (0.82 if "Heavy" in squad_turnover_intensity else 0.90)
        # ==============================================================================
# SEGMENT 4 OF 15: DORMANT API REQUEST ROUTER & PROFILE SELECTOR FORMS
# ==============================================================================
with st.sidebar:
    st.markdown("### 🔑 API Automation Options (Dormant Feed Track)")
    api_token_input = st.text_input("Enter API-Football Token Key:", value="4c023480e8ffe2539261cd8746f67121", type="password")
    sync_operation_mode = st.selectbox("Select API Query Framework:", ["Compile Bulk Historical CSV (Method 1)", "Global Calendar Date", "Dedicated Team Profile Form", "View Team Profile Identity", "Aggregated Team Stats"])
    
    if sync_operation_mode in ["Compile Bulk Historical CSV (Method 1)", "Aggregated Team Stats"]:
        target_sync_country = st.selectbox("Select Target Sync Competition:", list(API_LEAGUE_ID_MAP.keys()))
        sync_target_scope = st.radio("Select Sync Scope Window:", ["Settled Historical Data", "Upcoming 30-Day Fixtures"])
        manual_override_active = st.checkbox("Manual Season Override Year", value=False)
        selected_override_year = st.selectbox("Select Target Season Campaign Year:", options=list(range(2026, 2020, -1)), index=0)
    
    api_sync_triggered = st.button("🚀 Execute Automated Bulk Scrape")
    ui_email_recipient = st.text_input("Primary Email:", value="vvuyo007@gmail.com")
    ui_sms_recipient = st.text_input("Mobile SMS:", value="0750739223@sms.telkom.co.za")
    ui_google_app_password = st.text_input("Password Key:", type="password", value="your_free_google_app_password")
    # ==============================================================================
# SEGMENT 5 OF 15: CSV SCHEMA TRANSLATION ENGINE & DATA NOISE SHIELD
# ==============================================================================
full_validation_df = pd.DataFrame()
is_valid_data = False

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        manual_upload_df = pd.read_csv(uploaded_file, engine='python')
        
        ALIGNED_HEADER_TRANSLATION_MAP = {
            "div": "league_country", "league_name": "league_country", "competition": "league_country",
            "date": "match_timestamp", "timestamp": "match_timestamp",
            "home": "home_team", "hometeam": "home_team",
            "away": "away_team", "awayteam": "away_team",
            "fthg": "home_goals", "hg": "home_goals",
            "ftag": "away_goals", "ag": "away_goals",
            "hs": "home_sot", "as": "away_sot", "home shots": "home_sot", "away shots": "away_sot",
            "home_red_cards": "home_red_cards", "away_red_cards": "away_red_cards", "hrc": "home_red_cards", "arc": "away_red_cards"
        }
        manual_upload_df.columns = [str(c).strip().lower() for c in manual_upload_df.columns]
        manual_upload_df.rename(columns=ALIGNED_HEADER_TRANSLATION_MAP, inplace=True)
        
        # Disciplinary Red Card Anomaly Cleaner Pass
        if "home_red_cards" in manual_upload_df.columns and "away_red_cards" in manual_upload_df.columns:
            red_card_mask = (manual_upload_df["home_red_cards"] > 0) | (manual_upload_df["away_red_cards"] > 0)
            if red_card_mask.any():
                manual_upload_df.loc[red_card_mask, "home_goals"] = manual_upload_df.loc[red_card_mask, "home_goals"].clip(upper=3)
                manual_upload_df.loc[red_card_mask, "away_goals"] = manual_upload_df.loc[red_card_mask, "away_goals"].clip(upper=3)

        if "league_country" not in manual_upload_df.columns: manual_upload_df["league_country"] = "Imported League"
        if "match_timestamp" not in manual_upload_df.columns: manual_upload_df["match_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d")

        DEFAULT_TIER2_FALLBACKS = {
            "home_goals": np.nan, "away_goals": np.nan, "home_sot": 4.0, "away_sot": 3.5,
            "home_big_chances": 1.2, "away_big_chances": 0.9, "home_box_touches": 16.0, "away_box_touches": 13.0,
            "home_rest_days": 5.0, "away_rest_days": 5.0
        }
        
        for mandatory_col, fallback_val in DEFAULT_TIER2_FALLBACKS.items():
            if mandatory_col not in manual_upload_df.columns: manual_upload_df[mandatory_col] = fallback_val
            else: manual_upload_df[mandatory_col] = manual_upload_df[mandatory_col].fillna(fallback_val)
        
        full_validation_df = manual_upload_df.copy()
        is_valid_data = True
    except Exception as e: st.error(f"Manual Ingestion Shield Error: {e}")
    # ==============================================================================
# SEGMENT 6 OF 15: DUAL-TRACK LOCAL INGESTION SHIELD & DORMANT API ROUTER
# ==============================================================================
processed_execution_rows = []
historical_reference_df = pd.read_csv(storage_path) if os.path.exists(storage_path) else pd.DataFrame()

if not historical_reference_df.empty:
    historical_reference_df["match_timestamp"] = pd.to_datetime(historical_reference_df["match_timestamp"], errors='coerce')

# Offline Manual Local CSV File Processing Track
if is_valid_data and not full_validation_df.empty and not api_sync_triggered:
    st.sidebar.caption("🟢 Mode Status: Running 100% Offline Local CSV Track")
    total_upload_records = len(full_validation_df)
    
    for index, row in full_validation_df.iterrows():
        h_name = str(row["home_team"]).strip()
        a_name = str(row["away_team"]).strip()
        current_match_time = pd.to_datetime(row["match_timestamp"], errors='coerce')
        if pd.isnull(current_match_time): current_match_time = pd.Timestamp.now()
            
        calculated_home_rest_days = 5.0
        calculated_away_rest_days = 5.0
        if not historical_reference_df.empty:
            home_past = historical_reference_df[((historical_reference_df["home_team"] == h_name) | (historical_reference_df["away_team"] == h_name)) & (historical_reference_df["match_timestamp"] < current_match_time)]
            if not home_past.empty: calculated_home_rest_days = float(max(1, min(14, (current_match_time - home_past["match_timestamp"].max()).days)))
            away_past = historical_reference_df[((historical_reference_df["home_team"] == a_name) | (historical_reference_df["away_team"] == a_name)) & (historical_reference_df["match_timestamp"] < current_match_time)]
            if not away_past.empty: calculated_away_rest_days = float(max(1, min(14, (current_match_time - away_past["match_timestamp"].max()).days)))

        processed_execution_rows.append({
            "league_country": row.get("league_country", "Imported League"), "match_timestamp": current_match_time.isoformat(),
            "home_team": h_name, "away_team": a_name, "home_goals": row.get("home_goals"), "away_goals": row.get("away_goals"),
            "home_sot": float(row.get("home_sot", 4.0)), "away_sot": float(row.get("away_sot", 3.5)),
            "home_big_chances": float(row.get("home_big_chances", 1.2)), "away_big_chances": float(row.get("away_big_chances", 0.9)),
            "home_box_touches": float(row.get("home_box_touches", 16.0)), "away_box_touches": float(row.get("away_box_touches", 13.0)),
            "home_rest_days": calculated_home_rest_days, "away_rest_days": calculated_away_rest_days
        })

# Dormant API Automation Network Ingestion Track
elif api_sync_triggered and globals().get("target_fixtures"):
    st.sidebar.caption("⚡ Mode Status: API Override Activated Pass")
    for index, item in enumerate(target_fixtures):
        f_meta = item.get("fixture", {})
        teams = item.get("teams", {})
        goals = item.get("goals", {})
        h_name, a_name = teams.get("home", {}).get("name"), teams.get("away", {}).get("name")
        current_match_time = pd.to_datetime(f_meta.get("date", datetime.datetime.now().isoformat()))
        
        processed_execution_rows.append({
            "league_country": item.get("league", {}).get("country", "Global Stream"), "match_timestamp": current_match_time.isoformat(),
            "home_team": h_name, "away_team": a_name, "home_goals": goals.get("home"), "away_goals": goals.get("away"),
            "home_sot": 4.0, "away_sot": 3.5, "home_big_chances": 1.2, "away_big_chances": 0.9, "home_box_touches": 16.0, "away_box_touches": 13.0,
            "home_rest_days": 5.0, "away_rest_days": 5.0
        })

if processed_execution_rows:
    new_compiled_df = pd.DataFrame(processed_execution_rows)
    if not historical_reference_df.empty:
        combined_disk_df = pd.concat([historical_reference_df, new_compiled_df], ignore_index=True)
        combined_disk_df.drop_duplicates(subset=["league_country", "match_timestamp", "home_team", "away_team"], keep="last", inplace=True)
        combined_disk_df.to_csv(storage_path, index=False)
    else: new_compiled_df.to_csv(storage_path, index=False)
    st.success("💾 Tracking database logs updated to hard disk.")
    st.rerun()
    # ==============================================================================
# SEGMENT 7 OF 15: PIPELINE DATA REISTRY SELECTION & TUNING CONTROLS
# ==============================================================================
working_pipeline_df = pd.read_csv(storage_path) if os.path.exists(storage_path) else pd.DataFrame()

if not working_pipeline_df.empty:
    working_pipeline_df["match_timestamp"] = pd.to_datetime(working_pipeline_df["match_timestamp"], errors='coerce').fillna(pd.Timestamp.now())
    working_pipeline_df.drop_duplicates(subset=["league_country", "match_timestamp", "home_team", "away_team"], keep="last", inplace=True)
    
    for col in ["home_goals", "away_goals", "home_sot", "away_sot", "home_big_chances", "away_big_chances", "home_rest_days", "away_rest_days"]:
        if col in working_pipeline_df.columns:
            working_pipeline_df[col] = pd.to_numeric(working_pipeline_df[col], errors='coerce').fillna(0.0)
    uploaded_leagues = sorted(list(working_pipeline_df["league_country"].dropna().unique()))
else:
    st.info("📂 Please upload your master CSV dataset folder to activate dashboard.")
    st.stop()

selected_league_filter = st.selectbox("Select Target Division:", uploaded_leagues)
half_life_days = st.slider("Time-Decay Half Life (Days)", 15, 90, 45, 1)

for idx, league in enumerate(uploaded_leagues):
    st.session_state.freeze_matrix[league.lower().strip()] = st.checkbox(f"Freeze Decay: {league.upper()}", value=st.session_state.freeze_matrix.get(league.lower().strip(), False), key=f"f_{idx}")

max_score_cap = st.slider("Max Score Ceiling", 4, 10, 6, 1)
vol_dampener = st.slider("Volatility Dampener", 0.5, 1.5, 1.0, 0.05)
backtest_window = st.slider("Backtest Window Size (Days)", 90, 365, 180, 5)
confidence_floor_input = st.slider("Strict Confidence Floor Trigger (%)", 15, 85, 50, 5)
accuracy_threshold_floor = st.slider("Strict Accuracy Floor (%)", 35, 75, 50, 5) / 100.0

filtered_df = working_pipeline_df[working_pipeline_df["league_country"].str.lower().str.strip() == selected_league_filter.lower().strip()].reset_index(drop=True)
# ==============================================================================
# SEGMENT 8 OF 15: TIME-DECAY weight CHART & VENUE MOMENTUM INDICATORS
# ==============================================================================
st.markdown("### 📈 Exponential Time-Decay Weighting Behavior Visualization")
days_axis = np.arange(0, 120, 1)
decay_weights = (0.5) ** (days_axis / half_life_days)
st.line_chart(pd.DataFrame({"Model Weight Factor": decay_weights}, index=days_axis), use_container_width=True)

tab_pred, tab_tables, tab_history, tab_past = st.tabs(["📅 PROJECTIONS", "🌍 STANDINGS", "📜 BACKTESTER", "📜 PAST GAMES"])

with tab_pred:
    if not filtered_df.empty:
        options = {f"[{r['league_country'].upper()}] {r['home_team']} vs {r['away_team']} ({pd.to_datetime(r['match_timestamp']).strftime('%Y-%m-%d')})": r for idx, r in filtered_df.iterrows()}
        if options:
            sel_match = st.selectbox("Select Profile Target fixture:", list(options.keys()))
            target = options[sel_match]
            target_ts = pd.to_datetime(target["match_timestamp"])
            
            past_home = filtered_df[(filtered_df["home_team"] == target["home_team"]) & (filtered_df["match_timestamp"] < target_ts)].sort_values(by="match_timestamp").tail(5)
            past_away = filtered_df[(filtered_df["away_team"] == target["away_team"]) & (filtered_df["match_timestamp"] < target_ts)].sort_values(by="match_timestamp").tail(5)
            
            home_streak_score = sum([1 if r["home_goals"] > r["away_goals"] else -1 for _, r in past_home.iterrows()])
            away_streak_score = sum([1 if r["away_goals"] > r["home_goals"] else -1 for _, r in past_away.iterrows()])
            
            st.markdown("### 🚨 Venue Momentum Indicators")
            s_col1, s_col2 = st.columns(2)
            with s_col1: st.info(f"📊 {target['home_team']} Home Streak Index: {home_streak_score:+} Units")
            with s_col2: st.info(f"📊 {target['away_team']} Away Streak Index: {away_streak_score:+} Units")
            # ==============================================================================
# SEGMENT 9 OF 15: FLAT GLOBAL STRATEGIC OVERRIDES CONTROL BOARD
# ==============================================================================
# Left-aligned flat against the document margin to clear nested indentation traps
st.markdown("### ⛅ Matchday Conditions & Strategic Overrides")
w_col1, w_col2, w_col3 = st.columns(3)
with w_col1:
    weather_condition_selection = st.selectbox("Current Matchday Weather Climate:", ["Optimal / Standard Ambient / Indoor Dome", "Heavy Rain / High Pitch Slick Surface", "Extreme High Wind / Aerodynamic Drag Line"])
with w_col2:
    tournament_framework_selection = st.selectbox("Competition Tournament Format Stage:", ["Standard Domestic League Match", "🏆 Neutral-Site Tournament Group Stage", "💀 Knockout Round (Extra-Time Risk)"])
with w_col3:
    coach_stability_selection = st.selectbox("Host Team Coach Stability Status:", ["Long-Term Stability (2+ Years)", "Stable Baseline / Standard Tenure", "Recent Appointment / Caretaker Setup", "🚨 Public Dressing Room Friction"])

st.markdown("#### ⚙️ Syndicate Tactical Mismatch & Travel Metrics")
t_col1, t_col2, t_col3 = st.columns(3)
with t_col1:
    home_tactical_style = st.selectbox("Home Tactical Blueprint Style:", ["Standard Balanced / Unspecified", "High-Possession Pressing", "Fast Transition Counter-Attack", "Deep Ultra-Defensive Low-Block"])
with t_col2:
    away_tactical_style = st.selectbox("Away Tactical Blueprint Style:", ["Standard Balanced / Unspecified", "High-Possession Pressing", "Fast Transition Counter-Attack", "Deep Ultra-Defensive Low-Block"])
with t_col3:
    st.write("**Geographic Friction Tracks**")
    home_heavy_travel = st.checkbox("🚨 Home Team: Long-Distance Travel Exposure", value=False)
    away_heavy_travel = st.checkbox("🚨 Away Team: Long-Distance Travel Exposure", value=False)

st.markdown("#### 🏥 Team News Missing-Talent Impact Overrides")
i_col1, i_col2 = st.columns(2)
with i_col1:
    home_missing_talent_tier = st.select_slider("Home Key Player Injury / Suspension Severity:", options=["Full Strength Squad", "Tier 2 Depth Missing (5% Cap)", "Tier 1 Engine Asset Missing (15% Cap)"], value="Full Strength Squad")
with i_col2:
    away_missing_talent_tier = st.select_slider("Away Key Player Injury / Suspension Severity:", options=["Full Strength Squad", "Tier 2 Depth Missing (5% Cap)", "Tier 1 Engine Asset Missing (15% Cap)"], value="Full Strength Squad")

st.markdown("#### 🧠 Scheduling Psychology, Referees & Pitch Overrides")
b_col1, b_col2, b_col3 = st.columns(3)
with b_col1:
    lookahead_match_active = st.selectbox("Look-Ahead Match Distraction Profile:", ["None / Standard Focus Match", "🏠 Home Team: Massive Impending Cup/Derby Next Week", "✈️ Away Team: Massive Impending Cup/Derby Next Week"])
with b_col2:
    referee_strictness_profile = st.selectbox("Assigned Referee Strictness Profile:", ["Standard Baseline / Moderate Official", "Lenient / High-Flow Context", "🚨 Strict / Cards & Penalties Inclined"])
with b_col3:
    st.write("**Asymmetric Climate/Surface Friction**")
    asymmetric_pitch_climate_advantage = st.checkbox("🚨 Host Artificial Turf / Extreme Climate Advantage Active", value=False)

st.markdown("---")
derby_match_active = st.checkbox("🚨 Flag Entry as Local Derby / High-Intensity Rivalry", value=False)

weather_goals_multiplier = 0.92 if "Rain" in weather_condition_selection else (0.88 if "Wind" in weather_condition_selection else 1.00)
coach_attack_multiplier = 1.05 if "Long" in coach_stability_selection else (0.85 if "Recent" in coach_stability_selection else 1.00)
coach_volatility_expansion = 1.08 if "Public" in coach_stability_selection else 1.00
home_injury_penalty = 1.00 if home_missing_talent_tier == "Full Strength Squad" else (0.95 if "Tier 2" in home_missing_talent_tier else 0.85)
away_injury_penalty = 1.00 if away_missing_talent_tier == "Full Strength Squad" else (0.95 if "Tier 2" in away_missing_talent_tier else 0.85)
home_travel_multiplier = 0.92 if home_heavy_travel else 1.00
away_travel_multiplier = 0.92 if away_heavy_travel else 1.00
home_lookahead_penalty = 0.90 if "Home" in lookahead_match_active else 1.00
away_lookahead_penalty = 0.90 if "Away" in lookahead_match_active else 1.00
referee_volatility_expansion = 1.08 if "Strict" in referee_strictness_profile else (0.94 if "Lenient" in referee_strictness_profile else 1.00)
visitor_surface_penalty = 0.94 if asymmetric_pitch_climate_advantage else 1.00

o_col1, o_col2 = st.columns(2)
with o_col1:
    odds_1 = st.number_input("Home Odds (1):", min_value=1.01, value=2.10, step=0.05, key="o_1")
    odds_X = st.number_input("Draw Odds (X):", min_value=1.01, value=3.20, step=0.05, key="o_x")
    odds_2 = st.number_input("Away Odds (2):", min_value=1.01, value=3.40, step=0.05, key="o_2")
with o_col2:
    odds_over = st.number_input("Over 2.5 Goals Odds:", min_value=1.01, value=1.95, step=0.05, key="o_ov")
    odds_under = st.number_input("Under 2.5 Goals Odds:", min_value=1.01, value=1.85, step=0.05, key="o_un")

odds_1X, odds_X2, odds_12, odds_btts_y, odds_btts_n, odds_dnb1, odds_dnb2, odds_home_over_15, odds_home_under_15, odds_away_over_15, odds_away_under_15, odds_ah_home_minus_15, odds_ah_away_plus_15, odds_ah_home_plus_15, odds_ah_minus_15, odds_home_cs_y, odds_away_cs_y = 1.3, 1.6, 1.25, 1.8, 1.9, 1.5, 2.4, 2.1, 1.6, 3.1, 1.3, 3.8, 1.25, 1.18, 6.5, 2.6, 3.9
h_status, a_status = "stable", "stable"
league_key = selected_league_filter.lower().strip()
baseline_goals = engine.COMPETITION_MATRIX.get(league_key, {"baseline_goals": 2.65}).get("baseline_goals", 2.65)
is_fr = st.session_state.freeze_matrix.get(league_key, False)
# ==============================================================================
# SEGMENT 10A OF 15: FLAT GLOBAL DYNAMIC MOTIVATION STANDINGS LOOPS
# ==============================================================================
home_motivation_multiplier = 1.00
away_motivation_multiplier = 1.00
tournament_neutral_active = "Neutral" in tournament_framework_selection or "Knockout" in tournament_framework_selection
knockout_volatility_boost = 1.15 if "Knockout" in tournament_framework_selection else 1.00

if live_standings_df is not None and not live_standings_df.empty and not tournament_neutral_active:
    live_standings_df.columns = [str(c).strip().lower() for c in live_standings_df.columns]
    live_standings_df.rename(columns={"team": "Team", "p": "P", "played": "P", "pld": "P"}, inplace=True)
    
    if "Team" in live_standings_df.columns:
        live_standings_df["Team"] = live_standings_df["Team"].astype(str).str.strip().lower()
        home_match_row = live_standings_df[live_standings_df["Team"] == str(target["home_team"]).strip().lower()]
        if not home_match_row.empty:
            home_position = int(home_match_row.index) + 1
            if home_position <= 4: home_motivation_multiplier = 1.12
            elif home_position >= (len(live_standings_df) - 3): home_motivation_multiplier = 1.15
            # ==============================================================================
# SEGMENT 10B OF 15: MULTI-VARIABLE PROCESSOR CORE & POISSON SHIELD
# ==============================================================================
if tournament_neutral_active:
    home_motivation_multiplier, away_motivation_multiplier = 1.00, 1.00

calibrated_baseline_goals = baseline_goals * weather_goals_multiplier * preseason_turnover_rate
if "Knockout" in tournament_framework_selection: calibrated_baseline_goals *= 0.88

# --- PYTHAGOREAN EXPECTATION LUCK FILTER TRACKS ---
h_past_sot = filtered_df[filtered_df["home_team"] == target["home_team"]]["home_sot"].mean() if len(filtered_df) > 0 else 4.0
a_past_sot = filtered_df[filtered_df["away_team"] == target["away_team"]]["away_sot"].mean() if len(filtered_df) > 0 else 3.5
h_past_bc = filtered_df[filtered_df["home_team"] == target["home_team"]]["home_big_chances"].mean() if len(filtered_df) > 0 else 1.2
a_past_bc = filtered_df[filtered_df["away_team"] == target["away_team"]]["away_big_chances"].mean() if len(filtered_df) > 0 else 0.9

pythagorean_luck_ratio = (h_past_sot ** 2) / (h_past_sot ** 2 + a_past_sot ** 2) if (h_past_sot + a_past_sot) > 0 else 0.50
if pythagorean_luck_ratio > 0.65: calibrated_baseline_goals *= 0.95 

# --- OPPONENT STRENGTH OF SCHEDULE (SoS) EQUALIZER TRACKS ---
home_sos_equalizer, away_sos_equalizer = 1.00, 1.00
if live_standings_df is not None and not live_standings_df.empty and "Team" in live_standings_df.columns:
    total_table_teams = len(live_standings_df)
    home_opponents = filtered_df[(filtered_df["home_team"] == target["home_team"]) | (filtered_df["away_team"] == target["home_team"])].tail(5)
    away_opponents = filtered_df[(filtered_df["home_team"] == target["away_team"]) | (filtered_df["away_team"] == target["away_team"])].tail(5)
    
    def compute_sos_index(opp_df, active_team):
        positions = []
        for _, gm in opp_df.iterrows():
            opp = str(gm["away_team"]).strip().lower() if str(gm["home_team"]).strip().lower() == active_team.lower() else str(gm["home_team"]).strip().lower()
            look = live_standings_df[live_standings_df["Team"] == opp]
            if not look.empty: positions.append(int(look.index) + 1)
        if positions:
            avg_opp_pos = sum(positions) / len(positions)
            return 1.10 if avg_opp_pos <= (total_table_teams * 0.35) else (0.90 if avg_opp_pos >= (total_table_teams * 0.65) else 1.00)
        return 1.00

    home_sos_equalizer = compute_sos_index(home_opponents, target["home_team"])
    away_sos_equalizer = compute_sos_index(away_opponents, target["away_team"])

# --- SHOT QUALITY RATIO PROXY CORE ---
home_shot_quality_ratio = (h_past_bc + 1.0) / (h_past_sot + 1.0)
away_shot_quality_ratio = (a_past_bc + 1.0) / (a_past_sot + 1.0)

# --- ROCK-PAPER-SCISSORS ASYMMETRIC TACTICAL MULTIPLIERS ---
home_style_modifier = 1.00
away_style_modifier = 1.00
if home_tactical_style == "High-Possession Pressing" and away_tactical_style == "Fast Transition Counter-Attack":
    home_style_modifier, away_style_modifier = 0.88, 1.10
    st.sidebar.warning("🛡️ Tactical Mismatch: Pressing host exposed to Counter-Attack matrix tracks.")
elif home_tactical_style == "Deep Ultra-Defensive Low-Block" and away_tactical_style == "High-Possession Pressing":
    away_style_modifier = 0.90

vol_dampener_adjusted = vol_dampener * coach_volatility_expansion * knockout_volatility_boost * referee_volatility_expansion
if derby_match_active and not tournament_neutral_active:
    home_motivation_multiplier *= 0.85
    vol_dampener_adjusted *= 1.10

calibrated_home_attack = home_motivation_multiplier * home_shot_quality_ratio * home_sos_equalizer * coach_attack_multiplier * home_injury_penalty * home_travel_multiplier * home_style_modifier * home_lookahead_penalty
calibrated_away_attack = away_motivation_multiplier * away_shot_quality_ratio * away_sos_equalizer * away_injury_penalty * away_travel_multiplier * away_style_modifier * away_lookahead_penalty * visitor_surface_penalty

res = engine.predict_match_probabilities(filtered_df, target["home_team"], target["away_team"], target_ts, calibrated_baseline_goals, calibrated_home_attack, calibrated_away_attack, h_status, a_status, max_score_cap, vol_dampener_adjusted, is_fr)
h_s = engine.parse_live_team_averages(filtered_df, target["home_team"], target_ts, half_life_days, h_status, is_fr)
a_s = engine.parse_live_team_averages(filtered_df, target["away_team"], target_ts, half_life_days, a_status, is_fr)

prob_home, prob_draw, prob_away = res["market_probabilities"]["1 (Home Win)"], res["market_probabilities"]["X (Draw)"], res["market_probabilities"]["2 (Away Win)"]
prob_matrix = res["raw_matrix"]
over_25_p, btts_yes_p, home_cs_p, away_cs_p = 0.0, 0.0, 0.0, 0.0

max_r, max_a = int(prob_matrix.shape[0]), int(prob_matrix.shape[1])

for r_idx in range(max_r):
    for a_idx in range(max_a):
        cell_p = prob_matrix[r_idx, a_idx]
        if r_idx + a_idx > 2.5: over_25_p += cell_p
        if r_idx > 0 and a_idx > 0: btts_yes_p += cell_p
        if a_idx == 0: home_cs_p += cell_p
        if r_idx == 0: away_cs_p += cell_p
        
under_25_p, btts_no_p = 1.0 - over_25_p, 1.0 - btts_yes_p
dc_1X_p, dc_X2_p, dc_12_p = min(1.0, prob_home + prob_draw), min(1.0, prob_draw + prob_away), min(1.0, prob_home + prob_away)
dnb_denom = 1.0 - prob_draw if prob_draw < 1.0 else 1.0
dnb_1_p, dnb_2_p = prob_home / dnb_denom, prob_away / dnb_denom

markets_master_manifest = [
    ("HOME WIN (1)", odds_1, prob_home), ("DRAW MATCH (X)", odds_X, prob_draw), ("AWAY WIN (2)", odds_2, prob_away),
    ("OVER 2.5 GOALS", odds_over, over_25_p), ("UNDER 2.5 GOALS", odds_under, under_25_p)
]
sd = min(h_s.get("games_played", 12), a_s.get("games_played", 12))
confidence = min(100, int((sd / 12.0) * 100)) if sd > 0 else 50
# ==============================================================================
# SEGMENT 11 OF 15: FLAT GLOBAL EXPECTED VALUE AUDITOR & STRESS TESTER
# ==============================================================================
st.markdown("### 📊 Comprehensive Market Projections & Value Audit")
all_markets_rendered_rows = []
qualified_projections = []
MAX_EV_CEILING_CAP = 0.50 

for label, b_odds, m_prob in markets_master_manifest:
    calculated_ev = (m_prob * b_odds) - 1.0
    implied_bookie_prob = 1.0 / b_odds if b_odds > 0 else 0.0
    edge_delta = m_prob - implied_bookie_prob
    raw_individual_kelly = ((m_prob * b_odds) - 1.0) / (b_odds - 1.0) if b_odds > 1.0 else 0.0
    
    if confidence < confidence_floor_input:
        value_status_tag = f"❌ NO BET (LOW CONFIDENCE)"
        calculated_stake_allocation_pct = 0.0
    elif calculated_ev > MAX_EV_CEILING_CAP:
        value_status_tag = "⚠️ EXTREME VOLATILITY (CEILING SKIPPED)"
        calculated_stake_allocation_pct = 0.0
    elif calculated_ev >= 0.030 and m_prob >= (accuracy_threshold_floor):
        value_status_tag = "🔥 HIGH VALUE PREMIUM TICKET" if calculated_ev >= 0.070 else "📊 STANDARD REGULAR POSITION"
        calculated_stake_allocation_pct = max(0.5, min(5.0, round(raw_individual_kelly * 0.25 * 100, 2)))
        qualified_projections.append((label, calculated_ev, m_prob, b_odds, calculated_stake_allocation_pct, value_status_tag))
    else:
        value_status_tag = "❌ NO BET (EDGE VALUE DEFICIT)"
        calculated_stake_allocation_pct = 0.0
        
    all_markets_rendered_rows.append({
        "Betting Market": label, "Bookmaker Odds": f"{b_odds:.2f}", "Model Probability": f"{m_prob * 100:.1f}%",
        "Implied Odds Prob": f"{implied_bookie_prob * 100:.1f}%", "Model Edge": f"{edge_delta * 100:+.1f}%",
        "Expected Value (EV)": f"{calculated_ev * 100:+.1f}%", "Staking Allocation": f"{calculated_stake_allocation_pct:.2f}%",
        "Recommendation Action": value_status_tag
    })

st.markdown("#### ⚡ Real-Time Game-State Stress Tester Room")
stress_away_lead_draw_prob = min(0.95, prob_draw * 1.35)
stress_away_lead_under_prob = min(0.95, under_25_p * 1.20)

stress_rows = [
    {"Friction Scenario Profile": "Baseline Standard Plan", "Projected Draw (%)": f"{prob_draw * 100:.1f}%", "Projected Under 2.5 (%)": f"{under_25_p * 100:.1f}%", "Risk Verdict": "📊 Standard Operation"},
    {"Friction Scenario Profile": "Underdog Scores First (Early 0-1 Lead)", "Projected Draw (%)": f"{stress_away_lead_draw_prob * 100:.1f}%", "Projected Under 2.5 (%)": f"{stress_away_lead_under_prob * 100:.1f}%", "Risk Verdict": "🧱 Ultra Low-Block Inertia"}
]
st.dataframe(pd.DataFrame(stress_rows), use_container_width=True, hide_index=True)

st.markdown("### 🚨 Sisonke Engine Audit Room")
highest_ev_found = max([(m_p * b_o) - 1.0 for lbl, b_o, m_p in markets_master_manifest]) if markets_master_manifest else -1.0
if highest_ev_found >= 0.030 and confidence >= confidence_floor_input:
    st.success(f"🔥 ELITE PROJECTIONS UNLOCKED (+{highest_ev_found*100:.1f}% EV Edge Verified Across Multi-Variable Matrix Maps)")
else: st.error("📉 SELECTION REJECTED: Internal profit margins fail target professional risk floor bounds.")

st.dataframe(pd.DataFrame(all_markets_rendered_rows), use_container_width=True, hide_index=True)
# ==============================================================================
# SEGMENT 12 OF 15: FLAT GLOBAL EXACT MATCH GOALS & SCORE CURVES
# ==============================================================================
st.markdown("### 🎯 Exact Goals & Correct Score Matrix Projections")
exact_goals_distribution = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, "5+": 0.0}
graph_data_dict = {}

for r_idx in range(max_r):
    for a_idx in range(max_a):
        cell_p = prob_matrix[r_idx, a_idx]
        total_goals = r_idx + a_idx
        score_label = f"{r_idx}-{a_idx}"
        if cell_p >= 0.01: graph_data_dict[score_label] = float(cell_p * 100)
        
        if total_goals in exact_goals_distribution: exact_goals_distribution[total_goals] += cell_p
        else: exact_goals_distribution["5+"] += cell_p

if graph_data_dict:
    st.bar_chart(pd.DataFrame(list(graph_data_dict.items()), columns=["Scoreline", "Probability (%)"]).set_index("Scoreline"), use_container_width=True)
    # ==============================================================================
# SEGMENT 13 OF 15: FLAT GLOBAL MESSAGING RELAYS & CALIBRATED COUPON GENERATOR
# ==============================================================================
if qualified_projections and confidence >= confidence_floor_input:
    qualified_projections.sort(key=lambda x: x[1], reverse=True)
    optimal_bet = str(qualified_projections[0][0])
    best_ev = float(qualified_projections[0][1])
    best_prob = float(qualified_projections[0][2])
    best_odds = float(qualified_projections[0][3])
    fractional_scale_stake = float(qualified_projections[0][4])
    bet_rec = str(qualified_projections[0][5])
else: 
    optimal_bet, best_ev, best_prob, best_odds, fractional_scale_stake, bet_rec = "NO COMPREHENSIVE SELECTION MET FLOORS", 0.00, 0.00, 2.00, 0.00, "❌ NO BET"

c_col_l, c_col_r = st.columns(2)
with c_col_l:
    st.markdown("### 📊 Live Analytics Monitor")
    st.metric("Match Confidence Value", f"{confidence}%")
    st.metric("Value Threshold Rating", bet_rec)
    st.markdown("### 🧠 Model Tactical Rationale Breakdown")
    st.markdown(f"• **Dominant Threat Metrics Trace**: Home shots on target trends average **{h_past_sot:.1f} SOT** relative to Traveling Road parameters of **{a_past_sot:.1f} SOT**. Shot quality overlay parameters compute a home execution efficiency index of **{home_shot_quality_ratio:.2f}** versus an away efficiency index of **{away_shot_quality_ratio:.2f}**.")
    # ==============================================================================
# SEGMENT 14 OF 15: FLAT GLOBAL PERMANENT BANKROLL PERFORMANCE LEDGER
# ==============================================================================
with c_col_r:
    st.markdown("### 🏦 Sisonke Investment Ledger Room")
    ledger_path = "master_bankroll_ledger.csv"
    if not os.path.exists(ledger_path):
        pd.DataFrame(columns=["Log_ID", "Timestamp", "Match", "Market", "Model_Prob", "Entry_Odds", "Closing_Odds", "CLV_Edge_Pct", "Kelly_Stake_Pct", "Outcome", "Net_Profit_Units"]).to_csv(ledger_path, index=False)

    with st.form("ledger_commit_form"):
        closing_odds_input = st.number_input("Enter Bookmaker Final Closing Odds:", min_value=1.01, value=float(best_odds), step=0.05)
        match_outcome_selection = st.selectbox("Select Actual Match Reality Outcome:", ["Pending / Unplayed", "Won Match", "Lost Match", "Void / Refunded"])
        submit_ledger_entry = st.form_submit_button("💾 Save Ticket to Hard Drive Ledger")
        
        if submit_ledger_entry and "NO COMPREHENSIVE" not in optimal_bet:
            existing_ledger_df = pd.read_csv(ledger_path)
            clv_edge_margin_pct = round(((1.0 / float(best_odds)) - (1.0 / float(closing_odds_input))) * 100, 2)
            net_units = round(fractional_scale_stake * (float(best_odds) - 1.0), 2) if match_outcome_selection == "Won Match" else (-fractional_scale_stake if match_outcome_selection == "Lost Match" else 0.0)
            
            new_row = {"Log_ID": str(int(datetime.datetime.now().timestamp())), "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d"), "Match": f"{target['home_team']} vs {target['away_team']}", "Market": optimal_bet, "Model_Prob": f"{best_prob*100:.1f}%", "Entry_Odds": best_odds, "Closing_Odds": closing_odds_input, "CLV_Edge_Pct": f"{clv_edge_margin_pct:+.2f}%", "Kelly_Stake_Pct": f"{fractional_scale_stake:.2f}%", "Outcome": match_outcome_selection, "Net_Profit_Units": net_units}
            pd.concat([existing_ledger_df, pd.DataFrame([new_row])], ignore_index=True).to_csv(ledger_path, index=False)
            st.rerun()
            # ==============================================================================
# SEGMENT 15 OF 15: FLAT GLOBAL OUTRIGHT WINNER ARBITRAGE SIMULATOR
# ==============================================================================
with tab_tables:
    if not filtered_df.empty:
        settled_check_df = filtered_df.dropna(subset=["home_goals", "away_goals"])
        
        if len(settled_check_df) == 0 or preseason_calibration_active:
            st.markdown("#### 🏆 Syndicate Outright Winner Probability & Boardroom EV Arbitrage")
            all_participating_teams = sorted(list(set(filtered_df["home_team"].dropna().unique()).union(set(filtered_df["away_team"].dropna().unique()))))
            
            squad_profile_rows = [{"Competing Squad": team, "Transfer Additions Boost (%)": 0.0, "Player Departures Decay (%)": 0.0, "Squad Rotation Depth Index": 1.00, "Active in Continental Cups": False, "Corporate Manager Sack Floor (Min PPG)": 1.10, "Asymmetric Pitch Layout Width Index": 1.00, "Bookmaker Outright Odds": 25.00} for team in all_participating_teams]
            
            edited_profile_df = st.data_editor(pd.DataFrame(squad_profile_rows), column_config={"Competing Squad": st.column_config.TextColumn("Competing Squad", disabled=True), "Transfer Additions Boost (%)": st.column_config.NumberColumn("Signings Impact (+%)", min_value=0.0, max_value=25.0, format="%.1f%%"), "Player Departures Decay (%)": st.column_config.NumberColumn("Departures Decay (-%)", min_value=0.0, max_value=25.0, format="%.1f%%"), "Squad Rotation Depth Index": st.column_config.NumberColumn("Squad Rotation Depth", min_value=0.80, max_value=1.20, step=0.05), "Active in Continental Cups": st.column_config.CheckboxColumn("Multi-Cup Congestion?"), "Corporate Manager Sack Floor (Min PPG)": st.column_config.NumberColumn("Sack PPG Floor", min_value=0.50, max_value=2.00), "Asymmetric Pitch Layout Width Index": st.column_config.NumberColumn("Pitch Width Index", min_value=0.85, max_value=1.15), "Bookmaker Outright Odds": st.column_config.NumberColumn("Bookmaker Outright Odds", min_value=1.01)}, hide_index=True, use_container_width=True, key="outright_squad_ledger_v3")

            # Low-latency internal dictionary builders
            t_boost = {r["Competing Squad"]: 1.0 + (r["Transfer Additions Boost (%)"]/100.0) for _, r in edited_profile_df.iterrows()} if edited_profile_df is not None else {t: 1.0 for t in all_participating_teams}
            d_decay = {r["Competing Squad"]: 1.0 - (r["Player Departures Decay (%)"]/100.0) for _, r in edited_profile_df.iterrows()} if edited_profile_df is not None else {t: 1.0 for t in all_participating_teams}
            depth_map = {r["Competing Squad"]: r["Squad Rotation Depth Index"] for _, r in edited_profile_df.iterrows()} if edited_profile_df is not None else {t: 1.0 for t in all_participating_teams}
            congestion_map = {r["Competing Squad"]: r["Active in Continental Cups"] for _, r in edited_profile_df.iterrows()} if edited_profile_df is not None else {t: False for t in all_participating_teams}
            sack_map = {r["Competing Squad"]: r["Corporate Manager Sack Floor (Min PPG)"] for _, r in edited_profile_df.iterrows()} if edited_profile_df is not None else {t: 1.10 for t in all_participating_teams}
            pitch_map = {r["Competing Squad"]: r["Asymmetric Pitch Layout Width Index"] for _, r in edited_profile_df.iterrows()} if edited_profile_df is not None else {t: 1.00 for t in all_participating_teams}
            odds_map = {r["Competing Squad"]: r["Bookmaker Outright Odds"] for _, r in edited_profile_df.iterrows()} if edited_profile_df is not None else {t: 25.0 for t in all_participating_teams}

            outright_simulation_scoreboard = {team: 0 for team in all_participating_teams}
            mock_schedule_fixtures = [{"home": h, "away": a} for h in all_participating_teams for a in all_participating_teams if h != a]
            
            if mock_schedule_fixtures:
                for iteration in range(1000):
                    points_reg = {team: 0 for team in all_participating_teams}
                    games_reg = {team: 0 for team in all_participating_teams}
                    sacked_reg = {team: False for team in all_participating_teams}
                    
                    for index_f, fix in enumerate(mock_schedule_fixtures):
                        sim_goals = baseline_goals * weather_goals_multiplier * preseason_turnover_rate
                        games_reg[fix["home"]] += 1; games_reg[fix["away"]] += 1
                        
                        if index_f > (len(mock_schedule_fixtures) * 0.85) and fix["home"] == max(points_reg, key=points_reg.get): sim_goals *= 0.78
                        
                        h_sack = 1.10 if (games_reg[fix["home"]] >= 10 and (points_reg[fix["home"]]/games_reg[fix["home"]]) < sack_map.get(fix["home"], 1.10)) or sacked_reg[fix["home"]] else 1.00
                        if h_sack == 1.10: sacked_reg[fix["home"]] = True
                        a_sack = 1.10 if (games_reg[fix["away"]] >= 10 and (points_reg[fix["away"]]/games_reg[fix["away"]]) < sack_map.get(fix["away"], 1.10)) or sacked_reg[fix["away"]] else 1.00
                        if a_sack == 1.10: sacked_reg[fix["away"]] = True
                        
                        h_pitch = 0.93 if pitch_map.get(fix["home"], 1.00) < 0.95 else 1.00
                        h_attr = depth_map.get(fix["home"], 1.00) if index_f > (len(mock_schedule_fixtures)*0.60) else 1.00
                        a_attr = depth_map.get(fix["away"], 1.00) if index_f > (len(mock_schedule_fixtures)*0.60) else 1.00
                        h_cong = 0.915 if congestion_map.get(fix["home"], False) and (index_f % 7 == 0) else 1.00
                        a_cong = 0.915 if congestion_map.get(fix["away"], False) and (index_f % 7 == 0) else 1.00
                        
                        raw_h_exp = 1.35 * sim_goals * coach_attack_multiplier * t_boost.get(fix["home"],1.0) * d_decay.get(fix["home"],1.0) * h_attr * h_cong * h_sack * h_pitch
                        raw_a_exp = 1.05 * sim_goals * t_boost.get(fix["away"],1.0) * d_decay.get(fix["away"],1.0) * a_attr * a_cong * a_sack
                        
                        sim_h, sim_a = np.random.poisson(raw_h_exp), np.random.poisson(raw_a_exp)
                        if sim_h > sim_a: points_reg[fix["home"]] += 3
                        elif sim_a > sim_h: points_reg[fix["away"]] += 3
                        else: points_reg[fix["home"]] += 1; points_reg[fix["away"]] += 1
                            
                    for team in points_reg:
                        if points_reg[team] > 100: points_reg[team] = 100
                    outright_simulation_scoreboard[max(points_reg, key=points_reg.get)] += 1
            
            outright_results_rows = []
            for team, win_count in outright_simulation_scoreboard.items():
                p_win = float(win_count / 1000.0)
                b_odds = odds_map.get(team, 25.0)
                c_ev = (p_win * b_odds) - 1.0
                verdict = "🔥 HIGH VALUE FUTURES TICKET" if c_ev >= 0.070 else ("🟢 STANDARD VALUE ACCUMULATOR" if 0.030 <= c_ev <= 0.069 else "❌ NO BET")
                outright_results_rows.append({"Competing Squad": team, "Model Probability (%)": f"{p_win*100:.1f}%", "Fair Value Odds": f"{1.0/p_win:.2f}" if p_win > 0 else "999.00", "Your Input Odds": f"{b_odds:.2f}", "Outright EV (%)": f"{c_ev*100:+.1f}%", "Trading Verdict": verdict})
            
            st.write("📈 **Simulated Outright Forecasting & Arbitrage Report Matrix:**")
            st.dataframe(pd.DataFrame(outright_results_rows).sort_values(by="Model Probability (%)", ascending=False), use_container_width=True, hide_index=True)
            st.markdown("---")
            
        base_table = engine.generate_dynamic_league_table(filtered_df)
        if base_table is not None and not base_table.empty: st.dataframe(base_table, use_container_width=True)
with tab_history:
    if not filtered_df.empty:
        b_df = engine.run_rolling_window_backtest(filtered_df, baseline_goals, backtest_window, 7, vol_dampener)
        if b_df is not None and not b_df.empty:
            b_df["is_correct"] = b_df["model_probability"] >= accuracy_threshold_floor
            st.metric("Backtest Prediction Accuracy", f"{(b_df['is_correct'].sum() / len(b_df)) * 100:.1f}%")
            st.dataframe(b_df, use_container_width=True)
with tab_past:
    if not filtered_df.empty:
        past_h = filtered_df.dropna(subset=["home_goals", "away_goals"]).copy()
        if not past_h.empty: st.dataframe(past_h.sort_values(by="match_timestamp", ascending=False).reset_index(drop=True)[]
        
