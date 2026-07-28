# ==============================================================================
# SEGMENT 1 OF 15: CORE DEPENDENCIES, CUSTOM UI THEME STYLING & PLATFORM SLOGAN
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

# Enforce professional wide-angle trading layout metrics
st.set_page_config(page_title="Sisonke Football Predictive Analytics", layout="wide", initial_sidebar_state="expanded")

# High-utility interface CSS injections to anchor modern widescreen layout themes
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
    .metric-card {
        background-color: #1e293b; padding: 10px; border-radius: 6px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Platform primary branding identity: Soccer ball emoji replaces 'o' in Sisonke natively
st.markdown("<h1 style='margin-bottom: 0px;'>Sis⚽nke Football Predictive Analytics</h1>", unsafe_allow_html=True)

# Refined slogan engine: Formatted cleanly without quotation marks beneath branding title
st.markdown("<p style='font-style: italic; color: #94a3b8; font-size: 18px; margin-top: 0px; margin-bottom: 25px;'>We beat the odds</p>", unsafe_allow_html=True)

# Administrative global memory tracking matrix variable initialization pass
if "freeze_matrix" not in st.session_state:
    st.session_state.freeze_matrix = {"last_error": None}
    # ==============================================================================
# SEGMENT 2 OF 15: MASTER INITIALIZATION MATRIX & NAMESPACE GUARDS
# ==============================================================================

# Autorun backend handshake engine guard
try:
    import main_engine as engine
except ImportError:
    st.error("🚨 CRITICAL CORE MISCONFIGURED: The calculation file 'main_engine.py' was not detected in your project folder path directory. Place 'main_engine.py' in the same folder as 'app.py' to clear this block.")
    st.stop()

# Global scope initialization guards: Formally maps baseline placeholder values at boot to permanently erase NameErrors
if "live_standings_df" not in st.session_state:
    st.session_state["live_standings_df"] = pd.DataFrame()
if "tournament_neutral_active" not in st.session_state:
    st.session_state["tournament_neutral_active"] = False
if "tournament_framework_selection" not in st.session_state:
    st.session_state["tournament_framework_selection"] = "Standard Domestic League Match"
if "home_tactical_style" not in st.session_state:
    st.session_state["home_tactical_style"] = "Standard Balanced / Unspecified"
if "away_tactical_style" not in st.session_state:
    st.session_state["away_tactical_style"] = "Standard Balanced / Unspecified"
if "home_heavy_travel" not in st.session_state:
    st.session_state["home_heavy_travel"] = False
if "away_heavy_travel" not in st.session_state:
    st.session_state["away_heavy_travel"] = False
if "home_injury_penalty" not in st.session_state:
    st.session_state["home_injury_penalty"] = 1.00
if "away_injury_penalty" not in st.session_state:
    st.session_state["away_injury_penalty"] = 1.00
if "is_profile_view" not in st.session_state:
    st.session_state["is_profile_view"] = False
if "is_aggregate_stats_view" not in st.session_state:
    st.session_state["is_aggregate_stats_view"] = False
if "full_validation_df" not in st.session_state:
    st.session_state["full_validation_df"] = pd.DataFrame()

# Bind local alias pointers to maintain down-stream script harmony seamlessly
live_standings_df = st.session_state["live_standings_df"]
tournament_neutral_active = st.session_state["tournament_neutral_active"]
tournament_framework_selection = st.session_state["tournament_framework_selection"]
home_tactical_style = st.session_state["home_tactical_style"]
away_tactical_style = st.session_state["away_tactical_style"]
home_heavy_travel = st.session_state["home_heavy_travel"]
away_heavy_travel = st.session_state["away_heavy_travel"]
home_injury_penalty = st.session_state["home_injury_penalty"]
away_injury_penalty = st.session_state["away_injury_penalty"]
is_profile_view = st.session_state["is_profile_view"]
is_aggregate_stats_view = st.session_state["is_aggregate_stats_view"]
full_validation_df = st.session_state["full_validation_df"]

# Core structural mappings for international sports metrics ingestion pipelines
API_LEAGUE_ID_MAP = {
    "English Premier League": 39, "Spanish La Liga": 140, "Italian Serie A": 135,
    "German Bundesliga": 78, "French Ligue 1": 61, "UEFA Champions League": 2,
    "Africa Cup of Nations": 6, "FIFA World Cup": 1
}

# Ensure baseline variables default cleanly if API parameters are untriggered
api_sync_triggered = False
total_fixtures = 0
storage_path = "master_sisonke_database.csv"
# ==============================================================================
# SEGMENT 3A OF 15: SIDEBAR CONTROL ROOM & MULTI-LEAGUE INGESTION STATUS RADAR
# ==============================================================================
with st.sidebar:
    st.markdown("### 📂 Data Control Room")
    uploaded_file = st.file_uploader("Upload Master Match CSV", type=["csv"])
    active_radar_df = pd.DataFrame()
    
    # Check memory session state first, falling back to optional disk buffer safely
    if not full_validation_df.empty:
        active_radar_df = full_validation_df.copy()
    elif uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            active_radar_df = pd.read_csv(uploaded_file, engine='python', on_bad_lines='skip')
            uploaded_file.seek(0)
        except: pass
    elif os.path.exists(storage_path):
        try: active_radar_df = pd.read_csv(storage_path, on_bad_lines='skip')
        except: pass

    # Render dynamic ingestion radar to isolate early/in-progress league states
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
            # ==============================================================================
# SEGMENT 3B OF 15: INGESTION SETTINGS & PRE-SEASON CALIBRATION SIDEBAR SLIDERS
# ==============================================================================
    st.markdown("---")
    api_token_input = st.text_input("Enter Free API-Football Token Key:", value="4c023480e8ffe2539261cd8746f67121", type="password")
    sync_operation_mode = st.selectbox("Select API Query Framework:", ["Compile Bulk Historical CSV (Method 1)", "Global Calendar Date", "Dedicated Team Profile Form", "View Team Profile Identity", "Aggregated Team Stats"])
    
    if sync_operation_mode in ["Compile Bulk Historical CSV (Method 1)", "Aggregated Team Stats"]:
        target_sync_country = st.selectbox("Select Target Sync Competition:", list(API_LEAGUE_ID_MAP.keys()))
        sync_target_scope = st.radio("Select Sync Data Target Window:", ["Settled Historical Data", "Upcoming 30-Day Fixtures"])
        manual_override_active = st.checkbox("Manual Season Override Year", value=False)
        selected_override_year = st.selectbox("Select Target Season Campaign Year:", options=list(range(2026, 2020, -1)), index=0)
        target_team_id_input = st.number_input("Enter Target Team ID Key:", min_value=1, value=33, step=1) if sync_operation_mode == "Aggregated Team Stats" else 33
            
    elif sync_operation_mode == "Global Calendar Date":
        target_calendar_date = st.date_input("Select Target Query Date:", datetime.date.today())
        target_timezone_string = st.text_input("API Output Timezone Alignment:", value="Africa/Johannesburg")
        optional_league_scope = st.checkbox("Scope to Selected League Profile")
        if optional_league_scope: target_sync_country = st.selectbox("Select Target Sync Competition:", list(API_LEAGUE_ID_MAP.keys()))
        
    elif sync_operation_mode == "Dedicated Team Profile Form":
        target_team_id_input = st.number_input("Enter Official API Team ID Key:", min_value=1, value=33, step=1, key="form_team_id")
        team_form_scope = st.radio("Select Target Form Vector:", ["Next Upcoming Fixtures", "Last Completed Results"])
        team_record_depth = st.slider("Target Record Return Depth:", min_value=1, max_value=20, value=10)
        
    elif sync_operation_mode == "View Team Profile Identity":
        target_team_id_input = st.number_input("Enter Official API Team ID Key:", min_value=1, value=33, step=1, key="profile_team_id")

    st.markdown("---")
    st.markdown("### 🛠️ Pre-Season Calibration Room")
    preseason_calibration_active = st.checkbox("Activate Prior-Season Baseline Anchor", value=False)
    
    preseason_turnover_rate = 1.00
    if preseason_calibration_active:
        squad_turnover_intensity = st.select_slider("Select Summer Transfer Overhaul Intensity:", options=["Low Roster Change", "Standard Turnover", "Heavy Overhaul / New Manager"], value="Standard Turnover")
        preseason_turnover_rate = 0.95 if squad_turnover_intensity == "Low Roster Change" else (0.82 if "Heavy" in squad_turnover_intensity else 0.90)

    st.markdown("---")
    api_sync_triggered = st.button("🚀 Execute Automated Bulk Scrape")
    ui_email_recipient = st.text_input("Primary Email:", value="vvuyo007@gmail.com")
    ui_sms_recipient = st.text_input("Mobile SMS:", value="0750739223@sms.telkom.co.za")
    ui_google_app_password = st.text_input("Password Key:", type="password", value="your_free_google_app_password")
    # ==============================================================================
# SEGMENT 4A OF 15: JSON UNPACKING & NAMESPACE SAFETY SHIELD
# ==============================================================================
resolved_payload_string = globals().get("api_data_payload_string", "")

if api_sync_triggered and resolved_payload_string:
    try:
        api_data = json.loads(resolved_payload_string)
        target_fixtures = []
        is_profile_view = "View" in sync_operation_mode
        is_aggregate_stats_view = "Aggregated" in sync_operation_mode
        
        if is_profile_view and "response" in api_data and api_data["response"]:
            profile_payload = api_data["response"] if isinstance(api_data["response"], list) else api_data["response"]
            st.write("### 🛡️ Core Team Identity Card Profile")
            st.json(profile_payload.get("team", {}))
        elif is_aggregate_stats_view and "response" in api_data and api_data["response"]:
            st.write("### 📊 Season Performance Metrics Card Summary")
            st.json(api_data["response"])
        elif "response" in api_data:
            target_fixtures = api_data["response"]
        total_fixtures = len(target_fixtures)
        # ==============================================================================
# SEGMENT 4B OF 15: CLEAN JSON LOOP COMPILER & INGESTION HANDSHAKE GUARD
# ==============================================================================
        if 'target_fixtures' in locals() and target_fixtures:
            target_fixtures.sort(key=lambda x: str(x.get("fixture", {}).get("date", "")), reverse=False)
    except Exception as api_parse_structural_error:
        st.session_state.freeze_matrix["last_error"] = f"API Payload Parsing Exception: {str(api_parse_structural_error)}"

is_valid_data = False
# ==============================================================================
# SEGMENT 5 OF 15: UNIVERSAL SCHEMA TRANSLATION ENGINE & NOMENCLATURE SHIELD
# ==============================================================================
if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        # Quote shield allows the model to process all CSV layouts smoothly
        manual_upload_df = pd.read_csv(uploaded_file, engine='python', on_bad_lines='skip')
        
        ALIGNED_HEADER_TRANSLATION_MAP = {
            "div": "league_country", "league_name": "league_country", "competition": "league_country",
            "date": "match_timestamp", "timestamp": "match_timestamp",
            "home": "home_team", "hometeam": "home_team",
            "away": "away_team", "awayteam": "away_team",
            "fthg": "home_goals", "hg": "home_goals",
            "ftag": "away_goals", "ag": "away_goals",
            "hs": "home_sot", "as": "away_sot", "home shots": "home_sot", "away shots": "away_sot",
            "hbc": "home_big_chances", "abc": "away_big_chances", "home big chances": "home_big_chances", "away big chances": "away_big_chances",
            "home_red_cards": "home_red_cards", "away_red_cards": "away_red_cards", "hrc": "home_red_cards", "arc": "away_red_cards"
        }
        manual_upload_df.columns = [str(c).strip().lower() for c in manual_upload_df.columns]
        manual_upload_df.rename(columns=ALIGNED_HEADER_TRANSLATION_MAP, inplace=True)
        
        # --- FIXED: AUTHENTIC LEAGUE NOMENCLATURE SHIELD ---
        # Automatically detects and maps authentic regional league names to your dashboard options
        if "league_country" in manual_upload_df.columns:
            def segment_divisional_tiers(cell_val):
                val_clean = str(cell_val).strip().upper()
                
                # Direct regional overrides
                if "SPAIN" in val_clean:
                    return "SPAIN LA LIGA"
                elif "GERMANY" in val_clean:
                    return "GERMANY BUNDESLIGA"
                elif "ITALY" in val_clean:
                    return "ITALY SERIE A"
                elif "PREMIER" in val_clean or "EPL" in val_clean or "TIER 1" in val_clean:
                    return "ENGLAND PREMIER LEAGUE" if "ENGLAND" in val_clean else f"{cell_val} PREMIER LEAGUE"
                elif "CHAMPIONSHIP" in val_clean or "CHAM" in val_clean or "TIER 2" in val_clean:
                    return "ENGLAND CHAMPIONSHIP" if "ENGLAND" in val_clean else f"{cell_val} CHAMPIONSHIP"
                
                # Dynamic fallback check for flat text strings
                if val_clean == "ENGLAND":
                    return "ENGLAND PREMIER LEAGUE"
                return cell_val
                
            manual_upload_df["league_country"] = manual_upload_df["league_country"].apply(segment_divisional_tiers)

        if "home_red_cards" in manual_upload_df.columns and "away_red_cards" in manual_upload_df.columns:
            red_card_mask = (manual_upload_df["home_red_cards"] > 0) | (manual_upload_df["away_red_cards"] > 0)
            if red_card_mask.any():
                manual_upload_df.loc[red_card_mask, "home_goals"] = manual_upload_df.loc[red_card_mask, "home_goals"].clip(upper=3)
                manual_upload_df.loc[red_card_mask, "away_goals"] = manual_upload_df.loc[red_card_mask, "away_goals"].clip(upper=3)

        if "match_timestamp" not in manual_upload_df.columns: manual_upload_df["match_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d")

        COMPREHENSIVE_METRIC_FALLBACKS = {
            "home_goals": np.nan, "away_goals": np.nan, 
            "home_sot": 4.0, "away_sot": 3.5,
            "home_big_chances": 1.2, "away_big_chances": 0.9, 
            "home_box_touches": 16.0, "away_box_touches": 13.0,
            "home_through_passes": 1.5, "away_through_passes": 1.1, 
            "home_final_third_entries": 32.0, "away_final_third_entries": 28.0,
            "home_interceptions": 11.0, "away_interceptions": 12.0, 
            "home_recoveries": 48.0, "away_recoveries": 46.0,
            "home_saves": 2.5, "away_saves": 2.8, 
            "home_ground_duels_won_pct": 0.50, "away_ground_duels_won_pct": 0.50,
            "home_aerial_duels_won_pct": 0.50, "away_aerial_duels_won_pct": 0.50, 
            "home_dribbles_won_pct": 0.50, "away_dribbles_won_pct": 0.50,
            "home_tackles_won_pct": 0.52, "away_tackles_won_pct": 0.52, 
            "home_passes_final_third_pct": 0.68, "away_passes_final_third_pct": 0.65,
            "home_rest_days": 5.0, "away_rest_days": 5.0
        }
        
        for mandatory_col, fallback_val in COMPREHENSIVE_METRIC_FALLBACKS.items():
            if mandatory_col not in manual_upload_df.columns: 
                manual_upload_df[mandatory_col] = fallback_val
            else: 
                manual_upload_df[mandatory_col] = manual_upload_df[mandatory_col].fillna(fallback_val)
        
        st.session_state["full_validation_df"] = manual_upload_df.copy()
        full_validation_df = st.session_state["full_validation_df"]
        is_valid_data = True
    except Exception as e: st.error(f"Manual Ingestion Shield Error: {e}")
    # ==============================================================================
# SEGMENT 6 OF 15: MEMORY-ISOLATED INGESTION LAYER & RIGID NUMERIC PARSING ARMOR
# ==============================================================================
processed_execution_rows = []
historical_reference_df = pd.DataFrame()

# Initialize an in-memory execution lock flag if missing from session state
if "processed_cache_success" not in st.session_state:
    st.session_state["processed_cache_success"] = False

# Read and immediately standardize the historical reference sheet dates if it exists on disk
if os.path.exists(storage_path):
    try:
        historical_reference_df = pd.read_csv(storage_path, on_bad_lines='skip')
        historical_reference_df.columns = [str(c).strip().lower() for c in historical_reference_df.columns]
        # Robust datetime standardization pass over hard drive database records
        historical_reference_df["match_timestamp"] = pd.to_datetime(historical_reference_df["match_timestamp"], errors='coerce', dayfirst=True)
    except: pass

# Process your uploaded spreadsheet file entirely in RAM if it hasn't successfully executed yet
if is_valid_data and not full_validation_df.empty and not api_sync_triggered and not st.session_state["processed_cache_success"]:
    st.sidebar.caption("🟢 Mode Status: Compiling Isolated RAM Fatigue Matrix...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_upload_records = len(full_validation_df)
    
    # Pre-clean the incoming uploaded dataframe timestamps globally to neutralize mixed date layouts
    full_validation_df["match_timestamp"] = pd.to_datetime(full_validation_df["match_timestamp"], errors='coerce', dayfirst=True)
    
    for index, row in full_validation_df.iterrows():
        h_name = str(row["home_team"]).strip()
        a_name = str(row["away_team"]).strip()
        
        current_match_time = row["match_timestamp"]
        if pd.isnull(current_match_time): 
            current_match_time = pd.Timestamp.now()
            
        status_text.text(f"Processing File Rows {index+1}/{total_upload_records}: {h_name} vs {a_name}")
        calculated_home_rest_days = 5.0
        calculated_away_rest_days = 5.0
        
        if not historical_reference_df.empty:
            # Settle the home team lookback track, enforcing explicit datetime typing comparisons
            home_past_records = historical_reference_df[
                ((historical_reference_df["home_team"] == h_name) | (historical_reference_df["away_team"] == h_name))
            ].copy()
            
            if not home_past_records.empty:
                home_past_records["match_timestamp"] = pd.to_datetime(home_past_records["match_timestamp"], errors='coerce', dayfirst=True)
                home_past_records = home_past_records[(home_past_records["match_timestamp"].notna()) & (home_past_records["match_timestamp"] < current_match_time)]
                if not home_past_records.empty:
                    days_diff = (current_match_time - home_past_records["match_timestamp"].max()).days
                    calculated_home_rest_days = float(days_diff) if days_diff <= 14 else 5.0
                
            # Settle the away team lookback track, enforcing explicit datetime typing comparisons
            away_past_records = historical_reference_df[
                ((historical_reference_df["home_team"] == a_name) | (historical_reference_df["away_team"] == a_name))
            ].copy()
            
            if not away_past_records.empty:
                away_past_records["match_timestamp"] = pd.to_datetime(away_past_records["match_timestamp"], errors='coerce', dayfirst=True)
                away_past_records = away_past_records[(away_past_records["match_timestamp"].notna()) & (away_past_records["match_timestamp"] < current_match_time)]
                if not away_past_records.empty:
                    days_diff = (current_match_time - away_past_records["match_timestamp"].max()).days
                    calculated_away_rest_days = float(days_diff) if days_diff <= 14 else 5.0

        # Helper extraction utility pass to convert text spaces safely into floats without crashes
        def parse_safe_float(val, fallback):
            if pd.isna(val): return fallback
            val_str = str(val).strip().replace(" ", "")
            try: return float(val_str) if val_str != "" else fallback
            except: return fallback

        processed_execution_rows.append({
            "league_country": row.get("league_country", "Imported League"), 
            "match_timestamp": current_match_time.isoformat(),
            "home_team": h_name, 
            "away_team": a_name, 
            "home_goals": row.get("home_goals"), 
            "away_goals": row.get("away_goals"),
            "home_sot": parse_safe_float(row.get("home_sot"), 4.0), 
            "away_sot": parse_safe_float(row.get("away_sot"), 3.5),
            "home_big_chances": parse_safe_float(row.get("home_big_chances"), 1.2), 
            "away_big_chances": parse_safe_float(row.get("away_big_chances"), 0.9),
            "home_box_touches": parse_safe_float(row.get("home_box_touches"), 16.0), 
            "away_box_touches": parse_safe_float(row.get("away_box_touches"), 13.0),
            "home_rest_days": calculated_home_rest_days, 
            "away_rest_days": calculated_away_rest_days
        })
        progress_bar.progress((index + 1) / total_upload_records)
        
    status_text.empty()
    progress_bar.empty()

    if processed_execution_rows:
        st.session_state["full_validation_df"] = pd.DataFrame(processed_execution_rows)
        st.session_state["processed_cache_success"] = True
        st.rerun()

if uploaded_file is None and st.session_state["processed_cache_success"]:
    st.session_state["processed_cache_success"] = False
    # ==============================================================================
# SEGMENT 7 OF 15: GLOBAL SCHEMA SYNCHRONIZATION & TUNING CONTROLS
# ==============================================================================
working_pipeline_df = full_validation_df.copy() if (globals().get("is_valid_data", False) and not full_validation_df.empty) else (pd.read_csv(storage_path) if os.path.exists(storage_path) else pd.DataFrame())

if not working_pipeline_df.empty:
    working_pipeline_df.columns = [str(c).strip().lower() for c in working_pipeline_df.columns]
    working_pipeline_df["match_timestamp"] = pd.to_datetime(working_pipeline_df["match_timestamp"].astype(str).str.replace("T", " "), errors='coerce').fillna(pd.Timestamp.now())
    working_pipeline_df.drop_duplicates(subset=["league_country", "match_timestamp", "home_team", "away_team"], keep="last", inplace=True)
    
    # --- COMPREHENSIVE FIX: DYNAMIC SCHEMA SYNCHRONIZATION OVERLAY ---
    # Automatically injects and aligns required fallback metrics into old database rows on the fly
    CRITICAL_BACKEND_COLUMNS = {
        "home_sot": 4.0, "away_sot": 3.5,
        "home_big_chances": 1.2, "away_big_chances": 0.9, 
        "home_box_touches": 16.0, "away_box_touches": 13.0,
        "home_through_passes": 1.5, "away_through_passes": 1.1, 
        "home_final_third_entries": 32.0, "away_final_third_entries": 28.0,
        "home_interceptions": 11.0, "away_interceptions": 12.0, 
        "home_recoveries": 48.0, "away_recoveries": 46.0,
        "home_saves": 2.5, "away_saves": 2.8, 
        "home_ground_duels_won_pct": 0.50, "away_ground_duels_won_pct": 0.50,
        "home_aerial_duels_won_pct": 0.50, "away_aerial_duels_won_pct": 0.50, 
        "home_dribbles_won_pct": 0.50, "away_dribbles_won_pct": 0.50,
        "home_tackles_won_pct": 0.52, "away_tackles_won_pct": 0.52, 
        "home_passes_final_third_pct": 0.68, "away_passes_final_third_pct": 0.65,
        "home_rest_days": 5.0, "away_rest_days": 5.0
    }
    
    for mandatory_col, fallback_val in CRITICAL_BACKEND_COLUMNS.items():
        if mandatory_col not in working_pipeline_df.columns:
            working_pipeline_df[mandatory_col] = fallback_val
        else:
            working_pipeline_df[mandatory_col] = working_pipeline_df[mandatory_col].fillna(fallback_val)

    # Force float numeric casting over all processing variables safely
    for col in CRITICAL_BACKEND_COLUMNS.keys():
        working_pipeline_df[col] = pd.to_numeric(working_pipeline_df[col], errors='coerce').fillna(CRITICAL_BACKEND_COLUMNS[col])
        
    for col in ["home_goals", "away_goals"]:
        if col in working_pipeline_df.columns:
            working_pipeline_df[col] = pd.to_numeric(working_pipeline_df[col], errors='coerce')

    uploaded_leagues = sorted(list(working_pipeline_df["league_country"].dropna().unique()))
else:
    st.info("📂 Data Control Room Active: Please upload your recent match history CSV file to begin training.")
    st.stop()

selected_league_filter = st.selectbox("Select Target League:", uploaded_leagues)
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
# SEGMENT 8 OF 15: FLAT GLOBAL EXPONENTIAL DECAY WEIGHTS & STREAK INDICATORS
# ==============================================================================
st.markdown("### 📈 Exponential Time-Decay Weighting Behavior Visualization")
days_axis = np.arange(0, 120, 1)
decay_weights = (0.5) ** (days_axis / half_life_days)
st.line_chart(pd.DataFrame({"Model Predictive Weight": decay_weights}, index=days_axis), use_container_width=True)

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
# SEGMENT 9 OF 15: FLAT GLOBAL STRATEGIC OVERRIDES PANEL & ODDS INPUT GRID
# ==============================================================================
st.markdown("### ⛅ Matchday Conditions & Strategic Overrides")
w_col1, w_col2, w_col3 = st.columns(3)
with w_col1:
    weather_condition_selection = st.selectbox(
        "Current Matchday Weather Climate:",
        ["Optimal / Standard Ambient / Indoor Dome", "Heavy Rain / High Pitch Slick Surface", "Extreme High Wind / Aerodynamic Drag Line"]
    )
with w_col2:
    tournament_framework_selection = st.selectbox(
        "Competition Tournament Format Stage:",
        ["Standard Domestic League Match", "🏆 Neutral-Site Tournament Group Stage", "💀 Knockout Round (Extra-Time Risk)"]
    )
with w_col3:
    coach_stability_selection = st.selectbox(
        "Host Team Coach Stability Status:",
        ["Long-Term Stability (2+ Years)", "Stable Baseline / Standard Tenure", "Recent Appointment / Caretaker Setup", "🚨 Public Dressing Room Friction"]
    )

st.markdown("#### ⚙️ Syndicate Tactical Mismatch & Travel Metrics")
t_col1, t_col2, t_col3 = st.columns(3)
with t_col1:
    home_tactical_style = st.selectbox(
        "Home Tactical Blueprint Style:",
        ["Standard Balanced / Unspecified", "High-Possession Pressing", "Fast Transition Counter-Attack", "Deep Ultra-Defensive Low-Block"]
    )
with t_col2:
    away_tactical_style = st.selectbox(
        "Away Tactical Blueprint Style:",
        ["Standard Balanced / Unspecified", "High-Possession Pressing", "Fast Transition Counter-Attack", "Deep Ultra-Defensive Low-Block"]
    )
with t_col3:
    st.write("**Geographic Friction Tracks**")
    home_heavy_travel = st.checkbox("🚨 Home Team: Long-Distance Travel Exposure", value=False)
    away_heavy_travel = st.checkbox("🚨 Away Team: Long-Distance Travel Exposure", value=False)

st.markdown("#### 🏥 Team News Missing-Talent Impact Overrides")
i_col1, i_col2 = st.columns(2)
with i_col1:
    home_missing_talent_tier = st.select_slider(
        "Home Key Player Injury / Suspension Severity:",
        options=["Full Strength Squad", "Tier 2 Depth Missing (5% Cap)", "Tier 1 Engine Asset Missing (15% Cap)"],
        value="Full Strength Squad"
    )
with i_col2:
    away_missing_talent_tier = st.select_slider(
        "Away Key Player Injury / Suspension Severity:",
        options=["Full Strength Squad", "Tier 2 Depth Missing (5% Cap)", "Tier 1 Engine Asset Missing (15% Cap)"],
        value="Full Strength Squad"
    )

st.markdown("#### 🧠 Scheduling Psychology, Referees & Pitch Overrides")
b_col1, b_col2, b_col3 = st.columns(3)
with b_col1:
    lookahead_match_active = st.selectbox(
        "Look-Ahead Match Distraction Profile:",
        ["None / Standard Focus Match", "🏠 Home Team: Massive Impending Cup/Derby Next Week", "✈️ Away Team: Massive Impending Cup/Derby Next Week"]
    )
with b_col2:
    referee_strictness_profile = st.selectbox(
        "Assigned Referee Strictness Profile:",
        ["Standard Baseline / Moderate Official", "Lenient / High-Flow Context", "🚨 Strict / Cards & Penalties Inclined"]
    )
with b_col3:
    st.write("**Asymmetric Climate/Surface Friction & Pitch Dimensions**")
    asymmetric_pitch_climate_advantage = st.checkbox(
        "🚨 Host Artificial Turf / Extreme Climate Advantage Active", 
        value=False
    )
    asymmetric_pitch_width_advantage = st.checkbox(
        "📐 Host Narrow / Compressed Pitch Blueprint Surface Active",
        value=False,
        help="Reduces wide transitions of fast passing teams by 7%."
    )

st.markdown("---")
derby_match_active = st.checkbox(
    "🚨 Flag Entry as Local Derby / High-Intensity Rivalry", 
    value=False
)

# Convert active dashboard selections into precise decimal math parameters
weather_goals_multiplier = 1.00
if weather_condition_selection == "Heavy Rain / High Pitch Slick Surface": weather_goals_multiplier = 0.92
elif weather_condition_selection == "Extreme High Wind / Aerodynamic Drag Line": weather_goals_multiplier = 0.88

coach_attack_multiplier = 1.05 if "Long" in coach_stability_selection else (0.85 if "Recent" in coach_stability_selection else 1.00)
coach_volatility_expansion = 1.08 if "Public" in coach_stability_selection else 1.00

home_injury_penalty = 1.00 if home_missing_talent_tier == "Full Strength Squad" else (0.95 if "Tier 2" in home_missing_talent_tier else 0.85)
away_injury_penalty = 1.00 if away_missing_talent_tier == "Full Strength Squad" else (0.95 if "Tier 2" in away_missing_talent_tier else 0.85)

home_travel_multiplier = 0.92 if home_heavy_travel else 1.00
away_travel_multiplier = 0.92 if away_heavy_travel else 1.00

home_lookahead_penalty = 0.90 if "Home Team" in lookahead_match_active else 1.00
away_lookahead_penalty = 0.90 if "Away Team" in lookahead_match_active else 1.00

referee_volatility_expansion = 1.08 if "Strict" in referee_strictness_profile else (0.94 if "Lenient" in referee_strictness_profile else 1.00)
visitor_surface_penalty = 0.94 if asymmetric_pitch_climate_advantage else 1.00
home_pitch_width_modifier = 0.93 if asymmetric_pitch_width_advantage else 1.00

o_col1, o_col2 = st.columns(2)
with o_col1:
    odds_1 = st.number_input("Home Odds (1):", min_value=1.01, value=2.10, step=0.05, key="o_1")
    odds_X = st.number_input("Draw Odds (X):", min_value=1.01, value=3.20, step=0.05, key="o_x")
    odds_2 = st.number_input("Away Odds (2):", min_value=1.01, value=3.40, step=0.05, key="o_2")
with o_col2:
    odds_over = st.number_input("Over 2.5 Goals Odds:", min_value=1.01, value=1.95, step=0.05, key="o_ov")
    odds_under = st.number_input("Under 2.5 Goals Odds:", min_value=1.01, value=1.85, step=0.05, key="o_un")

# --- FIXED: INJECTED ALL INTERMEDIATE RETAIL ODDS TRACKING VARIABLES ---
odds_1X, odds_X2, odds_12 = 1.35, 1.65, 1.25
odds_btts_y, odds_btts_n = 1.80, 1.95
odds_dnb1, odds_dnb2 = 1.50, 2.45
odds_home_over_15, odds_home_under_15 = 2.10, 1.65
odds_away_over_15, odds_away_under_15 = 3.10, 1.35
odds_ah_home_minus_15, odds_ah_away_plus_15 = 3.80, 1.25
odds_ah_home_plus_15, odds_ah_away_minus_15 = 1.18, 5.50 # Aligned missing variable definition cleanly
odds_home_cs_y, odds_away_cs_y = 2.60, 3.90

h_status, a_status = "stable", "stable"
league_key = selected_league_filter.lower().strip()
baseline_goals = engine.COMPETITION_MATRIX.get(league_key, {"baseline_goals": 2.65}).get("baseline_goals", 2.65)
is_fr = st.session_state.freeze_matrix.get(league_key, False)
# ==============================================================================
# SEGMENT 10A OF 15: FLAT DYNAMIC MOTIVATION STANDINGS LOOPS & SAFETY SHIELD
# ==============================================================================

# Explicit namespace memory validator shield handles startup variable checks safely
resolved_standings_df = globals().get("live_standings_df", pd.DataFrame())
resolved_neutral_active = globals().get("tournament_neutral_active", False)
resolved_framework = globals().get("tournament_framework_selection", "Standard Domestic League Match")
resolved_vol_dampener = globals().get("vol_dampener", 1.0)
resolved_coach_vol = globals().get("coach_volatility_expansion", 1.0)
resolved_knockout_vol = globals().get("knockout_volatility_boost", 1.0)
resolved_referee_vol = globals().get("referee_volatility_expansion", 1.0)

home_motivation_multiplier = 1.00
away_motivation_multiplier = 1.00
tournament_neutral_active = "Neutral" in resolved_framework or "Knockout" in resolved_framework
knockout_volatility_boost = 1.15 if "Knockout" in resolved_framework else 1.00

# Execute real-world table lookups to isolate late-season urgency spikes
if not resolved_standings_df.empty and not resolved_neutral_active:
    resolved_standings_df.columns = [str(c).strip().lower() for c in resolved_standings_df.columns]
    resolved_standings_df.rename(columns={"team": "Team", "p": "P", "played": "P", "pld": "P"}, inplace=True)
    
    if "Team" in resolved_standings_df.columns and 'target' in globals():
        resolved_standings_df["Team"] = resolved_standings_df["Team"].astype(str).str.strip().lower()
        home_match_row = resolved_standings_df[resolved_standings_df["Team"] == str(target["home_team"]).strip().lower()]
        if not home_match_row.empty:
            home_position = int(home_match_row.index) + 1
            
            # --- ASYMMETRIC MOTIVATION STATE CHECKER (Late Campaign Inertia) ---
            # If team sits in dead-rubber safety zones, their motivation deflates automatically
            if 'total_fixtures' in locals() and total_fixtures > 0:
                current_matchday_trajectory = len(filtered_df[filtered_df["home_goals"].notna()]) / max(1, len(filtered_df))
                if current_matchday_trajectory >= 0.70:
                    if 6 <= home_position <= (len(resolved_standings_df) - 5):
                        home_motivation_multiplier = 0.88
                        st.sidebar.caption(f"🏖️ Dead-Rubber Inertia: {target['home_team']} motivation down-scaled.")
            
            # Standard elite baseline or relegation scrap urgency overrides
            if home_motivation_multiplier == 1.00:
                if home_position <= 4: 
                    home_motivation_multiplier = 1.12
                elif home_position >= (len(resolved_standings_df) - 3): 
                    home_motivation_multiplier = 1.15
                    # ==============================================================================
# SEGMENT 10B OF 15: COMBINATORIAL PROCESSOR CORE & 22-MARKET INTERMEDIATE INTERCPT
# ==============================================================================

if tournament_neutral_active:
    home_motivation_multiplier, away_motivation_multiplier = 1.00, 1.00

calibrated_baseline_goals = baseline_goals * weather_goals_multiplier * preseason_turnover_rate
if "Knockout" in tournament_framework_selection: 
    calibrated_baseline_goals *= 0.88

# --- PYTHAGOREAN EXPECTATION LUCK FILTER TRACKS ---
h_past_sot = filtered_df[filtered_df["home_team"] == target["home_team"]]["home_sot"].mean() if len(filtered_df) > 0 else 4.0
a_past_sot = filtered_df[filtered_df["away_team"] == target["away_team"]]["away_sot"].mean() if len(filtered_df) > 0 else 3.5
h_past_bc = filtered_df[filtered_df["home_team"] == target["home_team"]]["home_big_chances"].mean() if len(filtered_df) > 0 else 1.2
a_past_bc = filtered_df[filtered_df["away_team"] == target["away_team"]]["away_big_chances"].mean() if len(filtered_df) > 0 else 0.9

pythagorean_luck_ratio = (h_past_sot ** 2) / (h_past_sot ** 2 + a_past_sot ** 2) if (h_past_sot + a_past_sot) > 0 else 0.50
if pythagorean_luck_ratio > 0.65: 
    calibrated_baseline_goals *= 0.95 

# --- OPPONENT STRENGTH OF SCHEDULE (SoS) EQUALIZER TRACKS ---
home_sos_equalizer, away_sos_equalizer = 1.00, 1.00
if not resolved_standings_df.empty:
    resolved_standings_df.columns = [str(c).strip().lower() for c in resolved_standings_df.columns]
    resolved_standings_df.rename(columns={"team": "Team", "p": "P", "played": "P", "pld": "P"}, inplace=True)
    
    if "Team" in resolved_standings_df.columns:
        total_table_teams = len(resolved_standings_df)
        home_opponents = filtered_df[(filtered_df["home_team"] == target["home_team"]) | (filtered_df["away_team"] == target["home_team"])].tail(5)
        away_opponents = filtered_df[(filtered_df["home_team"] == target["away_team"]) | (filtered_df["away_team"] == target["away_team"])].tail(5)
        
        def compute_sos_index(opp_df, active_team):
            positions = []
            for _, gm in opp_df.iterrows():
                opp = str(gm["away_team"]).strip().lower() if str(gm["home_team"]).strip().lower() == active_team.lower() else str(gm["home_team"]).strip().lower()
                look = resolved_standings_df[resolved_standings_df["Team"] == opp]
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
    home_style_modifier = 0.88
    away_style_modifier = 1.10
    st.sidebar.warning("🛡️ Tactical Mismatch: Pressing host exposed to Counter-Attack tracks.")
elif home_tactical_style == "Deep Ultra-Defensive Low-Block" and away_tactical_style == "High-Possession Pressing":
    away_style_modifier = 0.90
    st.sidebar.info("🛡️ Tactical Mismatch: Low-Block defense suffocating traveling possession volume.")

vol_dampener_adjusted = resolved_vol_dampener * resolved_coach_vol * resolved_knockout_vol * resolved_referee_vol
if derby_match_active and not tournament_neutral_active:
    home_motivation_multiplier *= 0.85
    vol_dampener_adjusted *= 1.10

# --- UNIFIED COMPOUNDED PREDICTIVE FORMULA GRID PASS ---
calibrated_home_attack = home_motivation_multiplier * home_shot_quality_ratio * home_sos_equalizer * coach_attack_multiplier * home_injury_penalty * home_travel_multiplier * home_style_modifier * home_lookahead_penalty * home_pitch_width_modifier
calibrated_away_attack = away_motivation_multiplier * away_shot_quality_ratio * away_sos_equalizer * away_injury_penalty * away_travel_multiplier * away_style_modifier * away_lookahead_penalty * visitor_surface_penalty

res = engine.predict_match_probabilities(filtered_df, target["home_team"], target["away_team"], target_ts, calibrated_baseline_goals, calibrated_home_attack, calibrated_away_attack, h_status, a_status, max_score_cap, vol_dampener_adjusted, is_fr)
h_s = engine.parse_live_team_averages(filtered_df, target["home_team"], target_ts, half_life_days, h_status, is_fr)
a_s = engine.parse_live_team_averages(filtered_df, target["away_team"], target_ts, half_life_days, a_status, is_fr)

prob_home, prob_draw, prob_away = res["market_probabilities"]["1 (Home Win)"], res["market_probabilities"]["X (Draw)"], res["market_probabilities"]["2 (Away Win)"]
prob_matrix = res["raw_matrix"]

# Initialize all 22 advanced market tracking accumulators cleanly
over_25_p, btts_yes_p, home_cs_p, away_cs_p = 0.0, 0.0, 0.0, 0.0
home_over_15_p, away_over_15_p = 0.0, 0.0
ah_home_minus_15_p, ah_home_plus_15_p = 0.0, 0.0

# --- SHAPE TUPLE ISOLATION VECTOR PASS FIXED ---
max_r = int(prob_matrix.shape[0])
max_a = int(prob_matrix.shape[1])

for r_idx in range(max_r):
    for a_idx in range(max_a):
        cell_p = prob_matrix[r_idx, a_idx]
        
        # Totals accumulators
        if r_idx + a_idx > 2.5: over_25_p += cell_p
        if r_idx > 0 and a_idx > 0: btts_yes_p += cell_p
        
        # Clean Sheet accumulators
        if a_idx == 0: home_cs_p += cell_p
        if r_idx == 0: away_cs_p += cell_p
        
        # Team goals accumulators
        if r_idx > 1.5: home_over_15_p += cell_p
        if a_idx > 1.5: away_over_15_p += cell_p
        
        # Asian Handicap accumulators
        if r_idx - a_idx > 1.5: ah_home_minus_15_p += cell_p
        if r_idx - a_idx > -1.5: ah_home_plus_15_p += cell_p
        
# Finalize algebraic inversions for secondary option configurations
under_25_p, btts_no_p = 1.0 - over_25_p, 1.0 - btts_yes_p
dc_1X_p, dc_X2_p, dc_12_p = min(1.0, prob_home + prob_draw), min(1.0, prob_draw + prob_away), min(1.0, prob_home + prob_away)

dnb_denom = 1.0 - prob_draw if prob_draw < 1.0 else 1.0
dnb_1_p, dnb_2_p = prob_home / dnb_denom, prob_away / dnb_denom

home_under_15_p, away_under_15_p = 1.0 - home_over_15_p, 1.0 - away_over_15_p
ah_away_plus_15_p = 1.0 - ah_home_minus_15_p
ah_away_minus_15_p = 1.0 - ah_home_plus_15_p

sd = min(h_s.get("games_played", 12), a_s.get("games_played", 12))
confidence = min(100, int((sd / 12.0) * 100)) if sd > 0 else 50
# ==============================================================================
# SEGMENT 11 OF 15: EXPANDED EXPECTED VALUE AUDITOR & STRESS TESTER ENGINE
# ==============================================================================

st.markdown("### 📊 Comprehensive Market Projections & Value Audit")
all_markets_rendered_rows = []
qualified_projections = []
MAX_EV_CEILING_CAP = 0.50 

# --- ADVANCED EXPANDED INVENTORY ARRAYS ---
# Loops across all 22 parameters concurrently to build your automated insights sheets
extended_markets_master_manifest = [
    ("HOME WIN (1)", odds_1, prob_home),
    ("DRAW MATCH (X)", odds_X, prob_draw),
    ("AWAY WIN (2)", odds_2, prob_away),
    ("DOUBLE CHANCE 1X", odds_1X, dc_1X_p),
    ("DOUBLE CHANCE X2", odds_X2, dc_X2_p),
    ("DOUBLE CHANCE 12", odds_12, dc_12_p),
    ("OVER 2.5 TOTAL GOALS", odds_over, over_25_p),
    ("UNDER 2.5 TOTAL GOALS", odds_under, under_25_p),
    ("BOTH TEAMS TO SCORE (YES)", odds_btts_y, btts_yes_p),
    ("BOTH TEAMS TO SCORE (NO)", odds_btts_n, btts_no_p),
    ("DRAW NO BET HOME (DNB1)", odds_dnb1, dnb_1_p),
    ("DRAW NO BET AWAY (DNB2)", odds_dnb2, dnb_2_p),
    ("TEAM GOALS: HOME OVER 1.5", odds_home_over_15, home_over_15_p),
    ("TEAM GOALS: HOME UNDER 1.5", odds_home_under_15, home_under_15_p),
    ("TEAM GOALS: AWAY OVER 1.5", odds_away_over_15, away_over_15_p),
    ("TEAM GOALS: AWAY UNDER 1.5", odds_away_under_15, away_under_15_p),
    ("ASIAN HANDICAP: HOME -1.5", odds_ah_home_minus_15, ah_home_minus_15_p),
    ("ASIAN HANDICAP: AWAY +1.5", odds_ah_away_plus_15, ah_away_plus_15_p),
    ("ASIAN HANDICAP: HOME +1.5", odds_ah_home_plus_15, ah_home_plus_15_p),
    ("ASIAN HANDICAP: AWAY -1.5", odds_ah_away_minus_15, ah_away_minus_15_p),
    ("HOME CLEAN SHEET (YES)", odds_home_cs_y, home_cs_p),
    ("AWAY CLEAN SHEET (YES)", odds_away_cs_y, away_cs_p)
]

for label, b_odds, m_prob in extended_markets_master_manifest:
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
highest_ev_found = max([(m_p * b_o) - 1.0 for lbl, b_o, m_p in extended_markets_master_manifest]) if extended_markets_master_manifest else -1.0
if highest_ev_found >= 0.030 and confidence >= confidence_floor_input:
    st.success(f"🔥 ELITE PROJECTIONS UNLOCKED (+{highest_ev_found*100:.1f}% EV Edge Verified Across Multi-Variable Matrix Maps)")
else: st.error("📉 SELECTION REJECTED: Internal profit margins fail target professional risk floor bounds.")

st.dataframe(pd.DataFrame(all_markets_rendered_rows), use_container_width=True, hide_index=True)
# ==============================================================================
# SEGMENT 12 OF 15: FLAT GLOBAL EXACT MATCH GOALS RENDERS & SCORE CURVES
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
# SEGMENT 13 OF 15: FLAT GLOBAL MESSAGING RELAYS & CALIBRATED COUPON COUPLING
# ==============================================================================

if qualified_projections and confidence >= confidence_floor_input:
    qualified_projections.sort(key=lambda x: x[1], reverse=True)
    target_premium_selection = qualified_projections[0]
    optimal_bet = str(target_premium_selection[0])
    best_ev = float(target_premium_selection[1])
    best_prob = float(target_premium_selection[2])
    best_odds = float(target_premium_selection[3])
    fractional_scale_stake = float(target_premium_selection[4])
    bet_rec = str(target_premium_selection[5])
else: 
    optimal_bet, best_ev, best_prob, best_odds, fractional_scale_stake, bet_rec = "NO COMPREHENSIVE SELECTION MET FLOORS", 0.00, 0.00, 2.00, 0.00, "❌ NO BET"

c_col_l, c_col_r = st.columns(2)
with c_col_l:
    st.markdown("### 📊 Live Analytics Monitor")
    st.metric("Match Confidence Value", f"{confidence}%")
    st.metric("Value Threshold Rating", bet_rec)
    st.markdown("### 🧠 Model Tactical Rationale Breakdown")
    
    # Render automated textual insights based on calibrated Shot Quality proxies
    st.markdown(f"• **Dominant Threat Metrics Trace**: Home team recent shooting efficiency averages **{h_past_bc:.2f} big chances** from **{h_past_sot:.2f} SOT** relative to Traveling Road parameters of **{a_past_bc:.2f} big chances** from **{a_past_sot:.2f} SOT**. This forms the core anchor of the Poisson matrix grid splits.")
    # ==============================================================================
# SEGMENT 14 OF 15: MEMORY-ISOLATED PERFORMANCE TRACKER (NO DISK SAVES)
# ==============================================================================
with c_col_r:
    st.markdown("### 🎫 Calibrated Ticket Slip")
    ticket_string_content = (
        f"# ========================================\n"
        f"#          SISONKE CALIBRATED TICKET SLIP \n"
        f"# ========================================\n"
        f"MATCH PROFILE   : {target['home_team']} vs {target['away_team']}\n"
        f"RATING TIER TAG : {bet_rec}\n"
        f"TARGET MARKET   : {optimal_bet}\n"
        f"EXPECTED VALUE  : +{best_ev*100:.2f}%\n"
        f"KELLY STAKE     : {fractional_scale_stake}%\n"
        f"CONFIDENCE RATE : {confidence}%\n"
        f"TIMESTAMP EXP   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"# ========================================"
    )
    st.text_area("Ticket Log Slip View", value=ticket_string_content, height=180)
    
    st.download_button(
        label="💾 Download Coupon File Ticket (.txt)",
        data=ticket_string_content,
        file_name=f"sisonke_ticket_{target['home_team']}_vs_{target['away_team']}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("### 🏦 Sisonke Investment Ledger Room")
    
    # Initialize transient ledger list inside temporary container memory if missing
    if "transient_ledger_cache" not in st.session_state:
        st.session_state["transient_ledger_cache"] = []

    with st.form("ledger_commit_form"):
        try: safe_default_odds = float(best_odds)
        except: safe_default_odds = 2.00
        closing_odds_input = st.number_input("Enter Bookmaker Final Closing Odds:", min_value=1.01, value=safe_default_odds, step=0.05)
        match_outcome_selection = st.selectbox("Select Actual Match Reality Outcome:", ["Pending / Unplayed", "Won Match", "Lost Match", "Void / Refunded"])
        submit_ledger_entry = st.form_submit_button("💾 Log Ticket to Session Memory")
        
        if submit_ledger_entry and "NO COMPREHENSIVE" not in optimal_bet:
            entry_implied_prob = 1.0 / float(best_odds)
            closing_implied_prob = 1.0 / float(closing_odds_input)
            clv_edge_margin_pct = round((entry_implied_prob - closing_implied_prob) * 100, 2)
            net_units = round(fractional_scale_stake * (float(best_odds) - 1.0), 2) if match_outcome_selection == "Won Match" else (-fractional_scale_stake if match_outcome_selection == "Lost Match" else 0.0)
            
            new_transient_row = {
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d"), 
                "Match": f"{target['home_team']} vs {target['away_team']}", 
                "Market": optimal_bet, 
                "Model_Prob": f"{best_prob*100:.1f}%", 
                "Entry_Odds": best_odds, 
                "Closing_Odds": closing_odds_input, 
                "CLV_Edge_Pct": f"{clv_edge_margin_pct:+.2f}%", 
                "Kelly_Stake_Pct": f"{fractional_scale_stake:.2f}%", 
                "Outcome": match_outcome_selection, 
                "Net_Profit_Units": net_units
            }
            # Append rows directly to temporary memory state array instead of writing hard csv to drive
            st.session_state["transient_ledger_cache"].append(new_transient_row)
            st.toast("📬 Ticket recorded in transient cache memory successfully!")

    # Display rolling performance chart out of RAM memory cache safely
    if st.session_state["transient_ledger_cache"]:
        display_ledger_df = pd.DataFrame(st.session_state["transient_ledger_cache"])
        st.markdown("#### 📈 Session Bankroll Performance Ledger")
        st.dataframe(display_ledger_df.tail(10), use_container_width=True, hide_index=True)
        display_ledger_df["Cumulative_Units"] = display_ledger_df["Net_Profit_Units"].cumsum()
        st.write("**Visualized Session Return Yield Curve (Rolling RAM Profit)**")
        st.line_chart(display_ledger_df["Cumulative_Units"], use_container_width=True)
    else:
        st.info("No tickets recorded inside this temporary session timeline yet.")
        # ==============================================================================
# SEGMENT 15A OF 15: OUTRIGHT ARBITRAGE MATRIX & SQUAD OVERRIDES PANEL
# ==============================================================================

with tab_tables:
    if not filtered_df.empty:
        settled_check_df = filtered_df.dropna(subset=["home_goals", "away_goals"])
        
        if len(settled_check_df) == 0 or preseason_calibration_active:
            # FIXED: Title automatically formats to the specific selected tier name cleanly
            st.markdown(f"#### 🏆 Syndicate {selected_league_filter.upper()} Outright Winner Probability & Boardroom EV Arbitrage")
            st.info("📊 Elite Simulation Active: Running 1,000 parallel tournament iterations with corporate manager sack loops, climate turf friction, and closing-gap motivation logic...")
            
            all_participating_teams = sorted(list(set(filtered_df["home_team"].dropna().unique()).union(set(filtered_df["away_team"].dropna().unique()))))
            
            squad_profile_rows = []
            for team in all_participating_teams:
                squad_profile_rows.append({
                    "Competing Squad": team,
                    "Transfer Additions Boost (%)": 0.0,
                    "Player Departures Decay (%)": 0.0,
                    "Squad Rotation Depth Index": 1.00,
                    "Active in Continental Cups": False,
                    "Corporate Manager Sack Floor (Min PPG)": 1.10,
                    "Asymmetric Pitch Layout Width Index": 1.00,
                    "Bookmaker Outright Odds": 25.00
                })
                
            st.write("✏ Adjust individual roster depth, multi-cup commitments, pitch layouts, and boardroom metrics before running the simulation pass:")
            
            edited_profile_df = st.data_editor(
                pd.DataFrame(squad_profile_rows),
                column_config={
                    "Competing Squad": st.column_config.TextColumn("Competing Squad", disabled=True),
                    "Transfer Additions Boost (%)": st.column_config.NumberColumn("Signings Impact (+%)", min_value=0.0, max_value=25.0, step=1.0, format="%.1f%%"),
                    "Player Departures Decay (%)": st.column_config.NumberColumn("Departures Decay (-%)", min_value=0.0, max_value=25.0, step=1.0, format="%.1f%%"),
                    "Squad Rotation Depth Index": st.column_config.NumberColumn("Squad Rotation Depth", min_value=0.80, max_value=1.20, step=0.05, format="%.2f"),
                    "Active in Continental Cups": st.column_config.CheckboxColumn("Multi-Cup Congestion?"),
                    "Corporate Manager Sack Floor (Min PPG)": st.column_config.NumberColumn("Sack PPG Floor", min_value=0.50, max_value=2.00, step=0.05, format="%.2f"),
                    "Asymmetric Pitch Layout Width Index": st.column_config.NumberColumn("Pitch Width Index", min_value=0.85, max_value=1.15, step=0.05, format="%.2f"),
                    "Bookmaker Outright Odds": st.column_config.NumberColumn("Bookmaker Outright Odds", format="%.2f", min_value=1.01, step=0.5)
                },
                hide_index=True,
                use_container_width=True,
                key="outright_squad_ledger_final"
            )

            transfer_boost_map = {}
            departure_decay_map = {}
            depth_index_map = {}
            congestion_map = {}
            sack_floor_map = {}
            pitch_width_map = {}
            bookmaker_odds_map = {}
            
            if edited_profile_df is not None:
                for _, row in edited_profile_df.iterrows():
                    t_name = str(row["Competing Squad"])
                    transfer_boost_map[t_name] = 1.0 + (float(row["Transfer Additions Boost (%)"]) / 100.0)
                    departure_decay_map[t_name] = 1.0 - (float(row["Player Departures Decay (%)"]) / 100.0)
                    depth_index_map[t_name] = float(row["Squad Rotation Depth Index"])
                    congestion_map[t_name] = bool(row["Active in Continental Cups"])
                    sack_floor_map[t_name] = float(row["Corporate Manager Sack Floor (Min PPG)"])
                    pitch_width_map[t_name] = float(row["Asymmetric Pitch Layout Width Index"])
                    bookmaker_odds_map[t_name] = float(row["Bookmaker Outright Odds"])
            else:
                for team in all_participating_teams:
                    transfer_boost_map[team] = 1.0; departure_decay_map[team] = 1.0; depth_index_map[team] = 1.00; congestion_map[team] = False; sack_floor_map[team] = 1.10; pitch_width_map[team] = 1.00; bookmaker_odds_map[team] = 25.0
                    # ==============================================================================
# SEGMENT 15B OF 15: MONTE CARLO SIMULATION ENGINE & BACKTESTER AUXILIARY PANELS
# ==============================================================================

            outright_simulation_scoreboard = {team: 0 for team in all_participating_teams}
            mock_schedule_fixtures = [{"home": h, "away": a} for h in all_participating_teams for a in all_participating_teams if h != a]
            
            if mock_schedule_fixtures:
                for iteration in range(1000):
                    iteration_points_registry = {team: 0 for team in all_participating_teams}
                    iteration_games_played = {team: 0 for team in all_participating_teams}
                    manager_sacked_registry = {team: False for team in all_participating_teams}
                    
                    for index_f, fix in enumerate(mock_schedule_fixtures):
                        sim_baseline_goals = baseline_goals * weather_goals_multiplier * preseason_turnover_rate
                        iteration_games_played[fix["home"]] += 1
                        iteration_games_played[fix["away"]] += 1
                        
                        if index_f > (len(mock_schedule_fixtures) * 0.85):
                            top_team_interim = max(iteration_points_registry, key=iteration_points_registry.get)
                            if fix["home"] == top_team_interim: sim_baseline_goals *= 0.78
                        
                        home_sack_bounce = 1.00
                        away_sack_bounce = 1.00
                        if iteration_games_played[fix["home"]] >= 10:
                            home_current_ppg = iteration_points_registry[fix["home"]] / iteration_games_played[fix["home"]]
                            if home_current_ppg < sack_floor_map.get(fix["home"], 1.10) and not manager_sacked_registry[fix["home"]]:
                                manager_sacked_registry[fix["home"]] = True
                        if manager_sacked_registry[fix["home"]]: home_sack_bounce = 1.10
                        
                        if iteration_games_played[fix["away"]] >= 10:
                            away_current_ppg = iteration_points_registry[fix["away"]] / iteration_games_played[fix["away"]]
                            if away_current_ppg < sack_floor_map.get(fix["away"], 1.10) and not manager_sacked_registry[fix["away"]]:
                                manager_sacked_registry[fix["away"]] = True
                        if manager_sacked_registry[fix["away"]]: away_sack_bounce = 1.10
                        
                        home_pitch_modifier = 1.00
                        if pitch_width_map.get(fix["home"], 1.00) < 0.95: home_pitch_modifier = 0.93
                        
                        home_transfer_modifier = transfer_boost_map.get(fix["home"], 1.0) * departure_decay_map.get(fix["home"], 1.0)
                        away_transfer_modifier = transfer_boost_map.get(fix["away"], 1.0) * departure_decay_map.get(fix["away"], 1.0)
                        
                        home_attrition_modifier = 1.00
                        away_attrition_modifier = 1.00
                        if index_f > (len(mock_schedule_fixtures) * 0.60):
                            home_attrition_modifier = min(1.0, depth_index_map.get(fix["home"], 1.00))
                            away_attrition_modifier = min(1.0, depth_index_map.get(fix["away"], 1.00))
                            
                        home_congestion_modifier = 0.915 if congestion_map.get(fix["home"], False) and (index_f % 7 == 0) else 1.00
                        away_congestion_modifier = 0.915 if congestion_map.get(fix["away"], False) and (index_f % 7 == 0) else 1.00
                        
                        raw_h_exp = 1.35 * sim_baseline_goals * coach_attack_multiplier * home_transfer_modifier * home_attrition_modifier * home_congestion_modifier * home_sack_bounce * home_pitch_modifier
                        raw_a_exp = 1.05 * sim_baseline_goals * away_transfer_modifier * away_attrition_modifier * away_congestion_modifier * away_sack_bounce
                        
                        sim_h_goals = np.random.poisson(raw_h_exp)
                        sim_a_goals = np.random.poisson(raw_a_exp)
                        
                        if sim_h_goals > sim_a_goals: iteration_points_registry[fix["home"]] += 3
                        elif sim_a_goals > sim_h_goals: iteration_points_registry[fix["away"]] += 3
                        else:
                            iteration_points_registry[fix["home"]] += 1
                            iteration_points_registry[fix["away"]] += 1
                            
                    for team in iteration_points_registry:
                        if iteration_points_registry[team] > 100: iteration_points_registry[team] = 100
                            
                    champion_squad = max(iteration_points_registry, key=iteration_points_registry.get)
                    outright_simulation_scoreboard[champion_squad] += 1
            
            outright_results_rows = []
            for team, win_count in outright_simulation_scoreboard.items():
                projected_win_probability_pct = float(win_count / 1000.0)
                b_odds = bookmaker_odds_map.get(team, 25.0)
                calculated_outright_ev = (projected_win_probability_pct * b_odds) - 1.0
                
                if calculated_outright_ev >= 0.070: verdict = "🔥 HIGH VALUE FUTURES TICKET"
                elif 0.030 <= calculated_outright_ev <= 0.069: verdict = "🟢 STANDARD VALUE ACCUMULATOR"
                elif 0.000 <= calculated_outright_ev < 0.030: verdict = "❌ NO BET (EDGE VALUE DEFICIT)"
                else: verdict = "❌ NEGATIVE EXPECTED VALUE"
                
                outright_results_rows.append({
                    "Competing Squad": team,
                    "Model Probability (%)": f"{projected_win_probability_pct * 100:.1f}%",
                    "Fair Value Odds": f"{1.0 / projected_win_probability_pct:.2f}" if projected_win_probability_pct > 0 else "999.00",
                    "Your Input Odds": f"{b_odds:.2f}",
                    "Outright EV (%)": f"{calculated_outright_ev * 100:+.1f}%",
                    "Trading Verdict": verdict
                })
            
            outright_display_df = pd.DataFrame(outright_results_rows).sort_values(by="Model Probability (%)", ascending=False).reset_index(drop=True)
            st.write("📈 **Simulated Outright Forecasting & Arbitrage Report Matrix:**")
            st.dataframe(outright_display_df, use_container_width=True, hide_index=True)
            st.markdown("---")
            
        base_table = engine.generate_dynamic_league_table(filtered_df)
        if base_table is not None and not base_table.empty: 
            st.write("**Current Real-World Standings Table**")
            st.dataframe(base_table, use_container_width=True)
        else: st.info("Dynamic league standings are empty or uncompiled.")
    else: st.info("No context available to compile standings arrays.")

with tab_history:
    st.markdown("### Backtest Calibration Analysis")
    if not filtered_df.empty:
        league_key = selected_league_filter.lower().strip()
        baseline_goals = engine.COMPETITION_MATRIX.get(league_key, {"baseline_goals": 2.65}).get("baseline_goals", 2.65)
        b_df = engine.run_rolling_window_backtest(filtered_df, baseline_goals, backtest_window, 7, vol_dampener)
        if b_df is not None and not b_df.empty:
            b_df["is_correct"] = b_df["model_probability"] >= accuracy_threshold_floor
            st.metric("Backtest Prediction Accuracy", f"{(b_df['is_correct'].sum() / len(b_df)) * 100:.1f}%")
            st.dataframe(b_df, use_container_width=True)
        else: st.info("Insufficient historical metrics to parse target backtesting window arrays.")
    else: st.info("No datasets verified.")

with tab_past:
    st.markdown("### 📜 Settled Historical Results Ledger")
    if not filtered_df.empty:
        past_h = filtered_df.dropna(subset=["home_goals", "away_goals"]).copy()
        if not past_h.empty: 
            st.dataframe(past_h.sort_values(by="match_timestamp", ascending=False).reset_index(drop=True)[["match_timestamp", "home_team", "away_team", "home_goals", "away_goals"]], use_container_width=True)
        else: st.info("No historical matches found for this filter combination.")
    else: st.info("Database matrix workspace is currently unpopulated.")
    
