# ==============================================================================
# SEGMENT 1 OF 12: GLOBAL NAMESPACE INITIALIZATION & CORE IMPORTS
# ==============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import http.client
import json
import main_engine as engine

# Force institutional widescreen structural responsive layout framework rules
st.set_page_config(page_title="Sisonke Sports Analytics Core Hub", layout="wide", initial_sidebar_state="expanded")

# Initialize global storage dictionary keys inside streamlit session cache state
if "freeze_matrix" not in st.session_state:
    st.session_state.freeze_matrix = {}
if "processed_cache_success" not in st.session_state:
    st.session_state["processed_cache_success"] = False
if "full_validation_df" not in st.session_state:
    st.session_state["full_validation_df"] = pd.DataFrame()

# Establish localized folder structural boundaries on the host partition
storage_path = "master_sisonke_database.csv"
is_valid_data = False
api_sync_triggered = False
# ==============================================================================
# SEGMENT 2 OF 12: DORMANT API INTEGRATION HEADERS & SECURITY MAPS
# ==============================================================================
# Token placeholders map directly to corporate data stream servers when required
API_FOOTBALL_HOST_ENDPOINT = "v3.football.api-sports.io"
API_SECURE_TOKEN_CREDENTIALS = "YOUR_API_FOOTBALL_SECRET_TOKEN_HERE"

LEAGUE_API_IDENTIFIER_REGISTRY = {
    "england premier league": 39, "england championship": 40,
    "spain la liga": 140, "germany bundesliga": 78,
    "italy serie a": 135, "france ligue 1": 61,
    "south africa premier league": 288, "austria premier league": 218,
    "estonia premier league": 322, "uefa champions league": 2,
    "africa cup of nations": 6, "fifa world cup": 1
    }
    # ==============================================================================
# SEGMENT 3 OF 12: CORPORATE STRUCTURAL BRANDING LAYER & SIDEBAR LAYOUT
# ==============================================================================
st.title("🦅 Sisonke Football Predictive Analytics Hub")
st.markdown("##### *We Beat The Odds*")
st.sidebar.image("https://unsplash.com", use_container_width=True)
st.sidebar.markdown("### 🎛️ Active Data Control Room")
st.sidebar.caption("Sisonke Engine Status: 🟢 High-Utility Operations Standby")
    # ==============================================================================
# SEGMENT 4 OF 12: MULTI-LEAGUES MANUAL CSV INGESTION PORT
# ==============================================================================
st.sidebar.markdown("#### 📁 Historical Matchday Upload Port")
uploaded_file = st.sidebar.file_uploader(
    "Drop your imidlalo.csv or fixture ledger files here:", 
    type=["csv"], 
    help="Accepts mixed format data structures natively."
)
# ==============================================================================
# SEGMENT 5 OF 12: UNIVERSAL SCHEMA TRANSLATION ENGINE & NOMENCLATURE SHIELD
# ==============================================================================
if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        manual_upload_df = pd.read_csv(uploaded_file, engine='python', on_bad_lines='skip')
        
        ALIGNED_HEADER_TRANSLATION_MAP = {
            "div": "league_country", "league_name": "league_country", "competition": "league_country",
            "date": "match_timestamp", "timestamp": "match_timestamp",
            "home": "home_team", "hometeam": "home_team", "away": "away_team", "awayteam": "away_team",
            "fthg": "home_goals", "hg": "home_goals", "ftag": "away_goals", "ag": "away_goals",
            "hs": "home_sot", "as": "away_sot", "home shots": "home_sot", "away shots": "away_sot",
            "hbc": "home_big_chances", "abc": "away_big_chances", "home big chances": "home_big_chances", "away big chances": "away_big_chances",
            "home_red_cards": "home_red_cards", "away_red_cards": "away_red_cards", "hrc": "home_red_cards", "arc": "away_red_cards"
        }
        manual_upload_df.columns = [str(c).strip().lower() for c in manual_upload_df.columns]
        manual_upload_df.rename(columns=ALIGNED_HEADER_TRANSLATION_MAP, inplace=True)
        
        if "league_country" in manual_upload_df.columns:
            def segment_divisional_tiers(cell_val):
                val_clean = str(cell_val).strip().upper()
                if "SPAIN" in val_clean: return "SPAIN LA LIGA"
                elif "GERMANY" in val_clean: return "GERMANY BUNDESLIGA"
                elif "ITALY" in val_clean: return "ITALY SERIE A"
                elif "PREMIER" in val_clean or "EPL" in val_clean or "TIER 1" in val_clean:
                    return "ENGLAND PREMIER LEAGUE" if "ENGLAND" in val_clean else f"{cell_val} PREMIER LEAGUE"
                elif "CHAMPIONSHIP" in val_clean or "CHAM" in val_clean or "TIER 2" in val_clean:
                    return "ENGLAND CHAMPIONSHIP" if "ENGLAND" in val_clean else f"{cell_val} CHAMPIONSHIP"
                if val_clean == "ENGLAND": return "ENGLAND PREMIER LEAGUE"
                return cell_val
            manual_upload_df["league_country"] = manual_upload_df["league_country"].apply(segment_divisional_tiers)

        if "home_red_cards" in manual_upload_df.columns and "away_red_cards" in manual_upload_df.columns:
            red_card_mask = (manual_upload_df["home_red_cards"] > 0) | (manual_upload_df["away_red_cards"] > 0)
            if red_card_mask.any():
                manual_upload_df.loc[red_card_mask, "home_goals"] = manual_upload_df.loc[red_card_mask, "home_goals"].clip(upper=3)
                manual_upload_df.loc[red_card_mask, "away_goals"] = manual_upload_df.loc[red_card_mask, "away_goals"].clip(upper=3)

        if "match_timestamp" not in manual_upload_df.columns: 
            manual_upload_df["match_timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            manual_upload_df["match_timestamp"] = manual_upload_df["match_timestamp"].astype(str)

        COMPREHENSIVE_METRIC_FALLBACKS = {
            "home_goals": np.nan, "away_goals": np.nan, "home_sot": 4.0, "away_sot": 3.5,
            "home_big_chances": 1.2, "away_big_chances": 0.9, "home_box_touches": 16.0, "away_box_touches": 13.0,
            "home_through_passes": 1.5, "away_through_passes": 1.1, "home_final_third_entries": 32.0, "away_final_third_entries": 28.0,
            "home_interceptions": 11.0, "away_interceptions": 12.0, "home_recoveries": 48.0, "away_recoveries": 46.0,
            "home_saves": 2.5, "away_saves": 2.8, "home_ground_duels_won_pct": 0.50, "away_ground_duels_won_pct": 0.50,
            "home_aerial_duels_won_pct": 0.50, "away_aerial_duels_won_pct": 0.50, "home_dribbles_won_pct": 0.50, "away_dribbles_won_pct": 0.50,
            "home_tackles_won_pct": 0.52, "away_tackles_won_pct": 0.52, "home_passes_final_third_pct": 0.68, "away_passes_final_third_pct": 0.65,
            "home_rest_days": 5.0, "away_rest_days": 5.0
        }
        
        for mandatory_col, fallback_val in COMPREHENSIVE_METRIC_FALLBACKS.items():
            if mandatory_col not in manual_upload_df.columns: manual_upload_df[mandatory_col] = fallback_val
            else: manual_upload_df[mandatory_col] = manual_upload_df[mandatory_col].fillna(fallback_val)
        
        st.session_state["full_validation_df"] = manual_upload_df.copy()
        full_validation_df = st.session_state["full_validation_df"]
        is_valid_data = True
    except Exception as e: st.error(f"Manual Ingestion Shield Error: {e}")
# ==============================================================================
# SEGMENT 6 OF 12: MEMORY-ISOLATED INGESTION LAYER & LOCAL DISK AUTO-MIRROR
# ==============================================================================
processed_execution_rows = []
historical_reference_df = pd.DataFrame()

if os.path.exists(storage_path):
    try:
        historical_reference_df = pd.read_csv(storage_path, on_bad_lines='skip')
        historical_reference_df.columns = [str(c).strip().lower() for c in historical_reference_df.columns]
        historical_reference_df["match_timestamp"] = pd.to_datetime(historical_reference_df["match_timestamp"].astype(str), errors='coerce', dayfirst=True)
        if st.session_state["full_validation_df"].empty:
            st.session_state["full_validation_df"] = historical_reference_df.copy()
            full_validation_df = st.session_state["full_validation_df"]
    except: pass

if globals().get("is_valid_data", False) and not full_validation_df.empty and not api_sync_triggered and not st.session_state["processed_cache_success"]:
    st.sidebar.caption("🟢 Mode Status: Compiling Isolated RAM Fatigue Matrix...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    total_upload_records = len(full_validation_df)
    full_validation_df["match_timestamp"] = pd.to_datetime(full_validation_df["match_timestamp"].astype(str), errors='coerce', dayfirst=True)
    
    for index, row in full_validation_df.iterrows():
        h_name = str(row["home_team"]).strip()
        a_name = str(row["away_team"]).strip()
        current_match_time = row["match_timestamp"]
        if pd.isnull(current_match_time) or isinstance(current_match_time, str): current_match_time = pd.Timestamp.now()
            
        status_text.text(f"Processing File Rows {index+1}/{total_upload_records}: {h_name} vs {a_name}")
        calculated_home_rest_days, calculated_away_rest_days = 5.0, 5.0
        
        if not historical_reference_df.empty:
            home_candidates = historical_reference_df[(historical_reference_df["home_team"] == h_name) | (historical_reference_df["away_team"] == h_name)]
            home_past_dates = []
            for _, c_row in home_candidates.iterrows():
                ts_val = c_row["match_timestamp"]
                if pd.notna(ts_val) and isinstance(ts_val, (pd.Timestamp, datetime.datetime, datetime.date)) and ts_val < current_match_time:
                    home_past_dates.append(ts_val)
            if home_past_dates:
                days_diff = (current_match_time - max(home_past_dates)).days
                calculated_home_rest_days = float(days_diff) if days_diff <= 14 else 5.0
                
            away_candidates = historical_reference_df[(historical_reference_df["home_team"] == a_name) | (historical_reference_df["away_team"] == a_name)]
            away_past_dates = []
            for _, c_row in away_candidates.iterrows():
                ts_val = c_row["match_timestamp"]
                if pd.notna(ts_val) and isinstance(ts_val, (pd.Timestamp, datetime.datetime, datetime.date)) and ts_val < current_match_time:
                    away_past_dates.append(ts_val)
            if away_past_dates:
                days_diff = (current_match_time - max(away_past_dates)).days
                calculated_away_rest_days = float(days_diff) if days_diff <= 14 else 5.0

        def parse_safe_float(val, fallback):
            if pd.isna(val): return fallback
            val_str = str(val).strip().replace(" ", "")
            try: return float(val_str) if val_str != "" else fallback
            except: return fallback

        processed_execution_rows.append({
            "league_country": row.get("league_country", "Imported League"), "match_timestamp": current_match_time.isoformat(),
            "home_team": h_name, "away_team": a_name, "home_goals": row.get("home_goals"), "away_goals": row.get("away_goals"),
            "home_sot": parse_safe_float(row.get("home_sot"), 4.0), "away_sot": parse_safe_float(row.get("away_sot"), 3.5),
            "home_big_chances": parse_safe_float(row.get("home_big_chances"), 1.2), "away_big_chances": parse_safe_float(row.get("away_big_chances"), 0.9),
            "home_box_touches": parse_safe_float(row.get("home_box_touches"), 16.0), "away_box_touches": parse_safe_float(row.get("away_box_touches"), 13.0),
            "home_rest_days": calculated_home_rest_days, "away_rest_days": calculated_away_rest_days
        })
        progress_bar.progress((index + 1) / total_upload_records)
        
    status_text.empty()
    progress_bar.empty()

    if processed_execution_rows:
        new_memory_df = pd.DataFrame(processed_execution_rows)
        st.session_state["full_validation_df"] = new_memory_df.copy()
        if not historical_reference_df.empty:
            try:
                combined_replicated_df = pd.concat([historical_reference_df, new_memory_df], ignore_index=True)
                combined_replicated_df.drop_duplicates(subset=["league_country", "match_timestamp", "home_team", "away_team"], keep="last", inplace=True)
                combined_replicated_df.to_csv(storage_path, index=False)
            except: pass
        else: new_memory_df.to_csv(storage_path, index=False)
        st.session_state["processed_cache_success"] = True
        st.rerun()

if uploaded_file is None and st.session_state["processed_cache_success"]:
    st.session_state["processed_cache_success"] = False
full_validation_df = st.session_state["full_validation_df"]
# ==============================================================================
# SEGMENT 7 OF 12: AUTOMATED TIME-DECAY AUTO-TUNER & DROPDOWN LOCK VAULT
# ==============================================================================
working_pipeline_df = full_validation_df.copy() if not full_validation_df.empty else (pd.read_csv(storage_path) if os.path.exists(storage_path) else pd.DataFrame())

if not working_pipeline_df.empty:
    working_pipeline_df.columns = [str(c).strip().lower() for c in working_pipeline_df.columns]
    working_pipeline_df["match_timestamp"] = pd.to_datetime(working_pipeline_df["match_timestamp"].astype(str).str.replace("T", " "), errors='coerce').fillna(pd.Timestamp.now())
    working_pipeline_df.drop_duplicates(subset=["league_country", "match_timestamp", "home_team", "away_team"], keep="last", inplace=True)
    uploaded_leagues = sorted(list(working_pipeline_df["league_country"].dropna().unique()))
else:
    st.info("📂 Data Control Room Active: Please upload your recent match history CSV file to begin training.")
    st.stop()

selected_league_filter = st.selectbox("Select Target League Workspace Selection:", uploaded_leagues)
filtered_df = working_pipeline_df[working_pipeline_df["league_country"].str.lower().str.strip() == selected_league_filter.lower().strip()].reset_index(drop=True)
settled_past_games = filtered_df.dropna(subset=["home_goals", "away_goals"])

optimal_half_life = 45
if len(settled_past_games) >= 5:
    lowest_historical_brier = 999.0
    for test_hl in range(15, 91, 15):
        test_brier_accumulator, tc = 0.0, 0
        for idx, r in settled_past_games.tail(15).iterrows():
            act_outcome = 1.0 if r["home_goals"] > r["away_goals"] else 0.0
            h_sot_avg = filtered_df[(filtered_df["home_team"] == r["home_team"]) & (filtered_df["match_timestamp"] < r["match_timestamp"])]["home_sot"].mean()
            a_sot_avg = filtered_df[(filtered_df["away_team"] == r["away_team"]) & (filtered_df["match_timestamp"] < r["match_timestamp"])]["away_sot"].mean()
            h_sot_val = h_sot_avg if pd.notna(h_sot_avg) else 4.0
            a_sot_val = a_sot_avg if pd.notna(a_sot_avg) else 3.5
            p_win_proxy = h_sot_val / max(1.0, h_sot_val + a_sot_val)
            test_brier_accumulator += (p_win_proxy - act_outcome) ** 2
            tc += 1
        if tc > 0 and (test_brier_accumulator / tc) < lowest_historical_brier:
            lowest_historical_brier = test_brier_accumulator / tc
            optimal_half_life = test_hl

with st.expander("🛠️ Advanced Calibration & Mathematical Tuning Vault", expanded=False):
    st.markdown("🔒 *Sliders are locked inside this container dropdown to safeguard mobile interface screen taps.*")
    activate_manual_decay_override = st.checkbox("Uncouple Stage 1 Auto-Tuner (Manual Decay Override)", value=False)
    if activate_manual_decay_override: half_life_days = st.slider("Time-Decay Half Life (Days)", 15, 90, int(optimal_half_life), 1)
    else:
        half_life_days = int(optimal_half_life)
        st.success(f"🎯 Auto-Tuner Active: {selected_league_filter} Half-Life locked at {half_life_days} Days.")
    max_score_cap = st.slider("Max Score Ceiling", 4, 10, 6, 1)
    vol_dampener = st.slider("Volatility Dampener", 0.5, 1.5, 1.0, 0.05)
    backtest_window = st.slider("Backtest Window Size (Days)", 90, 365, 180, 5)
    confidence_floor_input = st.slider("Strict Confidence Floor Trigger (%)", 15, 85, 50, 5)
    accuracy_threshold_floor = st.slider("Strict Accuracy Floor (%)", 35, 75, 50, 5) / 100.0

for idx, league in enumerate(uploaded_leagues):
    st.session_state.freeze_matrix[league.lower().strip()] = st.checkbox(f"Freeze Decay: {league.upper()}", value=st.session_state.freeze_matrix.get(league.lower().strip(), False), key=f"f_{idx}")
    # ==============================================================================
# SEGMENT 8 & 9 OF 12: DROPDOWN OVERRIDES & LEFT COLS WORKING ENVIRONMENT
# ==============================================================================
tab_pred, tab_tables, tab_history, tab_past = st.tabs(["📅 PROJECTIONS", "🌍 STANDINGS", "📜 BACKTESTER", "📜 PAST GAMES"])

with tab_pred:
    if not filtered_df.empty:
        options = {f"[{r['league_country'].upper()}] {r['home_team']} vs {r['away_team']} ({pd.to_datetime(r['match_timestamp']).strftime('%Y-%m-%d')})": r for idx, r in filtered_df.iterrows()}
        if options:
            sel_match = st.selectbox("Select Active Fixture Profile Layout Selection:", list(options.keys()))
            target = options[sel_match]
            target_ts = pd.to_datetime(target["match_timestamp"])
            
            past_home = filtered_df[(filtered_df["home_team"] == target["home_team"]) & (filtered_df["match_timestamp"] < target_ts)].sort_values(by="match_timestamp").tail(5)
            past_away = filtered_df[(filtered_df["away_team"] == target["away_team"]) & (filtered_df["match_timestamp"] < target_ts)].sort_values(by="match_timestamp").tail(5)
            home_streak_score = sum([1 if r["home_goals"] > r["away_goals"] else -1 for _, r in past_home.iterrows()])
            away_streak_score = sum([1 if r["away_goals"] > r["home_goals"] else -1 for _, r in past_away.iterrows()])
            
            # --- CORE VARIABLE ATTACK VECTOR SEQUENCING ARMOUR ---
            league_key = str(selected_league_filter).lower().strip()
            baseline_goals = 2.65
            if 'engine' in globals() and hasattr(engine, 'COMPETITION_MATRIX'):
                baseline_goals = engine.COMPETITION_MATRIX.get(league_key, {"baseline_goals": 2.65}).get("baseline_goals", 2.65)
            
            h_status = "stable"
            a_status = "stable"
            
            weather_goals_multiplier = 1.00
            coach_attack_multiplier = 1.00
            coach_volatility_expansion = 1.00
            home_injury_penalty = 1.00
            away_injury_penalty = 1.00
            home_travel_multiplier = 1.00
            away_travel_multiplier = 1.00
            home_lookahead_penalty = 1.00
            away_lookahead_penalty = 1.00
            referee_volatility_expansion = 1.00
            visitor_surface_penalty = 1.00
            home_pitch_width_modifier = 1.00
            home_style_modifier = 1.00
            away_style_modifier = 1.00
            calibrated_home_attack = 1.00
            calibrated_away_attack = 1.00
            
            home_tactical_style = "Standard Balanced / Unspecified"
            away_tactical_style = "Standard Balanced / Unspecified"
            weather_condition_selection = "Optimal / Standard Ambient / Indoor Dome"
            tournament_framework_selection = "Standard Domestic League Match"
            coach_stability_selection = "Stable Baseline / Standard Tenure"
            lookahead_match_active = "None / Standard Focus Match"
            referee_strictness_profile = "Standard Baseline / Moderate Official"
        # ==============================================================================
# SEGMENT 10A OF 12: LEFT PANEL INPUT OVERRIDES WORKSPACE
# ==============================================================================
            # --- STEP 1: OPEN WIDESCREEN GRID CHANNELS ---
            dash_left, dash_right = st.columns(2)
            
            # --- STEP 2: RENDER STRATEGIC INPUT OVERRIDES (LEFT PANEL) ---
            with dash_left:
                st.markdown("### ⛅ Strategic Overrides & Context")
                with st.expander("📊 Venue Momentum & Streak Strengths", expanded=True):
                    st.info(f"🏟️ {target['home_team']} Streak Index: {home_streak_score:+} Units")
                    st.info(f"🚀 {target['away_team']} Streak Index: {away_streak_score:+} Units")
                with st.expander("⚙️ Strategic Matchday Weather & Format Conditions", expanded=False):
                    weather_condition_selection = st.selectbox("Current Matchday Weather Climate:", ["Optimal / Standard Ambient / Indoor Dome", "Heavy Rain / High Pitch Slick Surface", "Extreme High Wind / Aerodynamic Drag Line"])
                    tournament_framework_selection = st.selectbox("Competition Tournament Format Stage:", ["Standard Domestic League Match", "🏆 Neutral-Site Tournament Group Stage", "💀 Knockout Round (Extra-Time Risk)"])
                    coach_stability_selection = st.selectbox("Host Team Coach Stability Status:", ["Long-Term Stability (2+ Years)", "Stable Baseline / Standard Tenure", "Recent Appointment / Caretaker Setup", "🚨 Public Dressing Room Friction"])
                with st.expander("🏥 Team News Injury Sliders & Travel Friction", expanded=False):
                    home_tactical_style = st.selectbox("Home Tactical Blueprint Style:", ["Standard Balanced / Unspecified", "High-Possession Pressing", "Fast Transition Counter-Attack", "Deep Ultra-Defensive Low-Block"])
                    away_tactical_style = st.selectbox("Away Tactical Blueprint Style:", ["Standard Balanced / Unspecified", "High-Possession Pressing", "Fast Transition Counter-Attack", "Deep Ultra-Defensive Low-Block"])
                    home_heavy_travel = st.checkbox("🚨 Home Team: Long-Distance Travel Exposure Check", value=False)
                    away_heavy_travel = st.checkbox("🚨 Away Team: Long-Distance Travel Exposure Check", value=False)
                    home_missing_talent_tier = st.select_slider("Home Key Player Injury / Suspension Severity:", options=["Full Strength Squad", "Tier 2 Depth Missing (5% Cap)", "Tier 1 Engine Asset Missing (15% Cap)"], value="Full Strength Squad")
                    away_missing_talent_tier = st.select_slider("Away Key Player Injury / Suspension Severity:", options=["Full Strength Squad", "Tier 2 Depth Missing (5% Cap)", "Tier 1 Engine Asset Missing (15% Cap)"], value="Full Strength Squad")
                with st.expander("🧠 Referee Profiles, Pitch Blueprints & Rivalries", expanded=False):
                    lookahead_match_active = st.selectbox("Look-Ahead Match Distraction Profile:", ["None / Standard Focus Match", "🏠 Home Team: Massive Impending Cup/Derby Next Week", "✈️ Away Team: Massive Impending Cup/Derby Next Week"])
                    referee_strictness_profile = st.selectbox("Assigned Referee Strictness Profile:", ["Standard Baseline / Moderate Official", "Lenient / High-Flow Context", "🚨 Strict / Cards & Penalties Inclined"])
                    asymmetric_pitch_climate_advantage = st.checkbox("Host Artificial Turf Advantage Active Check", value=False)
                    asymmetric_pitch_width_advantage = st.checkbox("📐 Host Narrow Pitch Blueprint Surface Active Check", value=False)
                    derby_match_active = st.checkbox("🚨 Flag Entry as Local Derby / High Intensity Rivalry Check", value=False)
                with st.expander("💰 Bookmaker Entry Lines & Odds Setup", expanded=True):
                    odds_1 = st.number_input("Home Odds (1):", min_value=1.01, value=2.10, step=0.05, key="o_1")
                    odds_X = st.number_input("Draw Odds (X):", min_value=1.01, value=3.20, step=0.05, key="o_x")
                    odds_2 = st.number_input("Away Odds (2):", min_value=1.01, value=3.40, step=0.05, key="o_2")
                    odds_over = st.number_input("Over 2.5 Goals Odds:", min_value=1.01, value=1.95, step=0.05, key="o_ov")
                    odds_under = st.number_input("Under 2.5 Goals Odds:", min_value=1.01, value=1.85, step=0.05, key="o_un")
                    odds_correct_score = st.number_input("Target Correct Score Odds:", min_value=1.01, value=7.50, step=0.10, key="o_cs")
# ==============================================================================
# SEGMENT 10B OF 12: ENGINE PROBABILITY CALCULATION CORE LAYER
# ==============================================================================
            # --- STEP 3: RUN THE ADVANCED MATHEMATICAL THREE-STAGE OPTIMIZATION ENGINE ---
            # 📍 SEGMENT 10A: HISTORICAL FORM LOOKBACK MATRIX PASS
            h_past_sot = filtered_df[filtered_df["home_team"] == target["home_team"]]["home_sot"].mean() if len(filtered_df) > 0 else 4.0
            a_past_sot = filtered_df[filtered_df["away_team"] == target["away_team"]]["away_sot"].mean() if len(filtered_df) > 0 else 3.5
            h_past_bc = filtered_df[filtered_df["home_team"] == target["home_team"]]["home_big_chances"].mean() if len(filtered_df) > 0 else 1.2
            a_past_bc = filtered_df[filtered_df["away_team"] == target["away_team"]]["away_big_chances"].mean() if len(filtered_df) > 0 else 0.9
            pythagorean_luck_ratio = (h_past_sot ** 2) / (h_past_sot ** 2 + a_past_sot ** 2) if (h_past_sot + a_past_sot) > 0 else 0.50

            # 📍 INLINE DYNAMIC SOS EQUALIZER COUPLING
            home_sos_equalizer, away_sos_equalizer = 1.00, 1.00
            if 'resolved_standings_df' in globals() and not resolved_standings_df.empty:
                resolved_standings_df.columns = [str(c).strip().lower() for c in resolved_standings_df.columns]
                target_team_column_key = "team" if "team" in resolved_standings_df.columns else ("squad" if "squad" in resolved_standings_df.columns else "")
                if target_team_column_key != "" and not filtered_df.empty:
                    total_table_teams = len(resolved_standings_df)
                    home_opponents = filtered_df[(filtered_df["home_team"] == target["home_team"]) | (filtered_df["away_team"] == target["home_team"])].tail(5)
                    away_opponents = filtered_df[(filtered_df["home_team"] == target["away_team"]) | (filtered_df["away_team"] == target["away_team"])].tail(5)
                    def compute_inline_sos(opp_df, active_team, col_key):
                        positions = []
                        for _, gm in opp_df.iterrows():
                            opp = str(gm["away_team"]).strip().lower() if str(gm["home_team"]).strip().lower() == active_team.lower() else str(gm["home_team"]).strip().lower()
                            look = resolved_standings_df[resolved_standings_df[col_key] == opp]
                            if not look.empty: positions.append(int(look.index) + 1)
                        if positions:
                            avg_opp_pos = sum(positions) / len(positions)
                            return 1.10 if avg_opp_pos <= (total_table_teams * 0.35) else (0.90 if avg_opp_pos >= (total_table_teams * 0.65) else 1.00)
                        return 1.00
                    home_sos_equalizer = compute_inline_sos(home_opponents, target["home_team"], target_team_column_key)
                    away_sos_equalizer = compute_inline_sos(away_opponents, target["away_team"], target_team_column_key)

            # 📍 TRANSLATE MANUAL MATRICES CONDITIONAL PACKETS
            home_motivation_multiplier, away_motivation_multiplier = 1.00, 1.00
            tournament_neutral_active = "Neutral" in tournament_framework_selection or "Knockout" in tournament_framework_selection
            knockout_volatility_boost = 1.15 if "Knockout" in tournament_framework_selection else 1.00
            if 'resolved_standings_df' in globals() and not resolved_standings_df.empty and not tournament_neutral_active:
                if "team" in resolved_standings_df.columns:
                    home_match_row = resolved_standings_df[resolved_standings_df["team"] == str(target["home_team"]).strip().lower()]
                    if not home_match_row.empty:
                        home_position = int(home_match_row.index) + 1
                        if home_position <= 4: home_motivation_multiplier = 1.12
                        elif home_position >= (len(resolved_standings_df) - 3): home_motivation_multiplier = 1.15

            weather_goals_multiplier = 0.92 if weather_condition_selection == "Heavy Rain / High Pitch Slick Surface" else (0.88 if "Wind" in weather_condition_selection else 1.00)
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
            
            # 📍 SEGMENT 10B (STAGE 2): GOAL-CONVERSION EFFICIENCY MULTIPLIER
            h_recent_g = filtered_df[filtered_df["home_team"] == target["home_team"]]["home_goals"].tail(5).mean()
            a_recent_g = filtered_df[filtered_df["away_team"] == target["away_team"]]["away_goals"].tail(5).mean()
            h_recent_g_val = h_recent_g if pd.notna(h_recent_g) else 1.5
            a_recent_g_val = a_recent_g if pd.notna(a_recent_g) else 1.1
            home_conversion_efficiency = max(0.80, min(1.20, h_recent_g_val / max(0.5, (h_past_bc * 0.38) + (h_past_sot * 0.12))))
            away_conversion_efficiency = max(0.80, min(1.20, a_recent_g_val / max(0.5, (a_past_bc * 0.38) + (a_past_sot * 0.12))))

            home_shot_quality_ratio = (h_past_bc + 1.0) / (h_past_sot + 1.0)
            away_shot_quality_ratio = (a_past_bc + 1.0) / (a_past_sot + 1.0)
            home_style_modifier, away_style_modifier = 1.00, 1.00
            if home_tactical_style == "High-Possession Pressing" and away_tactical_style == "Fast Transition Counter-Attack":
                home_style_modifier = 0.88; away_style_modifier = 1.10
            elif home_tactical_style == "Deep Ultra-Defensive Low-Block" and away_tactical_style == "High-Possession Pressing":
                away_style_modifier = 0.90

            vol_dampener_adjusted = vol_dampener * coach_volatility_expansion * knockout_volatility_boost * referee_volatility_expansion
            if derby_match_active and not tournament_neutral_active:
                home_motivation_multiplier *= 0.85; vol_dampener_adjusted *= 1.10

            calibrated_home_attack = home_motivation_multiplier * home_shot_quality_ratio * home_sos_equalizer * coach_attack_multiplier * home_injury_penalty * home_travel_multiplier * home_style_modifier * home_lookahead_penalty * home_pitch_width_modifier * home_conversion_efficiency
            calibrated_away_attack = away_motivation_multiplier * away_shot_quality_ratio * away_sos_equalizer * away_injury_penalty * away_travel_multiplier * away_style_modifier * away_lookahead_penalty * visitor_surface_penalty * away_conversion_efficiency
            calibrated_baseline_goals = baseline_goals * weather_goals_multiplier
            if "Knockout" in tournament_framework_selection: calibrated_baseline_goals *= 0.88
            if pythagorean_luck_ratio > 0.65: calibrated_baseline_goals *= 0.95 
                                                                          # ==============================================================================
# SEGMENT 10C OF 12 (PART A): CORES EMITS MAPS & PROBABILITY VALUATIONS
# ==============================================================================
            res = engine.predict_match_probabilities(filtered_df, target["home_team"], target["away_team"], target_ts, calibrated_baseline_goals, calibrated_home_attack, calibrated_away_attack, h_status, a_status, max_score_cap, vol_dampener_adjusted, False)
            h_s = engine.parse_live_team_averages(filtered_df, target["home_team"], target_ts, half_life_days, h_status, False)
            a_s = engine.parse_live_team_averages(filtered_df, target["away_team"], target_ts, half_life_days, a_status, False)

            prob_home = res["market_probabilities"]["1 (Home Win)"]
            prob_draw = res["market_probabilities"]["X (Draw)"]
            prob_away = res["market_probabilities"]["2 (Away Win)"]
            prob_matrix = res["raw_matrix"]
            
            # 📍 SEGMENT 10B (STAGE 3): BIVARIATE SKELLAM DRAW RE-BALANCER
            exp_h_total_goals = float(h_s.get("avg_goals_scored", 1.5)) * calibrated_home_attack
            exp_a_total_goals = float(a_s.get("avg_goals_scored", 1.1)) * calibrated_away_attack
            if (exp_h_total_goals + exp_a_total_goals) < 2.30:
                skellam_bessel_corrective_factor = max(1.02, min(1.22, 1.0 + (0.5 * (exp_h_total_goals * exp_a_total_goals))))
                prob_draw = min(0.85, prob_draw * skellam_bessel_corrective_factor)
                prob_denom = prob_home + prob_draw + prob_away
                prob_home /= prob_denom; prob_draw /= prob_denom; prob_away /= prob_denom

            over_25_p, btts_yes_p, home_cs_p, away_cs_p = 0.0, 0.0, 0.0, 0.0
            home_over_15_p, away_over_15_p = 0.0, 0.0
            ah_home_minus_15_p, ah_home_plus_15_p = 0.0, 0.0
            
            # Unpack shape tuple coordinates explicitly to clear typeerror crashes
            max_r = int(prob_matrix.shape[0])
            max_a = int(prob_matrix.shape[1])
            graph_data_dict = {}
            scoreline_scenarios_list = []

            for r_idx in range(max_r):
                for a_idx in range(max_a):
                    cell_p = prob_matrix[r_idx, a_idx]
                    if r_idx == a_idx and (exp_h_total_goals + exp_a_total_goals) < 2.30: prob_matrix[r_idx, a_idx] = cell_p * 1.12
                    cell_p = prob_matrix[r_idx, a_idx]
                    if cell_p >= 0.001: 
                        graph_data_dict[f"{r_idx}-{a_idx}"] = float(cell_p * 100)
                        scoreline_scenarios_list.append({"Scoreline Scenario": f"{r_idx} - {a_idx}", "Probability": cell_p, "Fair Value Odds": 1.0 / cell_p if cell_p > 0 else 999.00})
                    if r_idx + a_idx > 2.5: over_25_p += cell_p
                    if r_idx > 0 and a_idx > 0: btts_yes_p += cell_p
                    if a_idx == 0: home_cs_p += cell_p
                    if r_idx == 0: away_cs_p += cell_p
                    if r_idx > 1.5: home_over_15_p += cell_p
                    if a_idx > 1.5: away_over_15_p += cell_p
                    if r_idx - a_idx > 1.5: ah_home_minus_15_p += cell_p
                    if r_idx - a_idx > -1.5: ah_home_plus_15_p += cell_p

            under_25_p, btts_no_p = 1.0 - over_25_p, 1.0 - btts_yes_p
            dc_1X_p, dc_X2_p, dc_12_p = min(1.0, prob_home + prob_draw), min(1.0, prob_draw + prob_away), min(1.0, prob_home + prob_away)
            dnb_denom = 1.0 - prob_draw if prob_draw < 1.0 else 1.0
            dnb_1_p, dnb_2_p = prob_home / dnb_denom, prob_away / dnb_denom
            home_under_15_p, away_under_15_p = 1.0 - home_over_15_p, 1.0 - away_over_15_p
            ah_away_plus_15_p, ah_away_minus_15_p = 1.0 - ah_home_minus_15_p, 1.0 - ah_home_plus_15_p
            
            odds_1X, odds_X2, odds_12 = 1.35, 1.65, 1.25
            odds_dnb1, odds_dnb2, odds_btts_y, odds_btts_n = 1.50, 2.45, 1.80, 1.95
            odds_home_over_15, odds_home_under_15 = 2.10, 1.65
            odds_away_over_15, odds_away_under_15 = 3.10, 1.35
            odds_ah_home_minus_15, odds_ah_away_plus_15 = 3.80, 1.25
            odds_ah_home_plus_15, odds_ah_away_minus_15 = 1.18, 5.50
            odds_home_cs_y, odds_away_cs_y = 2.60, 3.90
                                                      # ==============================================================================
# SEGMENT 10C OF 12 (PART B): RIGHT UI PANEL AND EXACT SCORE MATRIX
# ==============================================================================
            all_markets_rendered_rows = [
                {"Betting Market": "HOME WIN (1)", "Bookmaker Odds": f"{odds_1:.2f}", "Model Probability": f"{prob_home*100:.1f}%"},
                {"Betting Market": "DRAW MATCH (X)", "Bookmaker Odds": f"{odds_X:.2f}", "Model Probability": f"{prob_draw*100:.1f}%"},
                {"Betting Market": "AWAY WIN (2)", "Bookmaker Odds": f"{odds_2:.2f}", "Model Probability": f"{prob_away*100:.1f}%"},
                {"Betting Market": "DOUBLE CHANCE (1X)", "Bookmaker Odds": f"{odds_1X:.2f}", "Model Probability": f"{dc_1X_p*100:.1f}%"},
                {"Betting Market": "DOUBLE CHANCE (X2)", "Bookmaker Odds": f"{odds_X2:.2f}", "Model Probability": f"{dc_X2_p*100:.1f}%"},
                {"Betting Market": "DOUBLE CHANCE (12)", "Bookmaker Odds": f"{odds_12:.2f}", "Model Probability": f"{dc_12_p*100:.1f}%"},
                {"Betting Market": "DRAW NO BET (DNB1)", "Bookmaker Odds": f"{odds_dnb1:.2f}", "Model Probability": f"{dnb_1_p*100:.1f}%"},
                {"Betting Market": "DRAW NO BET (DNB2)", "Bookmaker Odds": f"{odds_dnb2:.2f}", "Model Probability": f"{dnb_2_p*100:.1f}%"},
                {"Betting Market": "OVER 2.5 GOALS", "Bookmaker Odds": f"{odds_over:.2f}", "Model Probability": f"{over_25_p*100:.1f}%"},
                {"Betting Market": "UNDER 2.5 GOALS", "Bookmaker Odds": f"{odds_under:.2f}", "Model Probability": f"{under_25_p*100:.1f}%"},
                {"Betting Market": "BOTH TEAMS TO SCORE (YES)", "Bookmaker Odds": f"{odds_btts_y:.2f}", "Model Probability": f"{btts_yes_p*100:.1f}%"},
                {"Betting Market": "BOTH TEAMS TO SCORE (NO)", "Bookmaker Odds": f"{odds_btts_n:.2f}", "Model Probability": f"{btts_no_p*100:.1f}%"},
                {"Betting Market": "HOME TOTAL GOALS OVER 1.5", "Bookmaker Odds": f"{odds_home_over_15:.2f}", "Model Probability": f"{home_over_15_p*100:.1f}%"},
                {"Betting Market": "HOME TOTAL GOALS UNDER 1.5", "Bookmaker Odds": f"{odds_home_under_15:.2f}", "Model Probability": f"{home_under_15_p*100:.1f}%"},
                {"Betting Market": "AWAY TOTAL GOALS OVER 1.5", "Bookmaker Odds": f"{odds_away_over_15:.2f}", "Model Probability": f"{away_over_15_p*100:.1f}%"},
                {"Betting Market": "AWAY TOTAL GOALS UNDER 1.5", "Bookmaker Odds": f"{odds_away_under_15:.2f}", "Model Probability": f"{away_under_15_p*100:.1f}%"},
                {"Betting Market": "ASIAN HANDICAP (HOME -1.5)", "Bookmaker Odds": f"{odds_ah_home_minus_15:.2f}", "Model Probability": f"{ah_home_minus_15_p*100:.1f}%"},
                {"Betting Market": "ASIAN HANDICAP (AWAY +1.5)", "Bookmaker Odds": f"{odds_ah_away_plus_15:.2f}", "Model Probability": f"{ah_away_plus_15_p*100:.1f}%"},
                {"Betting Market": "ASIAN HANDICAP (HOME +1.5)", "Bookmaker Odds": f"{odds_ah_home_plus_15:.2f}", "Model Probability": f"{ah_home_plus_15_p*100:.1f}%"},
                {"Betting Market": "ASIAN HANDICAP (AWAY -1.5)", "Bookmaker Odds": f"{odds_ah_away_minus_15:.2f}", "Model Probability": f"{ah_away_minus_15_p*100:.1f}%"},
                {"Betting Market": "HOME CLEAN SHEET (YES)", "Bookmaker Odds": f"{odds_home_cs_y:.2f}", "Model Probability": f"{home_cs_p*100:.1f}%"},
                {"Betting Market": "AWAY CLEAN SHEET (YES)", "Bookmaker Odds": f"{odds_away_cs_y:.2f}", "Model Probability": f"{away_cs_p*100:.1f}%"}
            ]
            stress_rows = [{"Friction Profile": "Baseline Execution", "Projected Draw": f"{prob_draw*100:.1f}%"}]
            sd = len(past_home) + len(past_away)
            confidence = min(100, int((sd / 10.0) * 100)) if sd > 0 else 50
            qualified_projections = []

            with dash_right:
                st.markdown("### 📊 Value Analytics & Tickets")
                highest_ev_found = (prob_home * odds_1) - 1.0
                if prob_home * odds_1 > 1.05 and confidence >= confidence_floor_input:
                    st.success("🔥 ELITE PROJECTIONS UNLOCKED (+5.0% EV Edge Verified)")
                    qualified_projections.append(("HOME WIN (1)", highest_ev_found, prob_home, odds_1, 2.50, "HIGH VALUE"))
                else: st.error("📉 SELECTION REJECTED: Internal profit limits deficit bounds.")
                    
                with st.expander("🎯 Exact Scoreline Probability Graph & Distribution", expanded=True):
                    if graph_data_dict: st.bar_chart(pd.DataFrame(list(graph_data_dict.items()), columns=["Scoreline", "Probability (%)"]).set_index("Scoreline"), use_container_width=True)
                
                with st.expander("🎯 Exact Scoreline Valuation Matrix (Top 10 Scenarios)", expanded=False):
                    st.markdown("🔒 *Tucked away safely to eliminate mobile phone scrolling lag.*")
                    if scoreline_scenarios_list:
                        scoreline_display_df = pd.DataFrame(scoreline_scenarios_list)
                        scoreline_display_df = scoreline_display_df.sort_values(by="Probability", ascending=False).head(10).reset_index(drop=True)
                        scoreline_display_df["Your Input Odds"] = f"{odds_correct_score:.2f}"
                        scoreline_display_df["Calculated EV Edge"] = ((scoreline_display_df["Probability"] * float(odds_correct_score)) - 1.0) * 100
                        
                        def format_scoreline_ev(val): return f"{val:+.1f}%"
                        scoreline_display_df["Calculated EV Edge"] = scoreline_display_df["Calculated EV Edge"].apply(format_scoreline_ev)
                        scoreline_display_df["Model Probability (%)"] = (scoreline_display_df["Probability"] * 100).apply(lambda x: f"{x:.1f}%")
                        scoreline_display_df["Fair Value Odds"] = scoreline_display_df["Fair Value Odds"].apply(lambda x: f"{x:.2f}")
                        st.dataframe(scoreline_display_df[["Scoreline Scenario", "Model Probability (%)", "Fair Value Odds", "Your Input Odds", "Calculated EV Edge"]], use_container_width=True, hide_index=True)

                with st.expander("⚡ Real-Time Game-State Friction Stress Tester", expanded=False):
                    st.dataframe(pd.DataFrame(stress_rows), use_container_width=True, hide_index=True)
                st.markdown("#### 🎫 Complete 22-Market Options Valuation Sheet")
                st.dataframe(pd.DataFrame(all_markets_rendered_rows), use_container_width=True, hide_index=True)
    # ==============================================================================
# SEGMENT 11 OF 12: TELEGRAM BOT PAGER & BANKROLL INVESTMENTS LEDGER
# ==============================================================================
st.markdown("---")
st.markdown("### 🤖 Telegram Bot Pager Alert Integration")
tg_col1, tg_col2 = st.columns(2)
with tg_col1: telegram_bot_token = st.text_input("Enter Private Telegram Bot Token (API Key):", type="password", value="YOUR_BOT_TOKEN_HERE")
with tg_col2: telegram_chat_id = st.text_input("Enter Target Telegram Chat ID Profile Key:", type="password", value="YOUR_CHAT_ID_HERE")

if qualified_projections:
    optimal_bet, best_ev, best_prob, best_odds, fractional_scale_stake, bet_rec = "HOME WIN (1)", highest_ev_found if 'highest_ev_found' in locals() else 0.05, prob_home, odds_1, 2.50, "HIGH VALUE PREMIUM TICKET"
else: optimal_bet, best_ev, best_prob, best_odds, fractional_scale_stake, bet_rec = "NO COMPREHENSIVE SELECTION MET FLOORS", 0.00, 0.00, 2.00, 0.00, "❌ NO BET"

c_col_l, c_col_r = st.columns(2)
with c_col_l:
    st.markdown("### 📊 Live Analytics Monitor")
    st.metric("Match Confidence Value", f"{confidence}%")
    st.metric("Value Threshold Rating", bet_rec)
    st.markdown("### 🧠 Model Tactical Rationale Breakdown")
    st.markdown(f"• **Dominant Threat Metrics Trace**: Home team recent shooting efficiency averages **{h_past_bc:.2f} big chances** from **{h_past_sot:.2f} SOT** relative to Traveling Road parameters of **{a_past_bc:.2f} big chances** from **{a_past_sot:.2f} SOT**.")

    if "HIGH VALUE" in bet_rec and telegram_bot_token != "YOUR_BOT_TOKEN_HERE" and telegram_chat_id != "YOUR_CHAT_ID_HERE":
        telegram_alert_payload_text = f"🔥 HIGH VALUE PREMIUM TICKET UNLOCKED! 🔥\n\n📋 MATCH : {target['home_team']} vs {target['away_team']}\n🎯 TARGET : {optimal_bet}\n📈 VALUE : +{best_ev * 100:.1f}% EV Edge\n🏦 STAKE : {fractional_scale_stake}% Quarter-Kelly\n\n⚡ Sisonke Pager Active"
        encoded_tg_msg = telegram_alert_payload_text.replace(" ", "%20").replace("\n", "%0A")
        try:
            tg_conn = http.client.HTTPSConnection("api.telegram.org", timeout=5)
            tg_conn.request("GET", f"/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={encoded_tg_msg}")
            tg_conn.close()
        except: pass

with c_col_r:
    st.markdown("### 🎫 Calibrated Ticket Slip")
    ticket_string_content = f"MATCH PROFILE : {target['home_team']} vs {target['away_team']}\nRATING TIER TAG : {bet_rec}\nTARGET MARKET : {optimal_bet}\nEXPECTED VALUE : +{best_ev*100:.2f}%\nKELLY STAKE : {fractional_scale_stake}%\nCONFIDENCE RATE : {confidence}%"
    st.text_area("Ticket Log Slip View", value=ticket_string_content, height=140)
    
    st.markdown("---")
    st.markdown("### 🏦 Sisonke Investment Ledger Room")
    ledger_path = "master_bankroll_ledger.csv"
    if not os.path.exists(ledger_path): pd.DataFrame(columns=["Timestamp", "Match", "Market", "Model_Prob", "Entry_Odds", "Closing_Odds", "CLV_Edge_Pct", "Kelly_Stake_Pct", "Outcome", "Net_Profit_Units"]).to_csv(ledger_path, index=False)
    try: display_replicated_ledger_df = pd.read_csv(ledger_path)
    except: display_replicated_ledger_df = pd.DataFrame()

    with st.form("ledger_commit_form"):
        closing_odds_input = st.number_input("Enter Bookmaker Final Closing Odds:", min_value=1.01, value=float(best_odds), step=0.05)
        match_outcome_selection = st.selectbox("Select Actual Match Reality Outcome Check:", ["Pending / Unplayed", "Won Match", "Lost Match", "Void / Refunded"])
        submit_ledger_entry = st.form_submit_button("💾 Save Ticket to Hard Drive Ledger")
        
        if submit_ledger_entry and "NO COMPREHENSIVE" not in optimal_bet:
            clv_edge_margin_pct = round(((1.0/float(best_odds)) - (1.0/float(closing_odds_input))) * 100, 2)
            net_units = round(fractional_scale_stake * (float(best_odds) - 1.0), 2) if match_outcome_selection == "Won Match" else (-fractional_scale_stake if match_outcome_selection == "Lost Match" else 0.0)
            new_replicated_row = {"Timestamp": datetime.datetime.now().strftime("%Y-%m-%d"), "Match": f"{target['home_team']} vs {target['away_team']}", "Market": optimal_bet, "Model_Prob": f"{best_prob*100:.1f}%", "Entry_Odds": best_odds, "Closing_Odds": closing_odds_input, "CLV_Edge_Pct": f"{clv_edge_margin_pct:+.2f}%", "Kelly_Stake_Pct": f"{fractional_scale_stake:.2f}%", "Outcome": match_outcome_selection, "Net_Profit_Units": net_units}
            updated_ledger_disk_df = pd.concat([display_replicated_ledger_df, pd.DataFrame([new_replicated_row])], ignore_index=True)
            updated_ledger_disk_df.to_csv(ledger_path, index=False)
            st.toast("💾 Replicated Ledger Row Backup Complete!")
            st.rerun()

    if not display_replicated_ledger_df.empty:
        display_replicated_ledger_df["Cumulative_Units"] = display_replicated_ledger_df["Net_Profit_Units"].cumsum()
        st.line_chart(display_replicated_ledger_df["Cumulative_Units"], use_container_width=True)
# ==============================================================================
# SEGMENT 12 OF 12: CAMPAIGNS TABLES, BSS CALIBRATOR & MULTI-MARKET LEDGER
# ==============================================================================
with tab_tables:
    st.markdown("### 🏆 Campaign Entry Ledger Frameworks")
    all_participating_teams = sorted(list(filtered_df["home_team"].unique())) if not filtered_df.empty else []
    
    if all_participating_teams:
        st.caption("Configure team simulation metrics below:")
        bookmaker_odds_map, depth_index_map, congestion_map = {}, {}, {}
        sack_floor_map, transfer_boost_map, departure_decay_map, pitch_width_map = {}, {}, {}, {}
        
        preseason_turnover_rate = st.sidebar.slider("Pre-Season Turnover Decay Rate", 0.85, 1.15, 1.00, 0.02)
        for squad in all_participating_teams:
            bookmaker_odds_map[squad] = 15.0; depth_index_map[squad] = 1.0; congestion_map[squad] = False
            sack_floor_map[squad] = 1.10; transfer_boost_map[squad] = 1.0; departure_decay_map[squad] = 1.0; pitch_width_map[squad] = 1.0

        outright_simulation_scoreboard = {team: 0 for team in all_participating_teams}
        mock_schedule_fixtures = [{"home": h, "away": a} for h in all_participating_teams for a in all_participating_teams if h != a]
        
        if mock_schedule_fixtures:
            for iteration in range(1000):
                iteration_points_registry = {team: 0 for team in all_participating_teams}
                iteration_games_played = {team: 0 for team in all_participating_teams}
                manager_sacked_registry = {team: False for team in all_participating_teams}
                
                for index_f, fix in enumerate(mock_schedule_fixtures):
                    sim_baseline_goals = baseline_goals * preseason_turnover_rate
                    iteration_games_played[fix["home"]] += 1; iteration_games_played[fix["away"]] += 1
                    
                    if index_f > (len(mock_schedule_fixtures) * 0.85):
                        top_team_interim = max(iteration_points_registry, key=iteration_points_registry.get)
                        if fix["home"] == top_team_interim: sim_baseline_goals *= 0.78
                    
                    home_sack_bounce, away_sack_bounce = 1.00, 1.00
                    if iteration_games_played[fix["home"]] >= 10:
                        home_current_ppg = iteration_points_registry[fix["
        
