import streamlit as st
import pandas as pd
import base64
import time
from datetime import datetime, date, timedelta

# ==========================================
# 1. KONFIGURASI & INISIALISASI STATE
# ==========================================
st.set_page_config(page_title="Storify - Smart Label & Retail OS", layout="wide", page_icon="🏷️")

def get_ts():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def get_ts_sec():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

soon_exp = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
safe_exp = (date.today() + timedelta(days=90)).strftime("%Y-%m-%d")

defaults = {
    "dark_mode": True,
    "logged_in": False,
    "app_tier": None,
    "active_branch": "Cabang Utama",
    "branches": ["Cabang Utama", "Cabang Karawang Barat"],
    "page": "home",
    "selected_rak": None,
    "epaper_style": "Klasik Terang",
    "epaper_footer": "Harga sudah termasuk PPN",
    "accounts": [
        {"name": "Beatrix", "role": "OWNER", "email": "beatrix@storify.id"},
        {"name": "Natannael", "role": "DEVELOPER", "email": "natannael@storify.id"},
        {"name": "Walden", "role": "DEVELOPER", "email": "walden@storify.id"},
        {"name": "Nathalee", "role": "STAFF", "email": "nathalee@storify.id"},
    ],
    "current_user_idx": 0,
    "logs": [{"time": get_ts_sec(), "type": "INFO", "action": "Sistem Storify & E-Paper Gateway aktif."}],
    "restock_requests": [
        {
            "id": 1, "branch": "Cabang Utama", "rak": "Rak B2", "item": "Keripik Singkong 100g", "qty": 20,
            "by": "Nathalee", "note": "Stok sisa 4 pcs, ramai pembeli.",
            "status": "Belum", "created_at": get_ts(), "resolved_at": "-", "resolved_by": "-"
        }
    ],
    "sales_history": [
        {"time": get_ts(), "branch": "Cabang Utama", "rak": "Rak A1", "item": "Kopi Sachet 25g", "qty": 2, "total": 30000, "cashier": "Nathalee"}
    ],
    "shift_notes": [
        {"time": get_ts(), "branch": "Cabang Utama", "author": "Nathalee", "shift": "Pagi", "note": "Semua label E-Paper rak depan sudah dicek dan menyala normal."}
    ],
    "team_chat": [
        {"sender": "Nathalee", "role": "STAFF", "msg": "Halo kak, Rak B2 keripik singkong sudah hampir habis ya.", "time": get_ts()},
        {"sender": "Beatrix", "role": "OWNER", "msg": "Oke siap, sudah saya catat untuk order ke supplier.", "time": get_ts()}
    ],
    "original_prices": {},
    "flash_sale_active": False,
    "flash_sale_end": 0.0,
    "inventory": {
        "Cabang Utama": {
            "Rak A1": {"item": "Kopi Sachet 25g", "category": "Minuman", "qty": 20, "cost": 11000, "price": 15000, "old_price": None, "exp_date": safe_exp, "battery": 98, "checked_today": True, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300", "inflow": [10, 15, 20], "outflow": [5, 12, 18]},
            "Rak B2": {"item": "Keripik Singkong 100g", "category": "Makanan", "qty": 4, "cost": 8500, "price": 12000, "old_price": None, "exp_date": soon_exp, "battery": 85, "checked_today": False, "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300", "inflow": [5, 8, 10], "outflow": [4, 7, 14]},
            "Rak C3": {"item": "Air Mineral 600ml", "category": "Minuman", "qty": 15, "cost": 3000, "price": 5000, "old_price": None, "exp_date": safe_exp, "battery": 92, "checked_today": True, "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300", "inflow": [15, 25, 30], "outflow": [10, 20, 25]},
            "Rak D4": {"item": "Deterjen Bubuk 800g", "category": "Rumah Tangga", "qty": 8, "cost": 19000, "price": 25000, "old_price": None, "exp_date": safe_exp, "battery": 74, "checked_today": False, "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300", "inflow": [6, 9, 12], "outflow": [3, 7, 10]},
        },
        "Cabang Karawang Barat": {
            "Rak A1": {"item": "Teh Botol 350ml", "category": "Minuman", "qty": 24, "cost": 3200, "price": 4500, "old_price": None, "exp_date": safe_exp, "battery": 96, "checked_today": True, "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=300", "inflow": [12, 24], "outflow": [6, 10]},
            "Rak B1": {"item": "Roti Tawar Kupas", "category": "Makanan", "qty": 3, "cost": 10500, "price": 14000, "old_price": None, "exp_date": soon_exp, "battery": 89, "checked_today": False, "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300", "inflow": [10, 10], "outflow": [8, 9]},
        }
    }
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def add_log(log_type, msg):
    st.session_state.logs.insert(0, {"time": get_ts_sec(), "type": log_type, "action": msg})

# Pastikan indeks akun selalu valid
if st.session_state.current_user_idx >= len(st.session_state.accounts):
    st.session_state.current_user_idx = 0

current_user = st.session_state.accounts[st.session_state.current_user_idx]
is_privileged = current_user["role"] in ["OWNER", "DEVELOPER", "MANAGER"]
tier = st.session_state.app_tier
is_dark = st.session_state.dark_mode

# ==========================================
# GLOBAL THEME & FONT (CLEAN WHITE LIGHT & DEEP DARK MODE)
# ==========================================
if is_dark:
    t = {
        "scheme": "dark",
        "bg": "#060913",
        "bg_grad": "radial-gradient(circle at 15% 0%, rgba(37, 99, 235, 0.14) 0%, transparent 45%), radial-gradient(circle at 85% 10%, rgba(124, 58, 237, 0.12) 0%, transparent 45%)",
        "sidebar_bg": "#0b1120",
        "card_bg": "#0f172a",
        "card_hover": "#3b82f6",
        "card_border": "#1e293b",
        "card_shadow": "0 8px 24px rgba(0, 0, 0, 0.45)",
        "text_main": "#f8fafc",
        "text_muted": "#94a3b8",
        "input_bg": "#162033",
        "input_border": "#2d3b52",
        "popover_bg": "#0f172a",
        "tab_bg": "#131c31",
        "tab_text": "#94a3b8",
        "tab_active_bg": "#1e293b",
        "tab_active_text": "#60a5fa",
        "sec_btn_bg": "#1e293b",
        "sec_btn_text": "#f8fafc",
        "sec_btn_hover_bg": "#2563eb",
        "sec_btn_hover_txt": "#ffffff",
        "sec_btn_border": "#334155",
        "pill_bg": "rgba(59, 130, 246, 0.18)",
        "pill_border": "rgba(96, 165, 250, 0.3)",
        "pill_text": "#93c5fd",
        "price_color": "#60a5fa",
        "pro_price_color": "#a78bfa",
        "badge_ok_bg": "rgba(16, 185, 129, 0.16)",
        "badge_ok_txt": "#34d399",
        "badge_low_bg": "rgba(239, 68, 68, 0.18)",
        "badge_low_txt": "#f87171",
        "badge_exp_bg": "rgba(245, 158, 11, 0.18)",
        "badge_exp_txt": "#fbbf24",
        "warn_bg": "#1e1b18",
        "warn_border": "#78350f",
        "warn_txt": "#fde68a",
        "code_bg": "#1e293b",
        "code_txt": "#93c5fd",
        "divider": "#1e293b",
    }
else:
    t = {
        "scheme": "light",
        "bg": "#f8fafc",
        "bg_grad": "radial-gradient(circle at 15% 0%, rgba(37, 99, 235, 0.05) 0%, transparent 45%), radial-gradient(circle at 85% 10%, rgba(124, 58, 237, 0.04) 0%, transparent 45%)",
        "sidebar_bg": "#ffffff",
        "card_bg": "#ffffff",
        "card_hover": "#3b82f6",
        "card_border": "#e2e8f0",
        "card_shadow": "0 1px 3px rgba(15, 23, 42, 0.04), 0 6px 16px rgba(15, 23, 42, 0.03)",
        "text_main": "#0f172a",
        "text_muted": "#64748b",
        "input_bg": "#ffffff",
        "input_border": "#cbd5e1",
        "popover_bg": "#ffffff",
        "tab_bg": "#e2e8f0",
        "tab_text": "#475569",
        "tab_active_bg": "#ffffff",
        "tab_active_text": "#2563eb",
        "sec_btn_bg": "#ffffff",
        "sec_btn_text": "#0f172a",
        "sec_btn_hover_bg": "#eff6ff",
        "sec_btn_hover_txt": "#1d4ed8",
        "sec_btn_border": "#cbd5e1",
        "pill_bg": "#dbeafe",
        "pill_border": "#bfdbfe",
        "pill_text": "#1d4ed8",
        "price_color": "#2563eb",
        "pro_price_color": "#7c3aed",
        "badge_ok_bg": "#dcfce7",
        "badge_ok_txt": "#15803d",
        "badge_low_bg": "#fee2e2",
        "badge_low_txt": "#b91c1c",
        "badge_exp_bg": "#fef3c7",
        "badge_exp_txt": "#b45309",
        "warn_bg": "#fffbeb",
        "warn_border": "#fcd34d",
        "warn_txt": "#92400e",
        "code_bg": "#f1f5f9",
        "code_txt": "#2563eb",
        "divider": "#e2e8f0",
    }

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        color-scheme: {t['scheme']} !important;
    }}

    /* Global Font tanpa menimpa Material Icons bawaan Streamlit */
    html, body, .stApp, button, input, select, textarea, .stMarkdown, .stText, label, p,
    span:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded),
    div:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

    /* Pastikan Ikon Material Streamlit tetap utuh */
    [data-testid="stIconMaterial"], .material-symbols-rounded {{
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-block !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
    }}

    h1, h2, h3, h4 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        color: {t['text_main']} !important;
    }}

    /* Latar Belakang Utama & Teks Global */
    .stApp {{
        background-color: {t['bg']} !important;
        background-image: {t['bg_grad']} !important;
        color: {t['text_main']} !important;
    }}
    .stApp p, .stApp span, .stApp label, .stApp li {{
        color: {t['text_main']};
    }}
    .stCaption, [data-testid="stCaptionContainer"] p {{
        color: {t['text_muted']} !important;
    }}
    code {{
        background-color: {t['code_bg']} !important;
        color: {t['code_txt']} !important;
        border: 1px solid {t['card_border']} !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
        font-weight: 700 !important;
    }}
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    hr {{
        border-color: {t['divider']} !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {t['sidebar_bg']} !important;
        border-right: 1px solid {t['card_border']} !important;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
        color: {t['text_main']};
    }}

    /* Card Containers (border=True) */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {t['card_bg']} !important;
        border: 1px solid {t['card_border']} !important;
        border-radius: 18px !important;
        box-shadow: {t['card_shadow']} !important;
        transition: border-color 0.2s ease, transform 0.2s ease !important;
    }}
    [data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: {t['card_hover']} !important;
    }}

    /* Metric Cards & Delta Badge */
    [data-testid="stMetric"] {{
        background-color: {t['card_bg']} !important;
        border: 1px solid {t['card_border']} !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        box-shadow: {t['card_shadow']} !important;
    }}
    [data-testid="stMetricLabel"] p {{
        font-weight: 600 !important;
        color: {t['text_muted']} !important;
        font-size: 13px !important;
    }}
    [data-testid="stMetricValue"] div {{
        font-weight: 800 !important;
        color: {t['text_main']} !important;
        letter-spacing: -0.02em !important;
    }}
    [data-testid="stMetricDelta"] {{
        background-color: {t['badge_low_bg']} !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
        width: fit-content !important;
    }}
    [data-testid="stMetricDelta"] div, [data-testid="stMetricDelta"] svg {{
        color: {t['badge_low_txt']} !important;
        fill: {t['badge_low_txt']} !important;
        font-weight: 700 !important;
    }}

    /* Tombol Primary */
    .stButton > button[kind="primary"], button[kind="primaryFormSubmit"] {{
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.1rem !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.28) !important;
        transition: all 0.18s ease !important;
    }}
    .stButton > button[kind="primary"] *, button[kind="primaryFormSubmit"] * {{
        color: #ffffff !important;
    }}
    .stButton > button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover {{
        background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%) !important;
        transform: translateY(-1px);
    }}

    /* Tombol Secondary, Download & Popover Trigger (Termasuk tombol Kelola Barang & Harga) */
    .stButton > button[kind="secondary"],
    button[kind="secondaryFormSubmit"],
    .stDownloadButton > button,
    [data-testid="stPopover"] button,
    button[data-testid="baseButton-secondary"] {{
        background-color: {t['sec_btn_bg']} !important;
        color: {t['sec_btn_text']} !important;
        border: 1px solid {t['sec_btn_border']} !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.18s ease !important;
    }}
    .stButton > button[kind="secondary"] *,
    button[kind="secondaryFormSubmit"] *,
    .stDownloadButton > button *,
    [data-testid="stPopover"] button *,
    button[data-testid="baseButton-secondary"] * {{
        color: {t['sec_btn_text']} !important;
    }}
    .stButton > button[kind="secondary"]:hover,
    button[kind="secondaryFormSubmit"]:hover,
    .stDownloadButton > button:hover,
    [data-testid="stPopover"] button:hover {{
        background-color: {t['sec_btn_hover_bg']} !important;
        border-color: #2563eb !important;
        color: {t['sec_btn_hover_txt']} !important;
    }}
    .stButton > button[kind="secondary"]:hover *,
    .stDownloadButton > button:hover *,
    [data-testid="stPopover"] button:hover * {{
        color: {t['sec_btn_hover_txt']} !important;
    }}
    .stButton > button:disabled {{
        opacity: 0.45 !important;
        cursor: not-allowed !important;
    }}

    /* Input Fields, Number Input & Selectbox (Semua lapisan BaseWeb dipaksa putih di Light Mode) */
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stDateInput > div > div,
    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] > div > div {{
        background-color: {t['input_bg']} !important;
        border-color: {t['input_border']} !important;
        border-radius: 12px !important;
        color: {t['text_main']} !important;
    }}
    .stSelectbox [data-baseweb="select"] > div {{
        border: 1px solid {t['input_border']} !important;
    }}
    .stSelectbox [data-baseweb="select"] * {{
        color: {t['text_main']} !important;
        fill: {t['text_main']} !important;
    }}
    .stTextInput input, .stNumberInput input, .stDateInput input {{
        background-color: transparent !important;
        color: {t['text_main']} !important;
        -webkit-text-fill-color: {t['text_main']} !important;
        font-weight: 500 !important;
    }}
    .stTextInput input::placeholder {{
        color: {t['text_muted']} !important;
        -webkit-text-fill-color: {t['text_muted']} !important;
        opacity: 0.85 !important;
    }}
    .stNumberInput button {{
        background-color: {t['input_bg']} !important;
        color: {t['text_main']} !important;
        border-color: {t['input_border']} !important;
    }}

    /* Popover & Dropdown Listbox (Saat selectbox/popover dibuka) */
    [data-testid="stPopoverBody"],
    [data-testid="stPopoverBody"] > div,
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: {t['popover_bg']} !important;
        border: 1px solid {t['card_border']} !important;
        border-radius: 14px !important;
        color: {t['text_main']} !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12) !important;
    }}
    ul[role="listbox"] li,
    ul[role="listbox"] li span,
    ul[role="listbox"] li div {{
        background-color: transparent !important;
        color: {t['text_main']} !important;
    }}
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li[aria-selected="true"] {{
        background-color: {t['pill_bg']} !important;
        color: {t['pill_text']} !important;
    }}

    /* Alert Boxes (st.warning, st.info, st.success) hingga div bagian dalam */
    [data-testid="stAlert"],
    [data-testid="stAlert"] > div {{
        background-color: {t['warn_bg']} !important;
        border-color: {t['warn_border']} !important;
        border-radius: 14px !important;
    }}
    [data-testid="stAlert"] {{
        border: 1px solid {t['warn_border']} !important;
    }}
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span,
    [data-testid="stAlert"] strong,
    [data-testid="stAlert"] div {{
        color: {t['warn_txt']} !important;
    }}

    /* Tabs Modern ala Pill Switcher */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {t['tab_bg']} !important;
        padding: 5px !important;
        border-radius: 14px !important;
        gap: 6px !important;
        border: 1px solid {t['card_border']} !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 8px 16px !important;
        border: none !important;
        background-color: transparent !important;
    }}
    .stTabs [data-baseweb="tab"] p, .stTabs [data-baseweb="tab"] span {{
        color: {t['tab_text']} !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {t['tab_active_bg']} !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
    }}
    .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span {{
        color: {t['tab_active_text']} !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}

    /* Expanders & Chat */
    [data-testid="stExpander"] {{
        background-color: {t['card_bg']} !important;
        border: 1px solid {t['card_border']} !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }}
    [data-testid="stExpander"] details summary {{
        background-color: {t['card_bg']} !important;
        color: {t['text_main']} !important;
        font-weight: 700 !important;
        padding: 10px 14px !important;
    }}
    [data-testid="stExpander"] details summary:hover {{
        background-color: {t['pill_bg']} !important;
    }}
    [data-testid="stChatMessage"] {{
        background-color: {t['input_bg']} !important;
        border: 1px solid {t['card_border']} !important;
        border-radius: 14px !important;
    }}

    /* Badges & Harga */
    .hero-pill {{
        display: inline-block;
        background-color: {t['pill_bg']};
        border: 1px solid {t['pill_border']};
        color: {t['pill_text']} !important;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}
    .gradient-title {{
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }}
    .badge-pro {{
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white !important; padding: 4px 12px; border-radius: 9999px;
        font-size: 11px; font-weight: 800; letter-spacing: 0.03em; display: inline-block;
    }}
    .badge-prm {{
        background: #2563eb; color: white !important; padding: 4px 12px;
        border-radius: 9999px; font-size: 11px; font-weight: 800; display: inline-block;
    }}
    .badge-std {{
        background: #475569; color: white !important; padding: 4px 12px;
        border-radius: 9999px; font-size: 11px; font-weight: 800; display: inline-block;
    }}
    .badge-ok {{ background: {t['badge_ok_bg']}; color: {t['badge_ok_txt']} !important; padding: 3px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; }}
    .badge-low {{ background: {t['badge_low_bg']}; color: {t['badge_low_txt']} !important; padding: 3px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; }}
    .badge-exp {{ background: {t['badge_exp_bg']}; color: {t['badge_exp_txt']} !important; padding: 3px 10px; border-radius: 8px; font-size: 12px; font-weight: 700; }}
    .price-text {{ color: {t['price_color']} !important; font-size: 22px; font-weight: 800; letter-spacing: -0.02em; }}
    .old-price {{ text-decoration: line-through; color: {t['text_muted']} !important; font-size: 13px; font-weight: 600; margin-right: 6px; }}

    /* Simulasi Layar E-Paper Fisik */
    .epaper-light {{
        background-color: #f4f4f0; color: #111111 !important; border: 6px solid #334155;
        border-radius: 14px; padding: 18px; font-family: 'Courier New', monospace !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }}
    .epaper-light * {{ font-family: 'Courier New', monospace !important; color: #111111 !important; }}
    .epaper-dark {{
        background-color: #18181b; color: #f4f4f5 !important; border: 6px solid #ef4444;
        border-radius: 14px; padding: 18px; font-family: 'Courier New', monospace !important;
        box-shadow: 0 8px 20px rgba(239,68,68,0.22);
    }}
    .epaper-dark * {{ font-family: 'Courier New', monospace !important; color: #f4f4f5 !important; }}
</style>
""", unsafe_allow_html=True)
def render_theme_toggle(key_suffix="top"):
    label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
    if st.button(label, key=f"theme_btn_{key_suffix}", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 2. HALAMAN LOGIN DEMO
# ==========================================
if not st.session_state.logged_in:
    _, _, col_t = st.columns([5, 1, 1.1])
    with col_t:
        render_theme_toggle("login")

    _, col_l, _ = st.columns([1, 1.25, 1])
    with col_l:
        st.markdown(f"""
        <div style='text-align: center; margin-top: 12px; margin-bottom: 18px;'>
            <span class='hero-pill'>🏷️ Smart Label & Retail OS</span>
            <h1 style='font-size: 38px; margin: 4px 0;'>Masuk ke <span class='gradient-title'>Storify</span></h1>
            <p style='color: {t['text_muted']}; font-size: 15px;'>Sistem Manajemen Smart Label E-Paper & Operasional Toko</p>
        </div>
        """, unsafe_allow_html=True)
        with st.container(border=True):
            email_in = st.text_input("Email Perusahaan", "beatrix@storify.id")
            pass_in = st.text_input("Password", type="password", value="demo123")
            st.write("")
            if st.button("Masuk ke Dashboard", type="primary", use_container_width=True):
                if email_in.strip() and pass_in.strip():
                    st.session_state.logged_in = True
                    st.session_state.accounts[0]["email"] = email_in.strip()
                    st.rerun()
                else:
                    st.error("Email dan password wajib diisi.")
    st.stop()

# ==========================================
# 3. HALAMAN AKTIVASI LISENSI PAKET
# ==========================================
if st.session_state.app_tier is None:
    _, _, col_t2 = st.columns([5, 1, 1.1])
    with col_t2:
        render_theme_toggle("license")

    st.markdown(f"""
    <div style='text-align: center; padding-top: 4px; margin-bottom: 24px;'>
        <span class='hero-pill'>🎟️ Portal Aktivasi Lisensi</span>
        <h1 style='font-size: 36px; margin: 4px 0;'>Aktivasi Paket <span class='gradient-title'>Storify</span></h1>
        <p style='color: {t['text_muted']}; font-size: 15px; max-width: 650px; margin: 0 auto;'>
            Semua paket bebas batasan jumlah rak & akun tim. Masukkan kode lisensi dari invoice pembelian Anda (min. 4 karakter).
        </p>
    </div>
    """, unsafe_allow_html=True)

    tiers_info = [
        (
            "Standard", "Operasional Toko Lengkap", "Rp 156.250", "/ bulan",
            "✔️ **Unlimited Rak & Unlimited Akun Tim**\n"
            "✔️ Update Harga & Stok Smart Label\n"
            "✔️ Kasir Cepat (-1 Terjual) & Export CSV\n"
            "✔️ Stock Opname / Cek Fisik Harian\n"
            "✔️ Notifikasi Restock & Chat Tim\n"
            "✔️ Simulasi Layar Fisik E-Paper",
            "secondary"
        ),
        (
            "Premium", "Otomasi Promo & Profit", "Rp 287.500", "/ bulan",
            "✔️ **Semua Fitur Standard**\n"
            "✔️ **Kalkulator Harga & Margin Profit**\n"
            "✔️ **Bulk Edit Harga & Stok Massal**\n"
            "✔️ **Flash Sale Otomatis & Diskon Coret**\n"
            "✔️ **Tracker Kedaluwarsa (Expired Alert)**\n"
            "✔️ **Cetak Daftar Harga & Grafik Stok**",
            "secondary"
        ),
        (
            "Pro", "Prioritas & Multi-Cabang", "Rp 437.500", "/ bulan",
            "✔️ **Semua Fitur Premium**\n"
            "✔️ **Manajemen Multi-Cabang & Transfer Stok**\n"
            "✔️ **Ringkasan Perbandingan Semua Cabang**\n"
            "✔️ **Kustomisasi Tema Layar E-Paper**\n"
            "✔️ **LED Locator (Tes Kedip Label Rak)**\n"
            "✔️ **Buku Handover Shift & Priority Sync**",
            "primary"
        )
    ]

    cols = st.columns(3, gap="large")
    for idx, (name, sub, price_lbl, cycle_lbl, desc, btn_type) in enumerate(tiers_info):
        with cols[idx]:
            with st.container(border=True):
                if name == "Pro":
                    st.markdown("<span class='badge-pro'>⭐ PRIORITAS ENTERPRISE</span>", unsafe_allow_html=True)
                elif name == "Premium":
                    st.markdown("<span class='badge-prm'>POPULER</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='badge-std'>DASAR</span>", unsafe_allow_html=True)

                price_color = t["pro_price_color"] if name == "Pro" else t["price_color"]
                st.markdown(f"""
                <h3 style='margin: 12px 0 2px 0; font-size: 22px; color: {t['text_main']};'>{name}</h3>
                <p style='color: {t['text_muted']}; font-size: 13px; margin-bottom: 14px;'>{sub}</p>
                <div style='margin-bottom: 8px;'>
                    <span style='font-size: 28px; font-weight: 800; color: {price_color};'>{price_lbl}</span>
                    <span style='font-size: 13px; color: {t['text_muted']}; font-weight: 600;'> {cycle_lbl}</span>
                </div>
                """, unsafe_allow_html=True)
                st.divider()
                st.markdown(desc)
                st.write("")
                code_in = st.text_input(f"Kode Lisensi {name}", placeholder=f"Contoh: STR-{name[:3].upper()}-8492", key=f"code_{name}")
                if st.button(f"Aktifkan {name}", type=btn_type, use_container_width=True, key=f"act_{name}"):
                    clean_code = code_in.strip()
                    if len(clean_code) >= 4:
                        st.session_state.app_tier = name
                        add_log("SUCCESS", f"Lisensi {name} diaktifkan (Kode: {clean_code})")
                        st.rerun()
                    else:
                        st.warning("Masukkan kode lisensi yang valid (minimal 4 karakter).")
    st.stop()

# ==========================================
# 4. AUTO-RESTORE FLASH SALE & DATA CABANG
# ==========================================
if tier != "Pro":
    st.session_state.active_branch = "Cabang Utama"

branch = st.session_state.active_branch
current_inv = st.session_state.inventory.setdefault(branch, {})

if st.session_state.flash_sale_active and time.time() > st.session_state.flash_sale_end:
    for r, orig_p in st.session_state.original_prices.items():
        if r in current_inv:
            current_inv[r]["price"] = orig_p
            current_inv[r]["old_price"] = None
    st.session_state.flash_sale_active = False
    st.session_state.original_prices = {}
    add_log("INFO", "Flash Sale selesai. Harga E-Paper kembali normal.")

active_notifs = [req for req in st.session_state.restock_requests if req["status"] == "Belum" and req.get("branch", "Cabang Utama") == branch]
history_reqs = [req for req in st.session_state.restock_requests if req["status"] == "Sudah" and req.get("branch", "Cabang Utama") == branch]

# HEADER UTAMA
c_head1, c_head_theme, c_head_sync = st.columns([2.6, 0.85, 1.25], vertical_alignment="center")
with c_head1:
    st.markdown(f"<h1 style='margin-bottom: 2px;'>🏷️ <span class='gradient-title'>Storify</span> — {branch}</h1>", unsafe_allow_html=True)
    tier_tag = "⭐ PRIORITAS PRO" if tier == "Pro" else f"PAKET {tier.upper()}"
    st.caption(f"Lisensi: **{tier_tag}** (Unlimited Rak & Akun) | Login: **{current_user['name']}** (`{current_user['role']}`) | 📅 {datetime.now().strftime('%d %b %Y')}")
with c_head_theme:
    render_theme_toggle("main_header")
with c_head_sync:
    sync_label = "⚡ Priority Sync E-Paper" if tier == "Pro" else "📡 Sync Semua E-Paper"
    if st.button(sync_label, type="primary", use_container_width=True):
        with st.spinner("Mengirim pembaruan ke Smart Label..."):
            time.sleep(0.15 if tier == "Pro" else 0.5)
        add_log("SUCCESS", f"[{current_user['name']}] Sinkronisasi {len(current_inv)} Smart Label di {branch} selesai.")
        st.toast(f"Semua label di {branch} berhasil diperbarui!", icon="✅")
if is_privileged and active_notifs:
    st.warning(f"🔔 **Notifikasi Masuk ({branch}):** Ada **{len(active_notifs)} permintaan restock** berstatus **Belum**. Buka tab **📩 Notifikasi & Chat** untuk menandai **Sudah**.", icon="📢")

# ==========================================
# 5. SIDEBAR KONTROL RINGKAS
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='margin-bottom: 10px;'>⚙️ Panel Kontrol</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"**👤 {current_user['name']}** (`{current_user['role']}`)")
        st.caption(f"📍 Lokasi: **{branch}**")
        render_theme_toggle("sidebar")

    # Fitur Khusus PRO: Multi-Cabang & Transfer Stok
    if tier == "Pro":
        with st.expander("🏢 Cabang & Transfer Stok (Pro)", expanded=True):
            sel_br = st.selectbox("Cabang Aktif:", st.session_state.branches, index=st.session_state.branches.index(branch))
            if sel_br != branch:
                st.session_state.active_branch = sel_br
                st.session_state.page = "home"
                st.rerun()
            if is_privileged:
                new_br = st.text_input("Nama Cabang Baru", placeholder="Contoh: Cabang Timur")
                if st.button("Tambah Cabang", use_container_width=True):
                    if new_br.strip() and new_br.strip() not in st.session_state.branches:
                        st.session_state.branches.append(new_br.strip())
                        st.session_state.inventory[new_br.strip()] = {}
                        st.session_state.active_branch = new_br.strip()
                        add_log("SUCCESS", f"Cabang baru ditambahkan: {new_br.strip()}")
                        st.rerun()

                if len(st.session_state.branches) > 1 and current_inv:
                    st.divider()
                    st.caption("**🚚 Transfer Stok ke Cabang Lain**")
                    tr_rak = st.selectbox("Produk Asal:", list(current_inv.keys()), format_func=lambda r: f"{r} - {current_inv[r]['item']} ({current_inv[r]['qty']})")
                    other_branches = [b for b in st.session_state.branches if b != branch]
                    tr_dest = st.selectbox("Cabang Tujuan:", other_branches)
                    avail_qty = current_inv[tr_rak]["qty"]
                    if avail_qty > 0:
                        tr_qty = st.number_input("Jumlah Transfer", min_value=1, max_value=avail_qty, value=1)
                        if st.button("Kirim Stok Antar Cabang", use_container_width=True):
                            current_inv[tr_rak]["qty"] -= tr_qty
                            current_inv[tr_rak]["outflow"].append(tr_qty)
                            dest_inv = st.session_state.inventory.setdefault(tr_dest, {})
                            if tr_rak in dest_inv:
                                dest_inv[tr_rak]["qty"] += tr_qty
                                dest_inv[tr_rak]["inflow"].append(tr_qty)
                            else:
                                dest_inv[tr_rak] = current_inv[tr_rak].copy()
                                dest_inv[tr_rak]["qty"] = tr_qty
                                dest_inv[tr_rak]["inflow"] = [tr_qty]
                                dest_inv[tr_rak]["outflow"] = [0]
                            add_log("INFO", f"[{current_user['name']}] Transfer {tr_qty} pcs {current_inv[tr_rak]['item']} ({branch} -> {tr_dest})")
                            st.toast("Transfer stok berhasil!", icon="🚚")
                            st.rerun()
                    else:
                        st.caption("⚠️ Stok produk asal kosong (0 pcs).")

    with st.expander("🔄 Ganti Akun Login"):
        acc_labels = [f"{a['name']} ({a['role']})" for a in st.session_state.accounts]
        sel_idx = st.selectbox("Pilih Akun:", range(len(acc_labels)), index=st.session_state.current_user_idx, format_func=lambda x: acc_labels[x])
        if st.button("Masuk Sebagai Akun Ini", use_container_width=True):
            st.session_state.current_user_idx = sel_idx
            st.rerun()

    if is_privileged:
        with st.expander("➕ Tambah Produk & Label"):
            new_rak = st.text_input("Kode Rak", f"Rak E{len(current_inv)+1}")
            new_item = st.text_input("Nama Produk", "Susu UHT 250ml")
            existing_cats = sorted(list(set(d["category"] for d in current_inv.values()))) if current_inv else ["Minuman", "Makanan"]
            cat_choice = st.selectbox("Kategori", existing_cats + ["+ Kategori Baru"])
            new_cat = st.text_input("Nama Kategori Baru", "Produk Susu") if cat_choice == "+ Kategori Baru" else cat_choice

            img_opt = st.radio("Foto Produk:", ["Link URL", "Upload File"], horizontal=True)
            final_img = "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300"
            if img_opt == "Upload File":
                up_file = st.file_uploader("Pilih Gambar", type=["png", "jpg", "jpeg"])
                if up_file:
                    b64 = base64.b64encode(up_file.getvalue()).decode("utf-8")
                    final_img = f"data:image/jpeg;base64,{b64}"
            else:
                url_in = st.text_input("URL Gambar", final_img)
                if url_in:
                    final_img = url_in

            new_qty = st.number_input("Stok Awal", min_value=0, value=15)
            new_cost = st.number_input("Harga Modal / HPP (Rp)", min_value=0, value=5500, step=500)
            new_price = st.number_input("Harga Jual E-Paper (Rp)", min_value=0, value=7500, step=500)
            if tier in ["Premium", "Pro"] and new_price > 0:
                margin_rp = new_price - new_cost
                margin_pct = (margin_rp / new_price) * 100
                st.caption(f"💰 Estimasi Margin: **Rp {margin_rp:,}** ({margin_pct:.1f}%)")
            new_exp = st.date_input("Tanggal Kedaluwarsa", value=date.today() + timedelta(days=60))

            if st.button("Simpan & Pasang Label", type="primary", use_container_width=True):
                if new_rak.strip() and new_item.strip():
                    current_inv[new_rak.strip()] = {
                        "item": new_item.strip(), "category": new_cat.strip(), "qty": new_qty,
                        "cost": new_cost, "price": new_price, "old_price": None,
                        "exp_date": new_exp.strftime("%Y-%m-%d"), "battery": 100, "checked_today": True,
                        "image": final_img, "inflow": [new_qty], "outflow": [0]
                    }
                    add_log("SUCCESS", f"[{current_user['name']}] Menambah {new_item} di {new_rak} ({branch})")
                    st.rerun()

        if tier in ["Premium", "Pro"]:
            with st.expander("⚡ Flash Sale Massal"):
                disc = st.slider("Diskon (%)", 5, 70, 15, 5)
                dur = st.selectbox("Durasi", [15, 30, 60, 120], format_func=lambda x: f"{x} Detik")
                if not st.session_state.flash_sale_active:
                    if st.button("Mulai Flash Sale", type="primary", use_container_width=True):
                        st.session_state.original_prices = {r: d["price"] for r, d in current_inv.items()}
                        for r in current_inv:
                            current_inv[r]["old_price"] = current_inv[r]["price"]
                            current_inv[r]["price"] = int(current_inv[r]["price"] * (1 - disc / 100))
                        st.session_state.flash_sale_active = True
                        st.session_state.flash_sale_end = time.time() + dur
                        add_log("WARNING", f"Flash Sale {disc}% aktif di {branch} selama {dur} detik!")
                        st.rerun()
                else:
                    st.warning(f"Sisa Waktu: {max(0, int(st.session_state.flash_sale_end - time.time()))} detik")
                    if st.button("Hentikan Flash Sale", use_container_width=True):
                        for r, op in st.session_state.original_prices.items():
                            if r in current_inv:
                                current_inv[r]["price"] = op
                                current_inv[r]["old_price"] = None
                        st.session_state.flash_sale_active = False
                        st.session_state.original_prices = {}
                        st.rerun()

        if tier == "Pro":
            with st.expander("🎨 Kustomisasi Layar E-Paper (Pro)"):
                st.session_state.epaper_style = st.selectbox("Tema Layar Label", ["Klasik Terang", "Mode Gelap Merah (Promo)"])
                st.session_state.epaper_footer = st.text_input("Teks Bawah Label", st.session_state.epaper_footer)

    with st.expander("🔐 Sesi & Lisensi"):
        if st.button("🔄 Ganti Paket Lisensi", use_container_width=True):
            st.session_state.app_tier = None
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.app_tier = None
            st.rerun()

# ==========================================
# 6. HALAMAN DETAIL PRODUK & PREVIEW E-PAPER
# ==========================================
if st.session_state.page == "detail":
    rak_key = st.session_state.selected_rak
    if rak_key not in current_inv:
        st.session_state.page = "home"
        st.rerun()
    prod = current_inv[rak_key]

    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page = "home"
        st.rerun()

    c_det1, c_det2 = st.columns([1.4, 1])
    with c_det1:
        with st.container(border=True):
            ic1, ic2 = st.columns([1, 2])
            with ic1:
                st.image(prod["image"], use_container_width=True)
            with ic2:
                st.subheader(f"{prod['item']} ({rak_key})")
                st.write(f"📂 **Kategori:** {prod['category']} | 📅 **Exp:** {prod.get('exp_date', '-')}")
                st.write(f"📦 **Stok Fisik:** {prod['qty']} Pcs | 🔋 **Baterai:** {prod.get('battery', 95)}%")
                st.write(f"🏷️ **Harga Jual:** Rp {prod['price']:,}")
                if tier in ["Premium", "Pro"] and is_privileged:
                    cost_val = prod.get("cost", 0)
                    profit_val = prod["price"] - cost_val
                    st.write(f"💰 **Modal:** Rp {cost_val:,} | **Profit:** Rp {profit_val:,}/pcs")
                if tier == "Pro":
                    if st.button("🔦 Tes Kedip LED Label Rak", use_container_width=True):
                        st.toast(f"Lampu LED pada perangkat {rak_key} berkedip hijau selama 10 detik!", icon="💡")

    with c_det2:
        st.caption("📟 **Simulasi Layar Fisik Smart Label (E-Ink):**")
        promo_tag = "🔥 PROMO" if prod.get("old_price") else "HARGA NORMAL"
        old_p_html = f"<div style='font-size:14px; text-decoration:line-through;'>Rp {prod['old_price']:,}</div>" if prod.get("old_price") else ""
        box_cls = "epaper-dark" if (tier == "Pro" and st.session_state.epaper_style == "Mode Gelap Merah (Promo)") else "epaper-light"
        footer_txt = st.session_state.epaper_footer if tier == "Pro" else f"ID-{rak_key.replace(' ', '')}-2026"
        st.markdown(f"""
        <div class="{box_cls}">
            <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:bold; border-bottom:2px solid currentColor; padding-bottom:4px;">
                <span>{rak_key.upper()}</span>
                <span>{promo_tag}</span>
            </div>
            <div style="font-size:16px; font-weight:bold; margin-top:8px;">{prod['item']}</div>
            {old_p_html}
            <div style="font-size:30px; font-weight:900; margin:4px 0;">Rp {prod['price']:,}</div>
            <div style="font-size:11px; border-top:1px dashed currentColor; padding-top:4px;">
                |||| || ||| |||| ||| &nbsp; {footer_txt}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    if tier in ["Premium", "Pro"]:
        st.subheader("📈 Pergerakan Stok (Masuk vs Terjual)")
        max_len = max(len(prod["inflow"]), len(prod["outflow"]))
        in_padded = prod["inflow"] + [0] * (max_len - len(prod["inflow"]))
        out_padded = prod["outflow"] + [0] * (max_len - len(prod["outflow"]))
        st.line_chart({"Masuk": in_padded, "Terjual": out_padded})
    else:
        st.info("🔒 Upgrade ke paket Premium/Pro untuk melihat grafik riwayat stok.")
    st.stop()

# ==========================================
# 7. SISTEM TAB UTAMA DASHBOARD
# ==========================================
notif_badge = f" ({len(active_notifs)})" if active_notifs else ""
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Monitoring Rak & Label",
    f"📩 Notifikasi & Chat{notif_badge}",
    "📊 History & Pencatatan",
    "👥 Manajemen Akun Tim"
])

# ------------------------------------------
# TAB 1: MONITORING RAK & PRODUK
# ------------------------------------------
with tab1:
    inv_list = list(current_inv.values())
    low_raks = [k for k, v in current_inv.items() if v["qty"] <= 5]
    checked_count = sum(1 for v in inv_list if v.get("checked_today", False))

    near_exp_raks = []
    for k, v in current_inv.items():
        if v.get("exp_date"):
            try:
                exp_dt = datetime.strptime(v["exp_date"], "%Y-%m-%d").date()
                if (exp_dt - date.today()).days <= 7:
                    near_exp_raks.append(k)
            except ValueError:
                pass

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Rak Aktif", f"{len(inv_list)} Rak")
    m2.metric("Total Stok Fisik", f"{sum(d['qty'] for d in inv_list)} Pcs")
    m3.metric("Nilai Aset Barang", f"Rp {sum(d['qty'] * d['price'] for d in inv_list):,}")
    m4.metric("Cek Fisik (Opname)", f"{checked_count} / {len(inv_list)} Rak", delta=f"{len(low_raks)} stok tipis" if low_raks else "Semua aman", delta_color="inverse")

    if tier in ["Premium", "Pro"] and near_exp_raks:
        st.warning(f"📅 **Peringatan Kedaluwarsa (≤7 Hari):** Produk pada **{', '.join(near_exp_raks)}** mendekati tanggal kedaluwarsa. Pertimbangkan memberi diskon cepat.", icon="⏳")

    # Toolbar Filter, Pencarian & Export CSV
    fc1, fc2, fc3, fc4 = st.columns([1.3, 1.3, 1.8, 1])
    with fc1:
        cats = ["Semua Kategori"] + sorted(list(set(d["category"] for d in inv_list)))
        sel_cat = st.selectbox("Kategori", cats, label_visibility="collapsed")
    with fc2:
        status_opts = ["Semua Status", "Stok Menipis (≤5)", "Belum Cek Fisik"]
        if tier in ["Premium", "Pro"]:
            status_opts.append("Dekat Kedaluwarsa")
        sel_status = st.selectbox("Status", status_opts, label_visibility="collapsed")
    with fc3:
        search_q = st.text_input("Cari", placeholder="🔍 Cari nama barang atau kode rak...", label_visibility="collapsed")
    with fc4:
        df_export = pd.DataFrame([
            {"Cabang": branch, "Kode Rak": k, "Produk": v["item"], "Kategori": v["category"], "Stok": v["qty"], "Harga": v["price"], "Exp Date": v.get("exp_date", "-")}
            for k, v in current_inv.items()
        ])
        st.download_button("📥 Export CSV", df_export.to_csv(index=False).encode("utf-8"), f"stok_{branch}.csv", "text/csv", use_container_width=True)

    # Fitur Premium & Pro: Bulk Edit Tabel & Cetak Daftar Harga
    if tier in ["Premium", "Pro"] and current_inv:
        b_tool1, b_tool2 = st.columns(2)
        with b_tool1:
            if is_privileged:
                with st.expander("📝 Edit Harga & Stok Massal (Bulk Edit)"):
                    bulk_df = pd.DataFrame([
                        {"Kode Rak": k, "Produk": v["item"], "Stok": v["qty"], "Harga Modal": v.get("cost", 0), "Harga Jual (Rp)": v["price"]}
                        for k, v in current_inv.items()
                    ])
                    edited_df = st.data_editor(bulk_df, disabled=["Kode Rak", "Produk"], use_container_width=True, hide_index=True, key=f"bulk_{branch}")
                    if st.button("💾 Terapkan Semua Perubahan", type="primary"):
                        for _, row in edited_df.iterrows():
                            rk = row["Kode Rak"]
                            if rk in current_inv:
                                old_q = current_inv[rk]["qty"]
                                new_q_bulk = int(row["Stok"])
                                if new_q_bulk > old_q:
                                    current_inv[rk]["inflow"].append(new_q_bulk - old_q)
                                elif new_q_bulk < old_q:
                                    current_inv[rk]["outflow"].append(old_q - new_q_bulk)
                                current_inv[rk]["qty"] = new_q_bulk
                                current_inv[rk]["cost"] = int(row["Harga Modal"])
                                current_inv[rk]["price"] = int(row["Harga Jual (Rp)"])
                        add_log("SUCCESS", f"[{current_user['name']}] Melakukan Bulk Edit massal di {branch}")
                        st.toast("Semua perubahan harga & stok berhasil disimpan!", icon="✅")
                        st.rerun()
        with b_tool2:
            with st.expander("🖨️ Katalog Daftar Harga Meja Kasir"):
                df_catalog = pd.DataFrame([
                    {"Kode Rak": k, "Nama Produk": v["item"], "Kategori": v["category"], "Harga Resmi": f"Rp {v['price']:,}"}
                    for k, v in current_inv.items()
                ])
                st.dataframe(df_catalog, use_container_width=True, hide_index=True)

    st.write("")

    if not current_inv:
        st.info(f"Belum ada produk terdaftar di **{branch}**. Tambahkan produk melalui menu **➕ Tambah Produk & Label** di sidebar.")
    else:
        for rak_id, data in list(current_inv.items()):
            if sel_cat != "Semua Kategori" and data["category"] != sel_cat:
                continue
            if sel_status == "Stok Menipis (≤5)" and data["qty"] > 5:
                continue
            if sel_status == "Belum Cek Fisik" and data.get("checked_today", False):
                continue
            if sel_status == "Dekat Kedaluwarsa" and rak_id not in near_exp_raks:
                continue
            if search_q.lower() not in data["item"].lower() and search_q.lower() not in rak_id.lower():
                continue

            with st.container(border=True):
                c_img, c_inf, c_stk, c_prc, c_act = st.columns([0.8, 2.1, 1.5, 1.6, 2], vertical_alignment="center")
                with c_img:
                    st.image(data["image"], use_container_width=True)
                with c_inf:
                    st.markdown(f"**📍 {rak_id} — {data['item']}**")
                    bat = data.get("battery", 95)
                    bat_icon = "🪫" if bat < 80 else "🔋"
                    exp_info = f" | 📅 Exp: {data['exp_date']}" if tier in ["Premium", "Pro"] and data.get("exp_date") else ""
                    st.caption(f"📂 {data['category']} | {bat_icon} {bat}%{exp_info}")

                    # Fitur Standard+: Checkbox Cek Fisik Harian (Stock Opname)
                    chk = st.checkbox("Sudah cek fisik hari ini", value=data.get("checked_today", False), key=f"chk_{branch}_{rak_id}")
                    if chk != data.get("checked_today", False):
                        current_inv[rak_id]["checked_today"] = chk
                        add_log("INFO", f"[{current_user['name']}] Cek fisik {rak_id}: {'Sudah' if chk else 'Batal'}")
                        st.rerun()

                with c_stk:
                    st.write(f"📦 **{data['qty']} Pcs**")
                    badges = []
                    if data["qty"] <= 5:
                        badges.append("<span class='badge-low'>⚠️ Stok Tipis</span>")
                    else:
                        badges.append("<span class='badge-ok'>✔ Aman</span>")
                    if tier in ["Premium", "Pro"] and rak_id in near_exp_raks:
                        badges.append("<span class='badge-exp'>⏳ Dekat Exp</span>")
                    st.markdown(" ".join(badges), unsafe_allow_html=True)

                with c_prc:
                    old_html = f"<span class='old-price'>Rp {data['old_price']:,}</span><br>" if data.get("old_price") else ""
                    st.markdown(f"{old_html}<span class='price-text'>Rp {data['price']:,}</span>", unsafe_allow_html=True)
                    if tier in ["Premium", "Pro"] and is_privileged and data.get("cost", 0) > 0:
                        profit = data["price"] - data["cost"]
                        st.caption(f"Margin: Rp {profit:,}")

                with c_act:
                    b_c1, b_c2 = st.columns(2)
                    with b_c1:
                        if st.button("📊 Detail", key=f"det_{branch}_{rak_id}", use_container_width=True):
                            st.session_state.selected_rak = rak_id
                            st.session_state.page = "detail"
                            st.rerun()
                    with b_c2:
                        if st.button("🛒 -1 Terjual", key=f"sell_{branch}_{rak_id}", use_container_width=True, disabled=(data["qty"] == 0)):
                            current_inv[rak_id]["qty"] -= 1
                            current_inv[rak_id]["outflow"].append(1)
                            st.session_state.sales_history.insert(0, {
                                "time": get_ts(), "branch": branch, "rak": rak_id, "item": data["item"],
                                "qty": 1, "total": data["price"], "cashier": current_user["name"]
                            })
                            add_log("INFO", f"[{current_user['name']}] Terjual 1 pcs {data['item']} ({rak_id} - {branch})")
                            st.rerun()

                    with st.popover("⚙️ Kelola Barang & Harga", use_container_width=True):
                        new_q = st.number_input("Stok Fisik", min_value=0, value=data["qty"], key=f"q_{branch}_{rak_id}")
                        if is_privileged:
                            new_p = st.number_input("Harga E-Paper (Rp)", min_value=0, value=int(data["price"]), step=500, key=f"p_{branch}_{rak_id}")
                            if tier in ["Premium", "Pro"]:
                                new_c = st.number_input("Harga Modal (Rp)", min_value=0, value=int(data.get("cost", 0)), step=500, key=f"c_{branch}_{rak_id}")
                                st.caption("Diskon Cepat (Coret Harga):")
                                d1, d2, d3, d4 = st.columns(4)
                                for col_d, pct in zip([d1, d2, d3], [10, 20, 50]):
                                    if col_d.button(f"-{pct}%", key=f"d{pct}_{branch}_{rak_id}", use_container_width=True):
                                        base_p = data["old_price"] if data.get("old_price") else data["price"]
                                        current_inv[rak_id]["old_price"] = base_p
                                        current_inv[rak_id]["price"] = int(base_p * (1 - pct/100))
                                        add_log("INFO", f"[{current_user['name']}] Diskon {pct}% pada {rak_id}")
                                        st.rerun()
                                if d4.button("Reset", key=f"rst_{branch}_{rak_id}", use_container_width=True):
                                    if data.get("old_price"):
                                        current_inv[rak_id]["price"] = data["old_price"]
                                        current_inv[rak_id]["old_price"] = None
                                        st.session_state.original_prices.pop(rak_id, None)
                                        st.rerun()
                            else:
                                new_c = data.get("cost", 0)

                            if st.button("💾 Simpan", type="primary", key=f"sv_{branch}_{rak_id}", use_container_width=True):
                                if new_q > data["qty"]:
                                    current_inv[rak_id]["inflow"].append(new_q - data["qty"])
                                elif new_q < data["qty"]:
                                    current_inv[rak_id]["outflow"].append(data["qty"] - new_q)
                                current_inv[rak_id]["qty"] = new_q
                                current_inv[rak_id]["price"] = new_p
                                current_inv[rak_id]["cost"] = new_c
                                add_log("INFO", f"[{current_user['name']}] Update {rak_id}: Stok={new_q}, Harga=Rp {new_p:,}")
                                st.rerun()

                            if st.button("🗑️ Hapus Rak", key=f"del_{branch}_{rak_id}", use_container_width=True):
                                del current_inv[rak_id]
                                st.session_state.original_prices.pop(rak_id, None)
                                add_log("ERROR", f"[{current_user['name']}] Menghapus {rak_id} ({branch})")
                                st.rerun()
                        else:
                            if st.button("💾 Update Stok", type="primary", key=f"sv_{branch}_{rak_id}", use_container_width=True):
                                if new_q > data["qty"]:
                                    current_inv[rak_id]["inflow"].append(new_q - data["qty"])
                                elif new_q < data["qty"]:
                                    current_inv[rak_id]["outflow"].append(data["qty"] - new_q)
                                current_inv[rak_id]["qty"] = new_q
                                add_log("INFO", f"[{current_user['name']}] Update stok {rak_id} -> {new_q} pcs")
                                st.rerun()

# ------------------------------------------
# TAB 2: NOTIFIKASI RESTOCK, CHAT & SHIFT
# ------------------------------------------
with tab2:
    col_req, col_chat = st.columns([1.2, 1])

    with col_req:
        st.subheader(f"🔔 Notifikasi Permintaan Restock ({branch})")

        with st.container(border=True):
            st.markdown("**Kirim Notifikasi Permintaan Barang**")
            rak_options = list(current_inv.keys())
            if rak_options:
                sel_rak_req = st.selectbox("Pilih Rak / Produk:", rak_options, format_func=lambda r: f"{r} - {current_inv[r]['item']} (Sisa: {current_inv[r]['qty']})")
                req_qty = st.number_input("Jumlah Dibutuhkan (Pcs)", min_value=1, value=20, step=5)
                req_note = st.text_input("Catatan", placeholder="Contoh: Stok menipis, mohon dipesan ke supplier")
                if st.button("📨 Kirim Notifikasi", type="primary", use_container_width=True):
                    new_id = max([r["id"] for r in st.session_state.restock_requests], default=0) + 1
                    st.session_state.restock_requests.insert(0, {
                        "id": new_id, "branch": branch, "rak": sel_rak_req, "item": current_inv[sel_rak_req]["item"],
                        "qty": req_qty, "by": current_user["name"], "note": req_note or "-",
                        "status": "Belum", "created_at": get_ts(), "resolved_at": "-", "resolved_by": "-"
                    })
                    add_log("WARNING", f"[{current_user['name']}] Mengirim notifikasi restock {sel_rak_req} ({branch})")
                    st.toast("Notifikasi restock terkirim!", icon="🔔")
                    time.sleep(0.3)
                    st.rerun()
            else:
                st.info("Tambahkan produk terlebih dahulu di cabang ini.")

        st.write(f"**Antrean Notifikasi Masuk ({len(active_notifs)}):**")
        if not active_notifs:
            st.success("✨ Tidak ada notifikasi tertunda. Semua permintaan sudah ditindaklanjuti dan masuk ke tab **History & Pencatatan**.")
        else:
            for req in active_notifs:
                with st.container(border=True):
                    r_c1, r_c2 = st.columns([2.2, 1.2], vertical_alignment="center")
                    with r_c1:
                        st.markdown(f"**📦 {req['rak']} — {req['item']}** (`{req['qty']} Pcs`)")
                        st.caption(f"🕒 **Waktu Kirim:** {req['created_at']} | 👤 **Oleh:** {req['by']}")
                        st.caption(f"📝 **Catatan:** {req['note']}")
                    with r_c2:
                        if is_privileged:
                            if st.button("✅ Sudah", key=f"done_{req['id']}", type="primary", use_container_width=True):
                                req["status"] = "Sudah"
                                req["resolved_at"] = get_ts()
                                req["resolved_by"] = current_user["name"]
                                add_log("SUCCESS", f"[{current_user['name']}] Menyelesaikan notifikasi restock {req['rak']} (Masuk ke History)")
                                st.toast("Dipindahkan ke History & Pencatatan!", icon="✅")
                                time.sleep(0.3)
                                st.rerun()
                        else:
                            st.warning("⏳ Belum")

    with col_chat:
        st.subheader("💬 Kontak Chat Tim (Gudang ↔ Manager)")
        with st.container(border=True, height=340):
            for chat in st.session_state.team_chat:
                is_me = chat["sender"] == current_user["name"]
                align_icon = "🧑‍💼" if chat["role"] != "STAFF" else "👷"
                with st.chat_message("user" if is_me else "assistant", avatar=align_icon):
                    st.markdown(f"**{chat['sender']}** `{chat['role']}` • <span style='font-size:11px; opacity:0.7;'>{chat['time']}</span>", unsafe_allow_html=True)
                    st.write(chat["msg"])

        with st.form("chat_form", clear_on_submit=True):
            c_in1, c_in2 = st.columns([4, 1])
            with c_in1:
                chat_msg = st.text_input("Ketik pesan...", placeholder="Tulis pesan untuk manager atau staf gudang...", label_visibility="collapsed")
            with c_in2:
                sent = st.form_submit_button("Kirim", type="primary", use_container_width=True)
            if sent and chat_msg.strip():
                st.session_state.team_chat.append({
                    "sender": current_user["name"], "role": current_user["role"],
                    "msg": chat_msg.strip(), "time": get_ts()
                })
                st.rerun()

        if tier == "Pro":
            st.divider()
            st.markdown("**📋 Buku Catatan Handover Shift (Pro)**")
            with st.form("shift_form", clear_on_submit=True):
                sc1, sc2 = st.columns([1, 2.5])
                with sc1:
                    sh_type = st.selectbox("Shift", ["Pagi", "Siang", "Malam"], label_visibility="collapsed")
                with sc2:
                    sh_note = st.text_input("Catatan Shift", placeholder="Tulis laporan kondisi toko/rak saat ganti shift...", label_visibility="collapsed")
                if st.form_submit_button("Simpan Catatan Shift", use_container_width=True) and sh_note.strip():
                    st.session_state.shift_notes.insert(0, {
                        "time": get_ts(), "branch": branch, "author": current_user["name"],
                        "shift": sh_type, "note": sh_note.strip()
                    })
                    st.rerun()

# ------------------------------------------
# TAB 3: HISTORY & PENCATATAN OPERASIONAL
# ------------------------------------------
with tab3:
    st.subheader(f"📊 Riwayat & Pencatatan Operasional ({branch})")

    # Fitur Eksklusif PRO: Perbandingan Ringkas Seluruh Cabang
    if tier == "Pro" and len(st.session_state.branches) > 1:
        st.markdown("### 🏢 Ringkasan Seluruh Cabang (Pro)")
        branch_summary = []
        for b_name in st.session_state.branches:
            b_inv = st.session_state.inventory.get(b_name, {})
            b_sales_total = sum(s["total"] for s in st.session_state.sales_history if s.get("branch") == b_name)
            branch_summary.append({
                "Nama Cabang": b_name,
                "Jumlah Rak": len(b_inv),
                "Total Stok Fisik": sum(d["qty"] for d in b_inv.values()),
                "Nilai Aset Barang": f"Rp {sum(d['qty'] * d['price'] for d in b_inv.values()):,}",
                "Total Penjualan Tercatat": f"Rp {b_sales_total:,}"
            })
        st.dataframe(pd.DataFrame(branch_summary), use_container_width=True, hide_index=True)
        st.divider()

    st.markdown("### ✅ Pencatatan Permintaan Restock (Sudah Diproses)")
    if not history_reqs:
        st.info("Belum ada riwayat permintaan restock yang ditandai 'Sudah' di cabang ini.")
    else:
        df_hist_req = pd.DataFrame([
            {
                "Waktu Permintaan": r["created_at"],
                "Waktu Selesai": r["resolved_at"],
                "Kode Rak": r["rak"],
                "Produk": r["item"],
                "Jumlah (Pcs)": r["qty"],
                "Diminta Oleh": r["by"],
                "Diproses Oleh": r["resolved_by"],
                "Catatan": r["note"]
            }
            for r in history_reqs
        ])
        st.dataframe(df_hist_req, use_container_width=True, hide_index=True)
        st.download_button(
            "📥 Download Pencatatan Restock (CSV)",
            df_hist_req.to_csv(index=False).encode("utf-8"),
            f"pencatatan_restock_{branch}.csv",
            "text/csv"
        )

    st.divider()

    col_h_sales, col_h_logs = st.columns(2)
    with col_h_sales:
        st.markdown("### 🛒 Pencatatan Barang Terjual")
        branch_sales = [s for s in st.session_state.sales_history if s.get("branch", "Cabang Utama") == branch]
        if branch_sales:
            df_sales = pd.DataFrame(branch_sales)[["time", "rak", "item", "qty", "total", "cashier"]]
            df_sales.columns = ["Waktu", "Rak", "Produk", "Qty", "Total (Rp)", "Petugas"]
            st.dataframe(df_sales, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada pencatatan penjualan di cabang ini.")

    with col_h_logs:
        if tier == "Pro":
            st.markdown("### 📋 Riwayat Catatan Shift")
            b_shifts = [s for s in st.session_state.shift_notes if s.get("branch", "Cabang Utama") == branch]
            if b_shifts:
                for sh in b_shifts[:5]:
                    with st.container(border=True):
                        st.markdown(f"**Shift {sh['shift']}** — {sh['author']} (`{sh['time']}`)")
                        st.caption(sh["note"])
            else:
                st.info("Belum ada catatan shift.")
        else:
            st.markdown("### 📜 Log Aktivitas & Sinkronisasi Sistem")
            if tier == "Premium" and is_privileged:
                with st.container(border=True, height=280):
                    for l in st.session_state.logs[:25]:
                        st.text(f"{l['time']} [{l['type']}] >> {l['action']}")
            else:
                st.info("🔒 Log aktivitas sistem tersedia pada paket Premium & Pro untuk Owner/Manager.")

    if tier == "Pro" and is_privileged:
        st.divider()
        with st.expander("📜 Log Aktivitas & Sinkronisasi Sistem Lengkap (Pro)", expanded=False):
            for l in st.session_state.logs[:30]:
                st.text(f"{l['time']} [{l['type']}] >> {l['action']}")

# ------------------------------------------
# TAB 4: MANAJEMEN AKUN TIM
# ------------------------------------------
with tab4:
    st.subheader(f"👥 Daftar & Pendaftaran Akun Karyawan ({len(st.session_state.accounts)} Akun Aktif)")
    col_acc_list, col_acc_add = st.columns([1.5, 1])

    with col_acc_list:
        for idx, acc in enumerate(st.session_state.accounts):
            with st.container(border=True):
                ac1, ac2, ac3 = st.columns([2.5, 1, 1], vertical_alignment="center")
                with ac1:
                    st.markdown(f"**{acc['name']}** ({acc['email']})")
                    st.caption(f"Hak Akses: `{acc['role']}`")
                with ac2:
                    if idx == st.session_state.current_user_idx:
                        st.success("Aktif")
                    else:
                        if st.button("Login", key=f"sw_{idx}", use_container_width=True):
                            st.session_state.current_user_idx = idx
                            st.rerun()
                with ac3:
                    if is_privileged and idx != st.session_state.current_user_idx and len(st.session_state.accounts) > 1:
                        if st.button("🗑️ Hapus", key=f"del_acc_{idx}", use_container_width=True):
                            active_acc = st.session_state.accounts[st.session_state.current_user_idx]
                            st.session_state.accounts.pop(idx)
                            st.session_state.current_user_idx = st.session_state.accounts.index(active_acc)
                            st.rerun()

    with col_acc_add:
        with st.container(border=True):
            st.markdown("**➕ Tambah Akun Baru**")
            if is_privileged:
                new_acc_name = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
                new_acc_email = st.text_input("Email", placeholder="budi@storify.id")
                new_acc_role = st.selectbox("Jabatan (Role)", ["STAFF", "MANAGER", "DEVELOPER", "OWNER"])
                if st.button("Daftarkan Akun", type="primary", use_container_width=True):
                    if new_acc_name.strip() and new_acc_email.strip():
                        if any(a["email"].lower() == new_acc_email.strip().lower() for a in st.session_state.accounts):
                            st.warning("Email tersebut sudah terdaftar.")
                        else:
                            st.session_state.accounts.append({
                                "name": new_acc_name.strip(),
                                "role": new_acc_role,
                                "email": new_acc_email.strip()
                            })
                            add_log("SUCCESS", f"[{current_user['name']}] Menambahkan akun baru: {new_acc_name} ({new_acc_role})")
                            st.success(f"Akun {new_acc_name} berhasil dibuat!")
                            time.sleep(0.4)
                            st.rerun()
                    else:
                        st.warning("Nama dan email wajib diisi.")
            else:
                st.info("🔒 Hanya Owner, Manager, atau Developer yang dapat menambahkan akun baru.")
