import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import joblib
import os
import datetime
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== 1. PAGE CONFIG & SETUP ====================
st.set_page_config(page_title="VayuPrahari AI Sentinel", page_icon="🌬️", layout="wide")

# Modern High-Tech Sentinel Theme & Custom Design Tokens
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Base Reset & Layout Centering */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: #0a0e17 !important;
    background-image: 
        radial-gradient(circle at 10% 8%, rgba(6, 182, 212, 0.08) 0%, transparent 45%),
        radial-gradient(circle at 90% 12%, rgba(59, 130, 246, 0.07) 0%, transparent 45%),
        radial-gradient(circle at 50% 95%, rgba(16, 185, 129, 0.06) 0%, transparent 50%) !important;
    color: #f1f5f9 !important;
}

.block-container {
    max-width: 1320px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    margin: 0 auto !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.02em !important;
}

/* Sentinel Top Hero Header */
.sentinel-hero {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.88) 50%, rgba(15, 23, 42, 0.96) 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 20px;
    padding: 24px 30px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
}

.sentinel-hero::after {
    content: '';
    position: absolute;
    top: -40%;
    right: -15%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    flex-wrap: wrap;
}

.pulse-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.14);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34d399;
    padding: 3px 12px;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse-glow 2s infinite ease-in-out;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.35; transform: scale(0.85); }
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 40%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: flex;
    align-items: center;
    gap: 12px;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 0.92rem;
    margin-top: 6px;
}

/* Modern 3-Card Cockpit Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 22px;
}

@media (max-width: 860px) {
    .metrics-grid {
        grid-template-columns: 1fr;
    }
}

.metric-card {
    background: linear-gradient(145deg, rgba(26, 34, 53, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 20px 22px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    border-color: rgba(56, 189, 248, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(6, 182, 212, 0.16);
}

.metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.metric-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #94a3b8;
}

.metric-chip {
    font-size: 0.74rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 9999px;
    letter-spacing: 0.03em;
}

.metric-value {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2.3rem;
    line-height: 1.1;
    margin-bottom: 8px;
}

.metric-footer {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    color: #94a3b8;
}

/* AQI Spectrum Bar */
.aqi-spectrum-wrapper {
    margin-top: 10px;
    padding-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.aqi-spectrum-bar {
    display: flex;
    height: 7px;
    border-radius: 9999px;
    overflow: hidden;
    position: relative;
    background: rgba(255, 255, 255, 0.05);
}

.aqi-seg {
    flex: 1;
    height: 100%;
}
.seg-good { background: #10b981; }
.seg-sat { background: #22c55e; }
.seg-mod { background: #f59e0b; }
.seg-poor { background: #f97316; }
.seg-vpoor { background: #ef4444; }
.seg-sev { background: #991b1b; }

.aqi-needle-track {
    position: relative;
    height: 10px;
    margin-top: 2px;
}

.aqi-needle-indicator {
    position: absolute;
    top: 0;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 6px solid #ffffff;
}

.aqi-spectrum-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.68rem;
    color: #64748b;
    margin-top: 2px;
}

/* Tabs Styling */
div[data-testid="stTabs"] button {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    border-radius: 10px 10px 0 0 !important;
    transition: all 0.2s ease !important;
    color: #94a3b8 !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    background: rgba(56, 189, 248, 0.1) !important;
    border-bottom: 3px solid #38bdf8 !important;
    color: #38bdf8 !important;
}

/* Care Circle Member Card Container */
.member-card-wrapper {
    background: linear-gradient(145deg, rgba(26, 34, 53, 0.8) 0%, rgba(15, 23, 42, 0.92) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    margin-bottom: 12px;
    transition: all 0.25s ease;
}

.member-card-wrapper:hover {
    border-color: rgba(56, 189, 248, 0.4);
    box-shadow: 0 12px 30px rgba(6, 182, 212, 0.14);
}

.member-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 14px;
    gap: 8px;
}

.member-name {
    font-family: 'Outfit', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.role-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    background: rgba(148, 163, 184, 0.14);
    color: #cbd5e1;
    border: 1px solid rgba(148, 163, 184, 0.25);
    margin-top: 4px;
}

.status-badge {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 9999px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    white-space: nowrap;
}

.badge-low {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34d399;
}

.badge-moderate {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: #fbbf24;
}

.badge-caution {
    background: rgba(249, 115, 22, 0.15);
    border: 1px solid rgba(249, 115, 22, 0.4);
    color: #fb923c;
}

.badge-high {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #f87171;
}

.badge-critical {
    background: rgba(220, 38, 38, 0.25);
    border: 1px solid #ef4444;
    color: #fca5a5;
}

.member-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 16px;
    background: rgba(15, 23, 42, 0.5);
    padding: 10px 14px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.meta-item {
    font-size: 0.74rem;
    color: #94a3b8;
}

.meta-item strong {
    color: #f1f5f9;
    display: block;
    font-size: 0.85rem;
    margin-top: 2px;
}

/* Styled Directive Blocks */
.directives-wrapper {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 16px;
}

.directive-card {
    background: rgba(15, 23, 42, 0.55);
    border-radius: 12px;
    padding: 12px 14px;
    border-left: 3px solid #38bdf8;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
    border-right: 1px solid rgba(255, 255, 255, 0.04);
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.directive-card.dir-timing {
    border-left-color: #38bdf8;
}
.directive-card.dir-clinical {
    border-left-color: #f59e0b;
}
.directive-card.dir-pollutant {
    border-left-color: #ec4899;
}
.directive-card.dir-domestic {
    border-left-color: #10b981;
}

.directive-header {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}

.directive-card.dir-timing .directive-header { color: #38bdf8; }
.directive-card.dir-clinical .directive-header { color: #fbbf24; }
.directive-card.dir-pollutant .directive-header { color: #f472b6; }
.directive-card.dir-domestic .directive-header { color: #34d399; }

.directive-text {
    font-size: 0.82rem;
    line-height: 1.45;
    color: #cbd5e1;
    margin: 0;
}

/* Companion Info Card (shown in Solo mode) */
.companion-card {
    background: linear-gradient(145deg, rgba(26, 34, 53, 0.6) 0%, rgba(15, 23, 42, 0.75) 100%);
    border: 1px dashed rgba(56, 189, 248, 0.3);
    border-radius: 18px;
    padding: 24px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.companion-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.companion-text {
    font-size: 0.84rem;
    line-height: 1.55;
    color: #94a3b8;
    margin-bottom: 14px;
}

/* 3-Phase Ventilation Timeline Guide */
.ventilation-guide-card {
    background: linear-gradient(135deg, rgba(26, 34, 53, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 18px;
    padding: 22px 26px;
    margin-top: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.guide-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 10px;
}

.guide-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    display: flex;
    align-items: center;
    gap: 8px;
}

.guide-pill {
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #38bdf8;
    padding: 3px 12px;
    border-radius: 9999px;
    font-size: 0.74rem;
    font-weight: 600;
}

.guide-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}

@media (max-width: 860px) {
    .guide-grid {
        grid-template-columns: 1fr;
    }
}

.guide-box {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 14px;
    padding: 16px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    position: relative;
}

.guide-box-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.caution-box {
    border-left: 3px solid #f97316;
}
.caution-box .guide-box-title { color: #fb923c; }

.safe-box {
    border-left: 3px solid #10b981;
}
.safe-box .guide-box-title { color: #34d399; }

.info-box {
    border-left: 3px solid #38bdf8;
}
.info-box .guide-box-title { color: #38bdf8; }

.guide-box p {
    font-size: 0.82rem;
    color: #cbd5e1;
    margin: 0;
    line-height: 1.45;
}

/* Chat Header Card & Pills */
.chat-header-card {
    background: linear-gradient(135deg, rgba(26, 34, 53, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.chat-context-pills {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 10px;
}

.chat-pill {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #cbd5e1;
    padding: 3px 12px;
    border-radius: 8px;
    font-size: 0.74rem;
    font-weight: 500;
}

/* Streamlit Native Widget Overrides */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

.stButton > button:hover {
    border-color: #38bdf8 !important;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2) !important;
    transform: translateY(-1px) !important;
}

/* Sidebar Dark Theme & Styling */
section[data-testid="stSidebar"] {
    background-color: #0d121f !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
}

/* Expander Polish */
div[data-testid="stExpander"] {
    background: rgba(26, 34, 53, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
}

/* Chat Message Styling */
div[data-testid="stChatMessage"] {
    background: rgba(26, 34, 53, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 14px !important;
    margin-bottom: 10px !important;
}
</style>
""", unsafe_allow_html=True)

def get_aqi_meta(aqi_val):
    """Returns (category_name, hex_color, bg_rgba, border_rgba) based on CPCB AQI standards."""
    try:
        val = int(float(aqi_val))
    except (ValueError, TypeError):
        val = 100
    if val <= 50:
        return "Good", "#10b981", "rgba(16, 185, 129, 0.15)", "rgba(16, 185, 129, 0.4)"
    elif val <= 100:
        return "Satisfactory", "#22c55e", "rgba(34, 197, 94, 0.15)", "rgba(34, 197, 94, 0.4)"
    elif val <= 200:
        return "Moderate", "#f59e0b", "rgba(245, 158, 11, 0.15)", "rgba(245, 158, 11, 0.4)"
    elif val <= 300:
        return "Poor", "#f97316", "rgba(249, 115, 22, 0.15)", "rgba(249, 115, 22, 0.4)"
    elif val <= 400:
        return "Very Poor", "#ef4444", "rgba(239, 68, 68, 0.15)", "rgba(239, 68, 68, 0.4)"
    else:
        return "Severe", "#dc2626", "rgba(220, 38, 38, 0.25)", "rgba(220, 38, 38, 0.6)"

def format_directive_cards(advice_text):
    """Formats raw advisory bullet text into clean, high-contrast micro-cards with dedicated category styling."""
    cards = []
    lines = [l.strip() for l in str(advice_text or "").split("\n") if l.strip()]
    for line in lines:
        clean = line.lstrip("•").strip()
        if "Routine Window" in clean:
            cls = "dir-timing"
            icon = "⏰"
            title = "Routine Window Protocol"
        elif "Sensitivity Action" in clean:
            cls = "dir-clinical"
            icon = "🩺"
            title = "Clinical & Sensitivity Directive"
        elif "Pollutant Defense" in clean:
            cls = "dir-pollutant"
            icon = "🛡️"
            title = "Dominant Pollutant Defense"
        elif "Indoor" in clean or "Safeguard" in clean:
            cls = "dir-domestic"
            icon = "🏠"
            title = "Domestic Ventilation & Filter Protocol"
        else:
            cls = "dir-timing"
            icon = "›"
            title = "Advisory Directive"
            
        body = re.sub(r'^\s*\*\*[^*]+\*\*:\s*', '', clean)
        cards.append(f"""
        <div class="directive-card {cls}">
            <div class="directive-header">{icon} {title}</div>
            <p class="directive-text">{body}</p>
        </div>
        """)
    return f'<div class="directives-wrapper">{"".join(cards)}</div>'

# ==================== 2. DATABASE SETUP (SQLite) ====================
def init_db():
    conn = sqlite3.connect("vrayuprahari.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            vulnerability TEXT,
            routine_time TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cursor.execute("SELECT value FROM app_metadata WHERE key = 'seeded'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO profiles (name, role, vulnerability, routine_time) VALUES (?, ?, ?, ?)",
                       ("Aman (Self)", "Primary User", "Dust Allergy / Commuter", "08:30 AM"))
        cursor.execute("INSERT INTO app_metadata (key, value) VALUES ('seeded', '1')")
    
    # Clean up any existing duplicate profiles in the database
    cursor.execute("""
        DELETE FROM profiles 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM profiles 
            GROUP BY LOWER(TRIM(name)), role, vulnerability, LOWER(TRIM(routine_time))
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_profiles():
    conn = sqlite3.connect("vrayuprahari.db")
    df = pd.read_sql("SELECT * FROM profiles ORDER BY id ASC", conn)
    conn.close()
    if not df.empty:
        # Guarantee identical profile entries never appear more than once on the UI
        df = df.drop_duplicates(subset=['name', 'role', 'vulnerability', 'routine_time'], keep='first')
    return df

def add_profile_db(name, role, vuln, routine):
    clean_name = str(name).strip()
    clean_routine = str(routine).strip()
    conn = sqlite3.connect("vrayuprahari.db")
    cursor = conn.cursor()
    # Check if exact same profile data already exists
    cursor.execute("""
        SELECT id FROM profiles 
        WHERE LOWER(TRIM(name)) = LOWER(?) 
          AND role = ? 
          AND vulnerability = ? 
          AND LOWER(TRIM(routine_time)) = LOWER(?)
    """, (clean_name, role, vuln, clean_routine))
    if cursor.fetchone():
        conn.close()
        return False

    cursor.execute("INSERT INTO profiles (name, role, vulnerability, routine_time) VALUES (?, ?, ?, ?)",
                   (clean_name, role, vuln, clean_routine))
    conn.commit()
    conn.close()
    return True

def delete_profile_db(profile_id):
    conn = sqlite3.connect("vrayuprahari.db")
    cursor = conn.cursor()
    # Explicitly cast to native Python int to ensure SQLite INTEGER matching
    cursor.execute("DELETE FROM profiles WHERE id = ?", (int(profile_id),))
    conn.commit()
    conn.close()

# ==================== 3. LOAD TRAINED ML MODEL ====================
model_path = "vayu_rf_model.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error("⚠️ Trained model 'vayu_rf_model.pkl' not found! Please run your 'train_model.py' script first.")
    st.stop()

# ==================== 3.1 DYNAMIC ADVISORY & RISK ENGINE ====================
class AdvisoryResult(tuple):
    """
    Tuple subclass representing personalized air quality advice.
    Supports tuple unpacking: `risk_level, advice = generate_personalized_advice(...)`
    attribute access: `res.risk_level, res.advice`
    and dictionary key lookup: `res['risk_level'], res['advice']`.
    """
    def __new__(cls, risk_level, advice):
        return super().__new__(cls, (risk_level, advice))

    @property
    def risk_level(self):
        return self[0]

    @property
    def advice(self):
        return self[1]

    def __getitem__(self, item):
        if item == 'risk_level':
            return self[0]
        elif item == 'advice':
            return self[1]
        return super().__getitem__(item)

    def get(self, key, default=None):
        if key == 'risk_level':
            return self[0]
        elif key == 'advice':
            return self[1]
        return default

    def to_dict(self):
        return {"risk_level": self[0], "advice": self[1]}

    def keys(self):
        return ["risk_level", "advice"]

    def items(self):
        return [("risk_level", self[0]), ("advice", self[1])]

    def values(self):
        return [self[0], self[1]]


def _parse_routine_hour(routine_time):
    """Safely extracts 24-hour integer from routine_time string."""
    if not routine_time or not isinstance(routine_time, str):
        return None
    time_str = routine_time.strip().upper()
    for fmt in ["%I:%M %p", "%I:%M%p", "%I %p", "%H:%M", "%H:%M:%S"]:
        try:
            return datetime.datetime.strptime(time_str, fmt).time().hour
        except ValueError:
            pass
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?', time_str)
    if match:
        hour = int(match.group(1))
        meridiem = match.group(3)
        if meridiem == "PM" and hour < 12:
            hour += 12
        elif meridiem == "AM" and hour == 12:
            hour = 0
        return hour
    return None


def generate_personalized_advice(predicted_aqi, dominant_pollutant, vulnerability_tag, routine_time):
    """
    Dynamically calculates risk levels and custom micro-advisories based on:
    - ML-predicted AQI
    - Dominant pollutant (e.g. PM2.5, NO2, O3, PM10)
    - User's medical/vulnerability sensitivity stored in SQLite
    - User's routine time (e.g. morning inversion vs afternoon dispersion)
    """
    try:
        aqi_val = int(float(predicted_aqi))
    except (ValueError, TypeError):
        aqi_val = 100

    pollutant = str(dominant_pollutant or "PM2.5 & NO2").strip()
    vuln = str(vulnerability_tag or "Healthy Adult").strip().lower()
    time_str = str(routine_time or "08:00 AM").strip()
    hour = _parse_routine_hour(time_str)

    # 1. Sensitivity Group Classification
    is_copd_asthma = any(k in vuln for k in ["copd", "asthma", "bronch", "respiratory", "cardiac", "heart", "pulmonary"])
    is_senior = any(k in vuln for k in ["senior", "elderly", "aged", "geriatric", "dada", "dadi", "nana", "nani"])
    is_child = any(k in vuln for k in ["child", "infant", "kid", "baby", "pediatric", "toddler"])
    is_allergy_commuter = any(k in vuln for k in ["dust", "allergy", "allergic", "commuter", "worker", "transit", "sinus", "rhinitis"])

    # 2. Atmospheric & Exposure Timing Windows
    is_morning_inversion = hour is not None and (5 <= hour <= 8)
    is_morning_rush = hour is not None and (8 <= hour <= 10)
    is_evening_rush = hour is not None and (18 <= hour <= 21)
    is_afternoon_dispersion = hour is not None and (11 <= hour <= 15)

    # 3. Dynamic Multi-Factor Risk Score
    if aqi_val <= 50:
        base_score = 1
    elif aqi_val <= 100:
        base_score = 2
    elif aqi_val <= 200:
        base_score = 3
    elif aqi_val <= 300:
        base_score = 4
    elif aqi_val <= 400:
        base_score = 5
    else:
        base_score = 6

    # Vulnerability modifier
    vuln_mod = 0
    if is_copd_asthma:
        vuln_mod = 3 if aqi_val > 150 else 2
    elif is_senior or is_child:
        vuln_mod = 2 if aqi_val > 150 else 1
    elif is_allergy_commuter:
        vuln_mod = 1 if aqi_val > 100 else 0

    # Timing modifier
    timing_mod = 0
    if (is_morning_inversion or is_morning_rush or is_evening_rush) and aqi_val > 120:
        timing_mod = 1
    elif is_afternoon_dispersion and aqi_val <= 200:
        timing_mod = -1

    total_score = max(1, base_score + vuln_mod + timing_mod)

    # Risk badge mapping
    if total_score <= 2:
        risk_level = "🟢 LOW RISK"
    elif total_score <= 4:
        risk_level = "🟡 MODERATE RISK"
    elif total_score == 5:
        risk_level = "🟠 ELEVATED CAUTION"
    elif total_score <= 7:
        risk_level = "🔴 HIGH ALERT"
    else:
        risk_level = "🚨 CRITICAL RISK"

    # 4. Tailored Micro-Advisories
    advisories = []

    # A. Routine Slot & Timing Guidance
    if is_morning_inversion and aqi_val > 120:
        advisories.append(f"• **Routine Window ({time_str}):** Reschedule outdoor outings. Morning thermal inversion traps heavy particulate toxins near ground level; shift exercise to midday.")
    elif is_morning_rush and (is_allergy_commuter or aqi_val > 120):
        advisories.append(f"• **Routine Window ({time_str}):** Morning vehicular traffic peak. Commute with car AC in recirculation mode; avoid waiting along open bus stops or congested junctions.")
    elif is_evening_rush and aqi_val > 120:
        advisories.append(f"• **Routine Window ({time_str}):** Post-sunset cooling is settling traffic emissions. Curtail prolonged outdoor chores.")
    elif is_afternoon_dispersion:
        advisories.append(f"• **Routine Window ({time_str}):** Optimal dispersion slot. Sun warming lifts inversion layer, offering today's lowest ground-level exposure.")
    else:
        if aqi_val > 200:
            advisories.append(f"• **Routine Window ({time_str}):** Regional pollution is severe. Limit continuous outdoor exposure to under 15 minutes during this slot.")
        else:
            advisories.append(f"• **Routine Window ({time_str}):** Regular routine acceptable. Maintain moderate hydration and avoid heavy congestion zones.")

    # B. Vulnerability / Clinical Action
    if is_copd_asthma:
        if aqi_val > 150:
            advisories.append("• **Sensitivity Action (Asthma/COPD):** High bronchospasm hazard. Keep fast-acting rescue inhaler handy, monitor SpO2, and avoid cold air inhalation.")
        else:
            advisories.append("• **Sensitivity Action (Asthma/COPD):** Mild airway irritation possible. Keep preventative medications nearby and avoid rapid outdoor exertion.")
    elif is_senior:
        if aqi_val > 150:
            advisories.append("• **Sensitivity Action (Senior Citizen):** Elevated cardiovascular stress. Strictly avoid outdoor walking; replace with gentle indoor mobility exercises.")
        else:
            advisories.append("• **Sensitivity Action (Senior Citizen):** Protect lungs with light outdoor coverage; avoid uphill or fast-paced walks.")
    elif is_child:
        if aqi_val > 150:
            advisories.append("• **Sensitivity Action (Child/Pediatric):** Children's lung intake rate is heightened. Restrict all outdoor playground and sports activities today.")
        else:
            advisories.append("• **Sensitivity Action (Child/Pediatric):** Keep outdoor playtime moderate; encourage frequent hydration to flush airway irritants.")
    elif is_allergy_commuter:
        if aqi_val > 100:
            advisories.append("• **Sensitivity Action (Dust Allergy/Commuter):** Fitted N95 respirator mandatory on transit. Rinse eyes and use saline nasal spray after returning indoors.")
        else:
            advisories.append("• **Sensitivity Action (Commuter):** Use a protective dust mask on two-wheelers or open vehicles.")
    else:
        if aqi_val > 200:
            advisories.append("• **Sensitivity Action (General):** Unhealthy for all groups. Curtail outdoor athletic workouts or heavy manual labor.")
        else:
            advisories.append("• **Sensitivity Action (General):** Good tolerance. No special medical restrictions for standard outdoor tasks.")

    # C. Dominant Pollutant Defense
    pollutant_upper = pollutant.upper()
    if "PM2.5" in pollutant_upper or "PM10" in pollutant_upper or "PARTICULATE" in pollutant_upper:
        advisories.append(f"• **Pollutant Defense ({pollutant}):** Micro-particulates bypass nasal filters and penetrate deep alveoli. Cloth/surgical masks are ineffective—use N95/FFP2.")
    elif "NO2" in pollutant_upper or "NOX" in pollutant_upper:
        advisories.append(f"• **Pollutant Defense ({pollutant}):** Toxic combustion gas irritates bronchial mucosa. Keep a safe distance from diesel trucks and idling buses.")
    elif "O3" in pollutant_upper or "OZONE" in pollutant_upper:
        advisories.append(f"• **Pollutant Defense ({pollutant}):** Strong oxidizing agent triggering chest tightness. Avoid intense afternoon cardio in direct sunlight.")
    elif "CO" in pollutant_upper:
        advisories.append(f"• **Pollutant Defense ({pollutant}):** Reduces oxygen delivery to vital organs. Ensure immediate ventilation in enclosed basements or garages.")
    elif "SO2" in pollutant_upper:
        advisories.append(f"• **Pollutant Defense ({pollutant}):** Acidic gas causes rapid throat constriction. Keep windows facing industrial corridors sealed.")
    else:
        advisories.append(f"• **Pollutant Defense ({pollutant}):** Ambient concentrations elevated. Ensure face protection during extended exposure.")

    # D. Domestic & Indoor Safeguards
    if aqi_val > 200:
        advisories.append("• **Indoor Safeguard:** Keep indoor HEPA air purification running continuously; seal gaps under exterior doors and keep windows shut.")
    elif aqi_val > 100:
        advisories.append("• **Indoor Safeguard:** Run air purifier in sleeping quarters; air out living spaces only during the designated green afternoon window.")
    else:
        advisories.append("• **Indoor Safeguard:** Air quality allows natural indoor cross-ventilation during daytime.")

    return AdvisoryResult(risk_level, "\n".join(advisories))


def calculate_diurnal_safe_window(ml_model, input_features, dominant_pol):
    """
    Dynamically projects a 24-hour atmospheric dispersion curve using diurnal meteorological
    factors (morning thermal inversion, photochemical ozone reaction, and planetary boundary
    layer convective mixing) and runs the trained Random Forest model to compute hourly AQI.
    Identifies the safest continuous 2-hour outdoor window.
    """
    # Diurnal multipliers for urban surface pollution:
    # Particulates & traffic gases (PM2.5, PM10, NOx, CO, NH3) peak during nocturnal/morning inversion
    # (5 AM - 8:30 AM) and evening rush (6 PM - 8 PM), dropping during midday convective mixing (12 PM - 3 PM).
    pm_diurnal = [
        1.10, 1.15, 1.18, 1.20, 1.25, 1.30, 1.35, 1.30, 1.20, 1.05,
        0.90, 0.78, 0.70, 0.68, 0.72, 0.80, 0.92, 1.05, 1.20, 1.25,
        1.20, 1.15, 1.12, 1.10
    ]
    # Ground-level Ozone (O3): Photochemical reaction peaks under strong UV radiation (1 PM - 3:30 PM)
    # and collapses during darkness.
    o3_diurnal = [
        0.35, 0.30, 0.30, 0.28, 0.28, 0.30, 0.45, 0.65, 0.85, 1.10,
        1.35, 1.55, 1.70, 1.75, 1.65, 1.45, 1.20, 0.90, 0.65, 0.50,
        0.42, 0.38, 0.36, 0.35
    ]

    rows = []
    for h in range(24):
        f_pm = pm_diurnal[h]
        f_o3 = o3_diurnal[h]
        row = {}
        for col in input_features.columns:
            val = float(input_features[col].values[0])
            if col == 'O3':
                row[col] = val * f_o3
            elif col == 'SO2':
                row[col] = val * (0.95 + 0.10 * np.sin(h / 24.0 * 2 * np.pi))
            else:
                row[col] = val * f_pm
        rows.append(row)

    diurnal_df = pd.DataFrame(rows)
    hourly_predictions = ml_model.predict(diurnal_df)

    # Evaluate active daytime hours (06:00 AM to 08:00 PM start)
    # Search for the continuous 2-hour window [h, h+2] with minimum average AQI
    window_scores = []
    for start_h in range(6, 20):
        avg_aqi = (hourly_predictions[start_h] + hourly_predictions[start_h + 1]) / 2.0
        window_scores.append((start_h, avg_aqi))

    best_start_h, min_window_aqi = min(window_scores, key=lambda x: x[1])

    def format_hour(h):
        period = "AM" if h < 12 else "PM"
        display_h = h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)
        return f"{display_h}:00 {period}"

    window_str = f"{format_hour(best_start_h)} – {format_hour(best_start_h + 2)}"
    baseline_aqi = int(ml_model.predict(input_features)[0])
    drop_pct = max(0, int(round((1 - (min_window_aqi / max(1, baseline_aqi))) * 100)))

    return {
        "window_str": window_str,
        "best_start_h": best_start_h,
        "min_window_aqi": int(round(min_window_aqi)),
        "baseline_aqi": baseline_aqi,
        "drop_pct": drop_pct,
        "hourly_aqi": [int(round(a)) for a in hourly_predictions]
    }

# ==================== 4. SIDEBAR: LOCATION & CARE CIRCLE ====================
st.sidebar.markdown("""
<div style="padding: 10px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 16px;">
    <div style="font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 800; color: #f8fafc; display: flex; align-items: center; gap: 8px;">
        🌬️ VAYUPRAHARI
    </div>
    <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 2px;">
        Environmental Sentinel & Care Circle
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📍 Location & Target City")
city = st.sidebar.selectbox("Select City", ["Lucknow", "Delhi", "Kanpur", "Varanasi", "Agra"])

st.sidebar.divider()
st.sidebar.markdown("### 👥 Profile & Care Circle")
profiles_df = get_profiles()
mode = "Care-Circle Mode" if len(profiles_df) > 1 else ("Solo Mode" if len(profiles_df) == 1 else "No Profiles Active")
mode_color = "#38bdf8" if len(profiles_df) > 1 else "#34d399"
st.sidebar.markdown(f"""
<div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255,255,255,0.08); padding: 10px 14px; border-radius: 10px; margin-bottom: 14px;">
    <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8; font-weight: 700;">ACTIVE ARCHITECTURE</div>
    <div style="font-size: 0.95rem; font-weight: 700; color: {mode_color}; margin-top: 2px;">{mode}</div>
    <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">{len(profiles_df)} profile(s) synchronized in local SQLite</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar.expander("➕ Add Person / Dependent"):
    with st.form("add_profile_form"):
        p_name = st.text_input("Name / Label")
        p_role = st.selectbox("Role", ["Family Member", "Roommate", "Dependent Senior", "Child"])
        p_vuln = st.selectbox("Vulnerability", ["Healthy Adult", "Asthma / COPD", "Senior Citizen", "Child / Infant"])
        p_time = st.text_input("Main Routine Time", "06:30 AM")
        submitted = st.form_submit_button("Add to Care Circle", use_container_width=True)
        if submitted and p_name.strip():
            added = add_profile_db(p_name, p_role, p_vuln, p_time)
            if added:
                st.rerun()
            else:
                st.warning("⚠️ This exact profile already exists in your Care Circle!")

if not profiles_df.empty:
    with st.sidebar.expander("🗑️ Manage / Remove Profiles"):
        st.caption("Registered Members:")
        for _, row in profiles_df.iterrows():
            st.markdown(f"👤 **{row['name']}** (*{row['role']}*)")
            if st.button(f"🗑️ Delete {row['name']}", key=f"del_side_{row['id']}", use_container_width=True):
                delete_profile_db(row['id'])
                st.rerun()
            st.markdown("---")

# ==================== 5. MAIN APP HEADER ====================
st.markdown(f"""
<div class="sentinel-hero">
    <div class="hero-badge-row">
        <span class="pulse-badge"><span class="pulse-dot"></span> ML INFERENCE ONLINE</span>
        <span class="pulse-badge" style="background: rgba(56, 189, 248, 0.12); border-color: rgba(56, 189, 248, 0.35); color: #38bdf8;">
            📍 {city.upper()} RADAR SECTOR
        </span>
        <span class="pulse-badge" style="background: rgba(168, 85, 247, 0.12); border-color: rgba(168, 85, 247, 0.35); color: #c084fc;">
            👥 {mode.upper()}
        </span>
    </div>
    <div class="hero-title">
        🌬️ VAYUPRAHARI <span style="font-size: 1.1rem; font-weight: 600; color: #38bdf8; letter-spacing: 0.08em; text-transform: uppercase; background: rgba(56, 189, 248, 0.12); padding: 2px 10px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.25);">Sentinel AI</span>
    </div>
    <div class="hero-subtitle">
        Dynamic 24-Hour Atmospheric Dispersion Modeling &bull; Clinical Sensitivity Risk Profiling &bull; Real-Time Action Advisory
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2 = st.tabs(["📅 Daily Action Board & Forecast", "💬 Vayu-Mitra AI Chatbot"])

# ==================== TAB 1: DAILY ACTION BOARD ====================
with tab1:
    # Simulate fetching recent average pollutant readings for the selected city to run automatic inference
    # (In production, this connects to an environmental API or your latest dataset row)
    np.random.seed(hash(city) % 2**32)
    sample_input = pd.DataFrame([[
        np.random.uniform(60, 180),  # PM2.5
        np.random.uniform(100, 250), # PM10
        np.random.uniform(10, 40),   # NO
        np.random.uniform(20, 60),   # NO2
        np.random.uniform(30, 80),   # NOx
        np.random.uniform(10, 30),   # NH3
        np.random.uniform(1.0, 3.5), # CO
        np.random.uniform(10, 50),   # SO2
        np.random.uniform(20, 70)    # O3
    ]], columns=['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3'])
    
    predicted_aqi = int(model.predict(sample_input)[0])
    
    # Dynamically determine the dominant pollutant based on CPCB benchmark ratios
    pollutant_benchmarks = {'PM2.5': 60.0, 'PM10': 100.0, 'NO2': 80.0, 'CO': 2.0, 'SO2': 80.0, 'O3': 100.0}
    ratios = {col: sample_input[col].values[0] / bm for col, bm in pollutant_benchmarks.items() if col in sample_input.columns}
    sorted_p = sorted(ratios.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_p) > 1 and sorted_p[1][1] > 0.75 * sorted_p[0][1]:
        dominant_pollutant = f"{sorted_p[0][0]} & {sorted_p[1][0]}"
    else:
        dominant_pollutant = sorted_p[0][0] if sorted_p else "PM2.5 & NO2"

    # Compute dynamic safe outdoor window from real diurnal dispersion inference
    diurnal_window = calculate_diurnal_safe_window(model, sample_input, dominant_pollutant)
    best_window = diurnal_window["window_str"]
    best_window_aqi = diurnal_window["min_window_aqi"]
    drop_pct = diurnal_window["drop_pct"]

    aqi_cat, aqi_hex, aqi_bg, aqi_border = get_aqi_meta(predicted_aqi)
    needle_pct = max(3, min(97, int(round((predicted_aqi / 500.0) * 100))))

    # 3-Card Cockpit Grid with Visual AQI Spectrum Gauge
    metrics_html = f"""
    <div class="metrics-grid">
        <div class="metric-card" style="border-top: 3px solid {aqi_hex};">
            <div class="metric-header">
                <span class="metric-label">Predicted Regional AQI</span>
                <span class="metric-chip" style="background: {aqi_bg}; color: {aqi_hex}; border: 1px solid {aqi_border};">{aqi_cat}</span>
            </div>
            <div class="metric-value" style="color: {aqi_hex};">{predicted_aqi}</div>
            <div class="aqi-spectrum-wrapper">
                <div class="aqi-spectrum-bar">
                    <div class="aqi-seg seg-good" title="Good (0-50)"></div>
                    <div class="aqi-seg seg-sat" title="Satisfactory (51-100)"></div>
                    <div class="aqi-seg seg-mod" title="Moderate (101-200)"></div>
                    <div class="aqi-seg seg-poor" title="Poor (201-300)"></div>
                    <div class="aqi-seg seg-vpoor" title="Very Poor (301-400)"></div>
                    <div class="aqi-seg seg-sev" title="Severe (401-500)"></div>
                </div>
                <div class="aqi-needle-track">
                    <div class="aqi-needle-indicator" style="left: {needle_pct}%;"></div>
                </div>
                <div class="aqi-spectrum-labels">
                    <span>0 Good</span>
                    <span>100</span>
                    <span>200</span>
                    <span>300</span>
                    <span>400</span>
                    <span>500+</span>
                </div>
            </div>
            <div class="metric-footer" style="margin-top: 8px;">
                <span class="pulse-dot" style="background: {aqi_hex}; box-shadow: 0 0 8px {aqi_hex};"></span>
                <span>Random Forest Inversion Model Active</span>
            </div>
        </div>
        <div class="metric-card" style="border-top: 3px solid #38bdf8;">
            <div class="metric-header">
                <span class="metric-label">Dominant Pollutant</span>
                <span class="metric-chip" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.35);">Primary Driver</span>
            </div>
            <div class="metric-value" style="color: #ffffff; font-size: 1.85rem; padding-top: 4px;">{dominant_pollutant}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 10px 0 14px 0;">
                Micro-particulates & combustion precursors with highest proportional excess over National Ambient Air Quality Standards (NAAQS).
            </div>
            <div class="metric-footer">
                <span>⚠️ Air Quality Limiting Contaminant</span>
            </div>
        </div>
        <div class="metric-card" style="border-top: 3px solid #10b981;">
            <div class="metric-header">
                <span class="metric-label">Safest Outdoor Window</span>
                <span class="metric-chip" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35);">~{best_window_aqi} AQI</span>
            </div>
            <div class="metric-value" style="color: #34d399; font-size: 1.75rem; padding-top: 4px;">{best_window}</div>
            <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.45; margin: 10px 0 14px 0;">
                Midday boundary layer thermal expansion maximizes vertical convective mixing, diluting ground-level particulate concentration.
            </div>
            <div class="metric-footer">
                <span>🟢 {drop_pct}% cleaner than morning inversion peak</span>
            </div>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)

    # Interactive 24-Hour Diurnal AQI & Safe Window Chart
    with st.expander("📈 View 24-Hour Diurnal AQI Forecast & Dispersion Science", expanded=False):
        col_cstat1, col_cstat2, col_cstat3 = st.columns(3)
        col_cstat1.markdown(f"**🟢 Safest Window:** {best_window} (~{best_window_aqi} AQI)")
        col_cstat2.markdown(f"**🔴 Peak Morning Inversion:** 06:00 AM (~{max(diurnal_window['hourly_aqi'])} AQI)")
        col_cstat3.markdown(f"**⚡ Exposure Reduction:** ~{drop_pct}% Cleaner")

        hours_labels = [
            f"{h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)}:00 {'AM' if h < 12 else 'PM'}"
            for h in range(24)
        ]
        diurnal_chart_df = pd.DataFrame({
            "Hour": hours_labels,
            "Predicted Hourly AQI": diurnal_window["hourly_aqi"]
        }).set_index("Hour")
        st.line_chart(diurnal_chart_df, color="#38bdf8")
        st.caption(
            f"💡 **Atmospheric Dispersion Science:** Early morning nocturnal inversions trap ground toxins. "
            f"The safest outdoor window is dynamically calculated as **{best_window}**, when planetary boundary layer convective mixing "
            f"lowers predicted AQI to **~{best_window_aqi}** (~{drop_pct}% cleaner than baseline)."
        )

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 26px 0 14px 0;">
        <div style="font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 700; color: #f8fafc; display: flex; align-items: center; gap: 8px;">
            🛡️ Personal Action Board & Clinical Advisories
        </div>
        <span class="guide-pill">{mode} &bull; {len(profiles_df)} Active</span>
    </div>
    """, unsafe_allow_html=True)

    def render_member_card(row, current_aqi, current_pollutant):
        v_tag = row['vulnerability']
        if row.get('role') and any(k in str(row['role']).lower() for k in ['senior', 'child', 'infant', 'dependent']):
            v_tag = f"{row['vulnerability']} ({row['role']})"

        risk_level, advice = generate_personalized_advice(
            predicted_aqi=current_aqi,
            dominant_pollutant=current_pollutant,
            vulnerability_tag=v_tag,
            routine_time=row['routine_time']
        )

        r_lower = f"{str(row['name'])} {str(row['role'])} {str(row['vulnerability'])}".lower()
        if any(k in r_lower for k in ['senior', 'dada', 'dadi', 'elder', 'aged', 'nana', 'nani']):
            avatar = "👴"
        elif any(k in r_lower for k in ['child', 'kid', 'infant', 'baby', 'toddler']):
            avatar = "🧒"
        elif any(k in r_lower for k in ['asthma', 'copd', 'bronch', 'respiratory']):
            avatar = "🫁"
        elif any(k in r_lower for k in ['commuter', 'dust', 'worker']):
            avatar = "🛵"
        elif any(k in r_lower for k in ['self', 'primary']):
            avatar = "👨‍💼"
        else:
            avatar = "👤"

        if "CRITICAL" in risk_level:
            badge_class = "badge-critical"
            border_color = "#ef4444"
        elif "HIGH" in risk_level:
            badge_class = "badge-high"
            border_color = "#f87171"
        elif "CAUTION" in risk_level or "ELEVATED" in risk_level:
            badge_class = "badge-caution"
            border_color = "#fb923c"
        elif "MODERATE" in risk_level:
            badge_class = "badge-moderate"
            border_color = "#fbbf24"
        else:
            badge_class = "badge-low"
            border_color = "#34d399"

        directives_html = format_directive_cards(advice)

        card_html = f"""
        <div class="member-card-wrapper" style="border-top: 4px solid {border_color};">
            <div class="member-header">
                <div>
                    <div class="member-name">{avatar} {row['name']}</div>
                    <span class="role-badge">{row['role']}</span>
                </div>
                <span class="status-badge {badge_class}">{risk_level}</span>
            </div>
            <div class="member-meta-grid">
                <div class="meta-item">
                    <span>CLINICAL SENSITIVITY</span>
                    <strong>{row['vulnerability']}</strong>
                </div>
                <div class="meta-item">
                    <span>ROUTINE SLOT</span>
                    <strong>⏰ {row['routine_time']}</strong>
                </div>
            </div>
            {directives_html}
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        if st.button(f"🗑️ Remove {row['name']}", key=f"del_card_{row['id']}", use_container_width=True, help=f"Remove {row['name']} from Care Circle"):
            delete_profile_db(row['id'])
            st.rerun()
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    def render_care_circle_guide():
        guide_html = """
        <div class="companion-card">
            <div>
                <div class="companion-title">
                    🛡️ Care Circle Protection Architecture
                </div>
                <p class="companion-text">
                    VayuPrahari customizes environmental health risk calculations based on each family member's clinical profile and daily schedule.
                </p>
                <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 14px;">
                    <div style="background: rgba(15, 23, 42, 0.5); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; border-left: 3px solid #38bdf8;">
                        <strong>👴 Senior Citizens & Children:</strong> Receive early warning alerts at lower particulate thresholds.
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.5); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; border-left: 3px solid #f59e0b;">
                        <strong>🫁 Asthma / Respiratory:</strong> Calibrates bronchodilator & rescue medication precautions.
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.5); padding: 8px 12px; border-radius: 8px; font-size: 0.8rem; border-left: 3px solid #10b981;">
                        <strong>🛵 Commuters / Routine:</strong> Informs vehicle AC recirculation and transit mask mandates.
                    </div>
                </div>
            </div>
            <div style="font-size: 0.78rem; color: #94a3b8; background: rgba(56, 189, 248, 0.08); padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.2);">
                💡 <em>Tip: Add family members or dependents using the sidebar <strong>➕ Add Person / Dependent</strong> form to calibrate individualized alerts.</em>
            </div>
        </div>
        """
        st.markdown(guide_html, unsafe_allow_html=True)

    if profiles_df.empty:
        st.info("ℹ️ No active profiles in your Care Circle. Use the sidebar **➕ Add Person / Dependent** to register a profile.")
    elif len(profiles_df) == 1:
        col_card, col_guide = st.columns([1.15, 0.85])
        with col_card:
            render_member_card(profiles_df.iloc[0], predicted_aqi, dominant_pollutant)
        with col_guide:
            render_care_circle_guide()
    elif len(profiles_df) == 2:
        col1, col2 = st.columns(2)
        with col1:
            render_member_card(profiles_df.iloc[0], predicted_aqi, dominant_pollutant)
        with col2:
            render_member_card(profiles_df.iloc[1], predicted_aqi, dominant_pollutant)
    else:
        cols = st.columns(3)
        for idx, row in profiles_df.iterrows():
            with cols[idx % 3]:
                render_member_card(row, predicted_aqi, dominant_pollutant)

    # 3-Phase Ventilation Timeline Guide
    ventilation_guide_html = f"""
    <div class="ventilation-guide-card">
        <div class="guide-header">
            <div class="guide-title">
                <span>🏡</span> Smart Ventilation & Living Space Diurnal Protocol
            </div>
            <span class="guide-pill">Sector: {city} &bull; Dispersion Sync</span>
        </div>
        <div class="guide-grid">
            <div class="guide-box caution-box">
                <div class="guide-box-title">🛑 Phase 1: Morning Inversion (05:30 – 09:30 AM)</div>
                <p>Keep windows and balcony doors tightly sealed. Ground thermal radiation cooling traps heavy vehicular and combustion pollutants below 100 meters altitude.</p>
            </div>
            <div class="guide-box safe-box">
                <div class="guide-box-title">🟢 Phase 2: Optimal Aeration ({best_window})</div>
                <p>Solar heating lifts the planetary boundary layer. Convective mixing lowers predicted AQI to <strong>~{best_window_aqi}</strong> (<strong>~{drop_pct}% cleaner</strong>). Safest 2-hour slot for cross-ventilation.</p>
            </div>
            <div class="guide-box info-box">
                <div class="guide-box-title">🏠 Phase 3: Nocturnal Protocol (After 06:30 PM)</div>
                <p>Re-seal exterior openings. Activate domestic HEPA purifiers in bedrooms. Use kitchen exhaust extraction during dinner preparation to limit indoor PM2.5 buildup.</p>
            </div>
        </div>
    </div>
    """
    st.markdown(ventilation_guide_html, unsafe_allow_html=True)

# ==================== TAB 2: VAYU-MITRA AI CHATBOT ====================
with tab2:
    # 1. API Key handling
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        try:
            gemini_api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            gemini_api_key = None

    active_city = city if 'city' in locals() else "Lucknow"
    active_aqi = predicted_aqi if 'predicted_aqi' in locals() else 150
    active_dominant = dominant_pollutant if 'dominant_pollutant' in locals() else "PM2.5 & NO2"
    active_window = best_window if 'best_window' in locals() else "11:00 AM – 1:00 PM"
    chat_aqi_cat, _, _, _ = get_aqi_meta(active_aqi)

    profiles_df_chat = get_profiles()

    st.markdown(f"""
    <div class="chat-header-card">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 2rem;">💬</span>
                <div>
                    <div style="font-family: 'Outfit', sans-serif; font-size: 1.35rem; font-weight: 700; color: #f8fafc;">
                        Vayu-Mitra AI Assistant
                    </div>
                    <div style="font-size: 0.82rem; color: #94a3b8;">
                        Context-aware environmental health consultant powered by Google Gemini
                    </div>
                </div>
            </div>
            <div class="chat-context-pills">
                <span class="chat-pill">📍 {active_city}</span>
                <span class="chat-pill">📊 AQI {active_aqi} ({chat_aqi_cat})</span>
                <span class="chat-pill">🕒 Clean Window: {active_window}</span>
                <span class="chat-pill">👥 {len(profiles_df_chat)} Member(s) Linked</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not gemini_api_key:
        st.error("🔑 **GEMINI_API_KEY Missing:** Please set the `GEMINI_API_KEY` environment variable or add it to `.streamlit/secrets.toml` to activate Vayu-Mitra AI.")
        with st.expander("🛠️ Enter Gemini API Key for this Session"):
            temp_key = st.text_input("Gemini API Key", type="password", key="temp_gemini_key", help="Key is stored in-session only.")
            if temp_key:
                gemini_api_key = temp_key.strip()
                st.rerun()

    # Dynamic Context Injection (System Instructions)
    if not profiles_df_chat.empty:
        profiles_summary = []
        for _, p in profiles_df_chat.iterrows():
            profiles_summary.append(
                f"- Name: {p['name']} | Role: {p['role']} | Vulnerability/Sensitivity: {p['vulnerability']} | Routine Slot: {p['routine_time']}"
            )
        care_circle_context = "\n".join(profiles_summary)
    else:
        care_circle_context = "- None registered (Solo user mode)."

    system_instruction = f"""You are "Vayu-Mitra", an empathetic, expert environmental health and personal air-quality assistant for the VayuPrahari Sentinel system.
Your goal is to provide brief, highly practical, and personalized lifestyle, commute, outdoor activity, and health advice based strictly on the live environmental and personal profile data provided below.

=== LIVE DASHBOARD STATE ===
• Target City: {active_city}
• Live ML-Predicted AQI: {active_aqi} ({chat_aqi_cat})
• Dominant Pollutant(s): {active_dominant}
• Recommended Cleanest Outdoor Window: {active_window}

=== REGISTERED CARE CIRCLE PROFILES (From SQLite) ===
{care_circle_context}

=== ADVISORY DIRECTIVES ===
1. Profile-Specific Guidance: When the user asks about an individual, senior, child, or commuter, tailor advice precisely to their vulnerability tag, role, and routine schedule from the Care Circle.
2. Scientific Grounding: Connect every suggestion to the current AQI ({active_aqi}) and dominant pollutant ({active_dominant}). Explain specifically why (e.g., N95 for PM2.5, avoiding morning thermal inversions, avoiding combustion fumes for NO2).
3. Brevity & Tone: Warm, empathetic, yet concise and highly practical. Use clean markdown bullet points. Never provide overly generic non-actionable disclaimers.
4. Language: Fluently handle queries in English, Hindi, or Hinglish.
"""

    # Session State & Chat History Management
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": f"Namaste! I am Vayu-Mitra. Current predicted AQI in {active_city} is **{active_aqi}** ({chat_aqi_cat}, Dominant: **{active_dominant}**). The cleanest outdoor window today is **{active_window}**. How can I assist you or your Care Circle?"}
        ]

    # Quick Suggestion Chips & Clear Chat Controls
    st.markdown("<p style='font-size: 0.78rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;'>💡 Quick Inquiry Suggestions</p>", unsafe_allow_html=True)
    chip_col1, chip_col2, chip_col3, chip_col4, chip_clear = st.columns([2.3, 2.3, 2.3, 2.3, 1.2])
    
    selected_chip_prompt = None
    with chip_col1:
        if st.button("🚶 Morning Walk Safety", key="chip_walk", use_container_width=True):
            selected_chip_prompt = f"Is it safe to go for an outdoor morning walk at our routine times in {active_city} today considering the AQI of {active_aqi}?"
    with chip_col2:
        if st.button("🪟 Balcony Airing Time", key="chip_window", use_container_width=True):
            selected_chip_prompt = f"When is the best time to open balcony windows for fresh air in {active_city} today, and when should we keep them closed?"
    with chip_col3:
        if st.button(f"😷 Mask for {active_dominant}", key="chip_mask", use_container_width=True):
            selected_chip_prompt = f"Given dominant pollutant {active_dominant} and AQI {active_aqi} in {active_city}, what mask or respiratory protection should our family use?"
    with chip_col4:
        if st.button("👶 Pediatric Safety", key="chip_kids", use_container_width=True):
            selected_chip_prompt = f"What precautions are advised for children and infants in {active_city} today with AQI {active_aqi} and dominant {active_dominant}?"
    with chip_clear:
        if st.button("🗑️ Reset", key="btn_clear_chat", use_container_width=True, help="Clear conversation history"):
            st.session_state["messages"] = [
                {"role": "assistant", "content": f"Namaste! I am Vayu-Mitra. Current predicted AQI in {active_city} is **{active_aqi}** ({chat_aqi_cat}, Dominant: **{active_dominant}**). The cleanest outdoor window today is **{active_window}**. How can I assist you or your Care Circle?"}
            ]
            st.rerun()

    # Display conversation history
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input and LLM execution
    chat_placeholder = "Ask about walks, commute, mask protection, or family safety..." if gemini_api_key else "Please provide a GEMINI_API_KEY to ask questions..."
    prompt = st.chat_input(chat_placeholder, disabled=not bool(gemini_api_key))
    if not prompt and selected_chip_prompt:
        prompt = selected_chip_prompt

    if prompt:
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate & Stream Response using google-genai
        with st.chat_message("assistant"):
            try:
                client = genai.Client(api_key=gemini_api_key)

                contents = []
                for msg in st.session_state["messages"]:
                    role = "user" if msg["role"] == "user" else "model"
                    if not contents and role != "user":
                        continue
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )

                candidate_models = ["gemini-3.8-flash", "gemma-4-26b-a4b-it", "gemini-3-flash-preview", "gemini-flash-latest"]
                full_response = None
                last_error = None

                for model_name in candidate_models:
                    try:
                        response_stream = client.models.generate_content_stream(
                            model=model_name,
                            contents=contents,
                            config=types.GenerateContentConfig(
                                system_instruction=system_instruction,
                                temperature=0.7,
                            )
                        )

                        def stream_generator():
                            for chunk in response_stream:
                                if chunk.text:
                                    yield chunk.text

                        full_response = st.write_stream(stream_generator)
                        if full_response:
                            break
                    except Exception as stream_err:
                        last_error = stream_err
                        try:
                            resp = client.models.generate_content(
                                model=model_name,
                                contents=contents,
                                config=types.GenerateContentConfig(
                                    system_instruction=system_instruction,
                                    temperature=0.7,
                                )
                            )
                            if resp.text:
                                full_response = resp.text
                                st.markdown(full_response)
                                break
                        except Exception as direct_err:
                            last_error = direct_err
                            continue

                if full_response:
                    st.session_state["messages"].append({"role": "assistant", "content": full_response})
                elif last_error:
                    raise last_error

            except Exception as e:
                error_msg = f"⚠️ Gemini Assistant Error: {str(e)}"
                st.error(error_msg)
                st.session_state["messages"].append({"role": "assistant", "content": error_msg})