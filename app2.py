import streamlit as st
import pandas as pd
import altair as alt
import base64
import time
import uuid
from datetime import datetime, date, timedelta

# ==========================================
# 1. KONFIGURASI & INISIALISASI STATE
# ==========================================
st.set_page_config(page_title="Storify - Smart Label & Inventory OS", layout="wide", page_icon="🏷️")

def get_ts():
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def get_ts_sec():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def gen_bid():
    return uuid.uuid4().hex[:8]

def safe_int(val, default=0):
    try:
        return int(val) if val is not None else default
    except (ValueError, TypeError):
        return default

soon_exp = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
mid_exp = (date.today() + timedelta(days=35)).strftime("%Y-%m-%d")
safe_exp = (date.today() + timedelta(days=90)).strftime("%Y-%m-%d")

# Definisi Lengkap Akses Menu (Tab) & Aksi (Permissions)
ALL_MENU_ACCESS = {
    "menu_monitoring": "📦 Menu: Monitoring Rak & Batch",
    "menu_notif_chat": "📩 Menu: Notifikasi Restock & Chat",
    "menu_history": "📊 Menu: History & Laporan",
    "menu_team": "👥 Menu: Manajemen Akun & Jabatan",
}

ALL_ACTION_PERMISSIONS = {
    "act_sell": "🛒 Aksi: Catat Penjualan (-1 Terjual)",
    "act_opname": "☑️ Aksi: Cek Fisik Harian (Opname)",
    "act_manage_batches": "🗂️ Aksi: Tambah / Edit / Hapus Batch Stok",
    "act_manage_products": "📦 Aksi: Tambah & Hapus Produk / Rak",
    "act_manage_prices": "🏷️ Aksi: Ubah Harga E-Paper & Diskon",
    "act_view_margin": "💰 Aksi: Lihat Harga Modal (HPP) & Margin",
    "act_approve_restock": "✅ Aksi: Setujui / Selesaikan Restock",
    "act_manage_branches": "🏢 Aksi: Kelola Multi-Cabang & Transfer",
    "act_manage_roles": "🛡️ Aksi: Kelola Akun & Custom Jabatan",
}

ALL_PERMISSIONS = {**ALL_MENU_ACCESS, **ALL_ACTION_PERMISSIONS}

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
    "roles_config": {
        "OWNER": {
            "level": 10,
            "core": True,
            "desc": "Pemilik bisnis dengan kontrol penuh seluruh cabang, keuangan, dan sistem.",
            "perms": {k: True for k in ALL_PERMISSIONS}
        },
        "MANAGER": {
            "level": 8,
            "core": False,
            "desc": "Kepala operasional toko, pengatur harga, margin, restock, dan tim.",
            "perms": {k: True for k in ALL_PERMISSIONS}
        },
        "DEVELOPER": {
            "level": 5,
            "core": False,
            "desc": "Teknisi sistem & label E-Paper (tanpa akses HPP/margin finansial).",
            "perms": {
                "menu_monitoring": True,
                "menu_notif_chat": True,
                "menu_history": True,
                "menu_team": False,
                "act_sell": True,
                "act_opname": True,
                "act_manage_batches": True,
                "act_manage_products": True,
                "act_manage_prices": True,
                "act_view_margin": False,
                "act_approve_restock": True,
                "act_manage_branches": False,
                "act_manage_roles": False,
            }
        },
        "STAFF": {
            "level": 2,
            "core": False,
            "desc": "Staf gudang & kasir harian (penjualan, opname, dan pengajuan restock).",
            "perms": {
                "menu_monitoring": True,
                "menu_notif_chat": True,
                "menu_history": False,
                "menu_team": False,
                "act_sell": True,
                "act_opname": True,
                "act_manage_batches": False,
                "act_manage_products": False,
                "act_manage_prices": False,
                "act_view_margin": False,
                "act_approve_restock": False,
                "act_manage_branches": False,
                "act_manage_roles": False,
            }
        }
    },
    "accounts": [
        {"name": "Beatrix", "role": "OWNER", "email": "beatrix@storify.id", "password": "owner123"},
        {"name": "Natannael", "role": "DEVELOPER", "email": "natannael@storify.id", "password": "dev123"},
        {"name": "Walden", "role": "DEVELOPER", "email": "walden@storify.id", "password": "dev123"},
        {"name": "Nathalee", "role": "STAFF", "email": "nathalee@storify.id", "password": "staff123"},
    ],
    "current_user_idx": 0,
    "switch_target_idx": None,
    "logs": [{"time": get_ts_sec(), "type": "INFO", "action": "Sistem Storify Inventory & E-Paper Gateway aktif."}],
    "restock_requests": [
        {
            "id": 1, "branch": "Cabang Utama", "rak": "Rak B2", "item": "Keripik Singkong 100g", "qty": 20,
            "by": "Nathalee", "note": "Stok sisa 4 pcs, ramai pembeli.",
            "status": "Belum", "created_at": get_ts(), "resolved_at": "-", "resolved_by": "-"
        }
    ],
    "sales_history": [
        {"time": get_ts(), "branch": "Cabang Utama", "rak": "Rak A1", "item": "Kopi Sachet 25g", "qty": 2, "total": 30000, "profit": 8000, "cashier": "Nathalee"}
    ],
    "team_chat": [
        {"sender": "Nathalee", "role": "STAFF", "msg": "Halo kak, Rak B2 keripik singkong sudah hampir habis ya.", "time": get_ts()},
        {"sender": "Beatrix", "role": "OWNER", "msg": "Oke siap, silakan tambahkan batch baru di detail produknya.", "time": get_ts()}
    ],
    "inventory": {
        "Cabang Utama": {
            "Rak A1": {
                "item": "Kopi Sachet 25g", "category": "Minuman", "qty": 20, "cost": 11000, "price": 15000, "old_price": None,
                "batches": [
                    {"id": "b_a1_1", "qty": 8, "exp": mid_exp, "note": "Batch Awal"},
                    {"id": "b_a1_2", "qty": 12, "exp": safe_exp, "note": "Restock Supplier"}
                ],
                "battery": 98, "checked_today": True,
                "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300",
                "inflow": [10, 15, 20], "outflow": [5, 12, 18]
            },
            "Rak B2": {
                "item": "Keripik Singkong 100g", "category": "Makanan", "qty": 4, "cost": 8500, "price": 12000, "old_price": None,
                "batches": [
                    {"id": "b_b2_1", "qty": 4, "exp": soon_exp, "note": "Batch Lama"}
                ],
                "battery": 85, "checked_today": False,
                "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300",
                "inflow": [5, 8, 10], "outflow": [4, 7, 14]
            },
            "Rak C3": {
                "item": "Air Mineral 600ml", "category": "Minuman", "qty": 15, "cost": 3000, "price": 5000, "old_price": None,
                "batches": [
                    {"id": "b_c3_1", "qty": 15, "exp": safe_exp, "note": "Stok Gudang"}
                ],
                "battery": 92, "checked_today": True,
                "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300",
                "inflow": [15, 25, 30], "outflow": [10, 20, 25]
            },
            "Rak D4": {
                "item": "Deterjen Bubuk 800g", "category": "Rumah Tangga", "qty": 8, "cost": 19000, "price": 25000, "old_price": None,
                "batches": [
                    {"id": "b_d4_1", "qty": 3, "exp": mid_exp, "note": "Batch 1"},
                    {"id": "b_d4_2", "qty": 5, "exp": safe_exp, "note": "Batch 2"}
                ],
                "battery": 74, "checked_today": False,
                "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300",
                "inflow": [6, 9, 12], "outflow": [3, 7, 10]
            },
        },
        "Cabang Karawang Barat": {
            "Rak A1": {
                "item": "Teh Botol 350ml", "category": "Minuman", "qty": 24, "cost": 3200, "price": 4500, "old_price": None,
                "batches": [{"id": "b_kb_1", "qty": 24, "exp": safe_exp, "note": "Stok Utama"}],
                "battery": 96, "checked_today": True,
                "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=300",
                "inflow": [12, 24], "outflow": [6, 10]
            },
            "Rak B1": {
                "item": "Roti Tawar Kupas", "category": "Makanan", "qty": 3, "cost": 10500, "price": 14000, "old_price": None,
                "batches": [{"id": "b_kb_2", "qty": 3, "exp": soon_exp, "note": "Batch Pagi"}],
                "battery": 89, "checked_today": False,
                "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300",
                "inflow": [10, 10], "outflow": [8, 9]
            },
        }
    }
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================
# HELPER MULTI-BATCH, FEFO & CUSTOM ROLE ACCESS
# ==========================================
def get_role_level(role_name):
    return st.session_state.roles_config.get(role_name, {"level": 1})["level"]

def has_perm(role_name, perm_key):
    if role_name == "OWNER":
        return True
    role_obj = st.session_state.roles_config.get(role_name)
    if not role_obj:
        return False
    return bool(role_obj.get("perms", {}).get(perm_key, False))

def needs_password_to_switch(from_role, to_role):
    return get_role_level(to_role) > get_role_level(from_role)

def ensure_batches(prod):
    if "batches" not in prod or not isinstance(prod["batches"], list):
        exp_val = prod.get("exp_date", safe_exp)
        q_init = safe_int(prod.get("qty", 0), 0)
        prod["batches"] = [{"id": gen_bid(), "qty": q_init, "exp": exp_val, "note": "-"}] if q_init > 0 else []

    cleaned = []
    for b in prod["batches"]:
        q = safe_int(b.get("qty", 0), 0)
        if q > 0:
            cleaned.append({
                "id": b.get("id") or gen_bid(),
                "qty": q,
                "exp": str(b.get("exp") or safe_exp),
                "note": str(b.get("note") or "-")
            })
    cleaned.sort(key=lambda x: x["exp"])
    prod["batches"] = cleaned
    prod["qty"] = sum(b["qty"] for b in cleaned)

def add_batch_stock(prod, add_qty, exp_str, note_str="-", merge_same_exp=True):
    ensure_batches(prod)
    qty_int = safe_int(add_qty, 0)
    if qty_int <= 0:
        return
    clean_note = note_str.strip() if note_str and note_str.strip() else "-"
    if merge_same_exp:
        for b in prod["batches"]:
            if b["exp"] == exp_str:
                b["qty"] += qty_int
                if clean_note != "-":
                    b["note"] = clean_note
                break
        else:
            prod["batches"].append({"id": gen_bid(), "qty": qty_int, "exp": exp_str, "note": clean_note})
    else:
        prod["batches"].append({"id": gen_bid(), "qty": qty_int, "exp": exp_str, "note": clean_note})

    prod["batches"].sort(key=lambda x: x["exp"])
    prod["qty"] = sum(b["qty"] for b in prod["batches"])
    prod["inflow"].append(qty_int)

def consume_stock_fefo(prod, reduce_qty):
    ensure_batches(prod)
    rem = min(safe_int(reduce_qty, 0), prod["qty"])
    if rem <= 0:
        return []
    consumed = []
    for b in prod["batches"]:
        if rem <= 0:
            break
        take = min(b["qty"], rem)
        b["qty"] -= take
        rem -= take
        consumed.append({"qty": take, "exp": b["exp"]})
    prod["batches"] = [b for b in prod["batches"] if b["qty"] > 0]
    prod["qty"] = sum(b["qty"] for b in prod["batches"])
    prod["outflow"].append(sum(c["qty"] for c in consumed))
    return consumed

def get_nearest_exp(prod):
    ensure_batches(prod)
    return prod["batches"][0]["exp"] if prod["batches"] else "-"

def get_exp_alert_batches(prod, days_threshold=7):
    ensure_batches(prod)
    alerts = []
    for b in prod["batches"]:
        try:
            exp_dt = datetime.strptime(b["exp"], "%Y-%m-%d").date()
            if (exp_dt - date.today()).days <= days_threshold:
                alerts.append(b)
        except ValueError:
            pass
    return alerts

def add_log(log_type, msg):
    st.session_state.logs.insert(0, {"time": get_ts_sec(), "type": log_type, "action": msg})

if not st.session_state.accounts:
    st.session_state.accounts = defaults["accounts"]
if st.session_state.current_user_idx >= len(st.session_state.accounts) or st.session_state.current_user_idx < 0:
    st.session_state.current_user_idx = 0

current_user = st.session_state.accounts[st.session_state.current_user_idx]
u_role = current_user["role"]

# Evaluasi dinamis seluruh menu & aksi sesuai jabatan aktif
can_menu_monitoring = has_perm(u_role, "menu_monitoring")
can_menu_notif = has_perm(u_role, "menu_notif_chat")
can_menu_history = has_perm(u_role, "menu_history")
can_menu_team = has_perm(u_role, "menu_team")

can_sell = has_perm(u_role, "act_sell")
can_opname = has_perm(u_role, "act_opname")
can_manage_batches = has_perm(u_role, "act_manage_batches")
can_manage_products = has_perm(u_role, "act_manage_products")
can_manage_prices = has_perm(u_role, "act_manage_prices")
can_view_margin = has_perm(u_role, "act_view_margin")
can_approve_restock = has_perm(u_role, "act_approve_restock")
can_manage_branches = has_perm(u_role, "act_manage_branches")
can_manage_roles = has_perm(u_role, "act_manage_roles")

tier = st.session_state.app_tier
is_dark = st.session_state.dark_mode

# ==========================================
# GLOBAL THEME & MODERN SAAS DESIGN
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
        "grid_head": "#131c31",
        "grid_row": "#0b1222",
        "grid_hover": "#16223a",
        "grid_line": "#1e293b",
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
        "grid_head": "#f1f5f9",
        "grid_row": "#ffffff",
        "grid_hover": "#f8fafc",
        "grid_line": "#e2e8f0",
    }

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {{
        color-scheme: {t['scheme']} !important;
    }}

    html, body, .stApp, button, input, select, textarea, .stMarkdown, .stText, label, p,
    span:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded),
    div:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}

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

    [data-testid="stSidebar"] {{
        background-color: {t['sidebar_bg']} !important;
        border-right: 1px solid {t['card_border']} !important;
    }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {{
        color: {t['text_main']};
    }}

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

    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {{
        border: 1px solid {t['grid_line']} !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        background-color: {t['grid_row']} !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12) !important;
    }}
    .modern-grid-card {{
        border: 1px solid {t['grid_line']};
        border-radius: 16px;
        overflow: hidden;
        background-color: {t['grid_row']};
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.06);
        margin: 6px 0 16px 0;
    }}
    .modern-grid-scroll {{
        width: 100%;
        overflow-x: auto;
    }}
    .modern-grid {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 13.5px;
    }}
    .modern-grid thead th {{
        background-color: {t['grid_head']};
        color: {t['text_muted']};
        font-weight: 700;
        font-size: 11.5px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 13px 18px;
        text-align: left;
        border-bottom: 1px solid {t['grid_line']};
        white-space: nowrap;
    }}
    .modern-grid tbody tr {{
        background-color: {t['grid_row']};
        transition: background-color 0.15s ease;
    }}
    .modern-grid tbody tr:hover {{
        background-color: {t['grid_hover']};
    }}
    .modern-grid tbody td {{
        padding: 13px 18px;
        color: {t['text_main']};
        border-bottom: 1px solid {t['grid_line']};
        vertical-align: middle;
        line-height: 1.45;
    }}
    .modern-grid tbody tr:last-child td {{
        border-bottom: none;
    }}
    .grid-num {{
        font-variant-numeric: tabular-nums;
        font-weight: 700;
    }}
    .grid-sub {{
        display: block;
        font-size: 11.5px;
        color: {t['text_muted']};
        margin-top: 2px;
    }}

    .batch-prog-bg {{
        width: 100%;
        height: 8px;
        background-color: {t['code_bg']};
        border-radius: 999px;
        overflow: hidden;
        margin-top: 6px;
    }}
    .batch-prog-fill {{
        height: 100%;
        border-radius: 999px;
        transition: width 0.3s ease;
    }}

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
        padding: 8px 14px !important;
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
    .badge-ok {{ background: {t['badge_ok_bg']}; color: {t['badge_ok_txt']} !important; padding: 4px 11px; border-radius: 999px; font-size: 12px; font-weight: 700; display: inline-block; }}
    .badge-low {{ background: {t['badge_low_bg']}; color: {t['badge_low_txt']} !important; padding: 4px 11px; border-radius: 999px; font-size: 12px; font-weight: 700; display: inline-block; }}
    .badge-exp {{ background: {t['badge_exp_bg']}; color: {t['badge_exp_txt']} !important; padding: 4px 11px; border-radius: 999px; font-size: 12px; font-weight: 700; display: inline-block; }}
    .badge-info {{ background: {t['pill_bg']}; color: {t['pill_text']} !important; padding: 4px 11px; border-radius: 999px; font-size: 12px; font-weight: 700; display: inline-block; }}

    .batch-chip {{
        display: inline-block;
        background-color: {t['code_bg']};
        color: {t['text_main']} !important;
        border: 1px solid {t['card_border']};
        padding: 3px 9px;
        border-radius: 8px;
        font-size: 11.5px;
        font-weight: 600;
        margin: 2px 4px 2px 0;
    }}
    .batch-chip-exp {{
        display: inline-block;
        background-color: {t['badge_exp_bg']};
        color: {t['badge_exp_txt']} !important;
        border: 1px solid {t['badge_exp_txt']};
        padding: 3px 9px;
        border-radius: 8px;
        font-size: 11.5px;
        font-weight: 700;
        margin: 2px 4px 2px 0;
    }}
    .price-text {{ color: {t['price_color']} !important; font-size: 22px; font-weight: 800; letter-spacing: -0.02em; }}
    .old-price {{ text-decoration: line-through; color: {t['text_muted']} !important; font-size: 13px; font-weight: 600; margin-right: 6px; }}

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

def render_modern_table(headers, rows_html_list):
    th_html = "".join(f"<th>{h}</th>" for h in headers)
    tr_html = "".join(f"<tr>{r}</tr>" for r in rows_html_list)
    st.markdown(f"""
    <div class="modern-grid-card">
        <div class="modern-grid-scroll">
            <table class="modern-grid">
                <thead><tr>{th_html}</tr></thead>
                <tbody>{tr_html}</tbody>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_theme_toggle(key_suffix="top"):
    label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
    if st.button(label, key=f"theme_btn_{key_suffix}", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ==========================================
# 2. HALAMAN LOGIN DEMO (TERVERIFIKASI)
# ==========================================
if not st.session_state.logged_in:
    _, _, col_t = st.columns([5, 1, 1.1])
    with col_t:
        render_theme_toggle("login")

    _, col_l, _ = st.columns([1, 1.25, 1])
    with col_l:
        st.markdown(f"""
        <div style='text-align: center; margin-top: 12px; margin-bottom: 18px;'>
            <span class='hero-pill'>📦 Smart Label & Inventory OS</span>
            <h1 style='font-size: 38px; margin: 4px 0;'>Masuk ke <span class='gradient-title'>Storify</span></h1>
            <p style='color: {t['text_muted']}; font-size: 15px;'>Sistem Manajemen Smart Label E-Paper & Multi-Batch Inventory</p>
        </div>
        """, unsafe_allow_html=True)
        with st.container(border=True):
            email_in = st.text_input("Email Perusahaan", "beatrix@storify.id")
            pass_in = st.text_input("Password", type="password", value="owner123")
            st.caption("Akun Demo: `beatrix@storify.id` (`owner123`), `natannael@storify.id` (`dev123`), `nathalee@storify.id` (`staff123`)")
            if st.button("Masuk ke Dashboard", type="primary", use_container_width=True):
                matched_idx = None
                for i, acc in enumerate(st.session_state.accounts):
                    if acc["email"].lower() == email_in.strip().lower() and acc["password"] == pass_in:
                        matched_idx = i
                        break
                if matched_idx is not None:
                    st.session_state.current_user_idx = matched_idx
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Email atau password tidak cocok dengan akun terdaftar.")
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
            Kontrol stok akurat hingga ke level Batch & Tanggal Kedaluwarsa. Masukkan kode lisensi paket Anda untuk mengaktifkan sistem (min. 4 karakter).
        </p>
    </div>
    """, unsafe_allow_html=True)

    tiers_info = [
        (
            "Standard", "Kontrol Stok Harian Toko",
            "**✔️ Unlimited Rak & Unlimited Akun Tim**  \n"
            "**✔️ Custom Jabatan & Matriks Menu/Aksi**  \n"
            "**✔️ Update Harga & Stok Smart Label + E-Paper**  \n"
            "**✔️ Kasir Cepat (-1 Terjual) & Export CSV**  \n"
            "**✔️ Stock Opname / Cek Fisik Harian**  \n"
            "**✔️ Kontak Chat Tim (Gudang ↔ Manager)**",
            "secondary"
        ),
        (
            "Premium", "Manajemen Batch, Exp Date & Profit",
            "**✔️ Semua Fitur Standard**  \n"
            "**✔️ Multi-Batch Exp Date (Custom Batch per Produk)**  \n"
            "**✔️ Prioritas Stok Keluar FEFO & Expired Alert ≤7 Hari**  \n"
            "**✔️ Notifikasi Stok Menipis & Rekomendasi Restock**  \n"
            "**✔️ Bulk Edit Harga Massal (Tabel Editor)**  \n"
            "**✔️ Kalkulator Margin Profit (Sesuai Izin Jabatan)**",
            "secondary"
        ),
        (
            "Pro", "Multi-Cabang & Audit Stok Lengkap",
            "**✔️ Semua Fitur Premium (Termasuk Multi-Batch Exp Date)**  \n"
            "**✔️ Manajemen Multi-Cabang & Transfer Stok FEFO**  \n"
            "**✔️ Ringkasan Perbandingan Stok Semua Cabang**  \n"
            "**✔️ Kustomisasi Tema Layar E-Paper**  \n"
            "**✔️ LED Locator (Tes Kedip Label Rak)**  \n"
            "**✔️ Audit Log Mutasi Stok & Priority Sync E-Paper**",
            "primary"
        )
    ]

    cols = st.columns(3, gap="large")
    for idx, (name, sub, desc, btn_type) in enumerate(tiers_info):
        with cols[idx]:
            with st.container(border=True):
                if name == "Pro":
                    st.markdown("<span class='badge-pro'>⭐ PRIORITAS ENTERPRISE</span>", unsafe_allow_html=True)
                elif name == "Premium":
                    st.markdown("<span class='badge-prm'>POPULER</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='badge-std'>DASAR</span>", unsafe_allow_html=True)

                st.markdown(f"""
                <h3 style='margin: 12px 0 2px 0; font-size: 24px; color: {t['text_main']};'>{name}</h3>
                <p style='color: {t['text_muted']}; font-size: 13px; margin-bottom: 8px;'>{sub}</p>
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
# 4. SINKRONISASI DATA CABANG & BATCH
# ==========================================
if tier != "Pro":
    st.session_state.active_branch = "Cabang Utama"

branch = st.session_state.active_branch
current_inv = st.session_state.inventory.setdefault(branch, {})
for prod_item in current_inv.values():
    ensure_batches(prod_item)

active_notifs = [req for req in st.session_state.restock_requests if req["status"] == "Belum" and req.get("branch", "Cabang Utama") == branch]
history_reqs = [req for req in st.session_state.restock_requests if req["status"] == "Sudah" and req.get("branch", "Cabang Utama") == branch]

# HEADER UTAMA
c_head1, c_head_theme, c_head_sync = st.columns([2.6, 0.85, 1.25], vertical_alignment="center")
with c_head1:
    st.markdown(f"<h1 style='margin-bottom: 2px;'>🏷️ <span class='gradient-title'>Storify</span> — {branch}</h1>", unsafe_allow_html=True)
    tier_tag = "⭐ PRIORITAS PRO" if tier == "Pro" else f"PAKET {tier.upper()}"
    u_lvl = get_role_level(u_role)
    st.caption(f"Lisensi: **{tier_tag}** | Login: **{current_user['name']}** (`{u_role}` • Lv.{u_lvl}) | 📅 {datetime.now().strftime('%d %b %Y')}")
with c_head_theme:
    render_theme_toggle("main_header")
with c_head_sync:
    sync_label = "⚡ Priority Sync E-Paper" if tier == "Pro" else "📡 Sync Semua E-Paper"
    if st.button(sync_label, type="primary", use_container_width=True):
        with st.spinner("Mengirim pembaruan ke Smart Label..."):
            time.sleep(0.15 if tier == "Pro" else 0.5)
        add_log("SUCCESS", f"[{current_user['name']}] Sinkronisasi {len(current_inv)} Smart Label di {branch} selesai.")
        st.toast(f"Semua label di {branch} berhasil diperbarui!", icon="✅")

if can_approve_restock and active_notifs:
    st.warning(f"🔔 **Notifikasi Masuk ({branch}):** Ada **{len(active_notifs)} permintaan restock** berstatus **Belum**. Buka menu **📩 Notifikasi & Chat** untuk menandai **Sudah**.", icon="📢")

# ==========================================
# 5. SIDEBAR KONTROL RINGKAS
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='margin-bottom: 10px;'>⚙️ Panel Kontrol</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f"**👤 {current_user['name']}** (`{u_role}` • Lv.{get_role_level(u_role)})")
        role_desc = st.session_state.roles_config.get(u_role, {}).get("desc", "")
        if role_desc:
            st.caption(role_desc)
        st.caption(f"📍 Lokasi: **{branch}**")
        render_theme_toggle("sidebar")

    # Ganti Akun dengan Aturan Password Berjenjang Level Jabatan
    with st.expander("🔄 Ganti Akun Login", expanded=True):
        acc_labels = [f"{a['name']} ({a['role']} • Lv.{get_role_level(a['role'])})" for a in st.session_state.accounts]
        sel_idx = st.selectbox("Pilih Akun Tujuan:", range(len(acc_labels)), index=st.session_state.current_user_idx, format_func=lambda x: acc_labels[x])
        target_acc = st.session_state.accounts[sel_idx]

        if sel_idx == st.session_state.current_user_idx:
            st.caption("✅ Sedang login sebagai akun ini.")
        else:
            req_pass = needs_password_to_switch(u_role, target_acc["role"])
            if req_pass:
                st.caption(f"🔒 Naik ke jabatan `{target_acc['role']}` (Lv.{get_role_level(target_acc['role'])}) wajib password.")
                sw_pass = st.text_input(f"Password {target_acc['name']}", type="password", placeholder="Masukkan password akun...", key="sb_sw_pass")
                if st.button("Verifikasi & Masuk", type="primary", use_container_width=True, key="sb_sw_btn_lock"):
                    if sw_pass == target_acc.get("password", ""):
                        st.session_state.current_user_idx = sel_idx
                        st.session_state.switch_target_idx = None
                        st.session_state.page = "home"
                        add_log("INFO", f"Pergantian akun terverifikasi ke {target_acc['name']} ({target_acc['role']})")
                        st.rerun()
                    else:
                        st.error("Password salah! Akses ditolak.")
            else:
                st.caption(f"🔓 Akses langsung tanpa password (Lv.{get_role_level(u_role)} → Lv.{get_role_level(target_acc['role'])}).")
                if st.button("Masuk Langsung", type="primary", use_container_width=True, key="sb_sw_btn_free"):
                    st.session_state.current_user_idx = sel_idx
                    st.session_state.switch_target_idx = None
                    st.session_state.page = "home"
                    add_log("INFO", f"{current_user['name']} berpindah ke akun {target_acc['name']} ({target_acc['role']})")
                    st.rerun()

    # Fitur Khusus PRO: Multi-Cabang & Transfer Stok (FEFO)
    if tier == "Pro":
        with st.expander("🏢 Cabang & Transfer Stok (Pro)", expanded=False):
            sel_br = st.selectbox("Cabang Aktif:", st.session_state.branches, index=st.session_state.branches.index(branch))
            if sel_br != branch:
                st.session_state.active_branch = sel_br
                st.session_state.page = "home"
                st.rerun()
            if can_manage_branches:
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
                    st.caption("**🚚 Transfer Stok Antar Cabang (FEFO)**")
                    tr_rak = st.selectbox("Produk Asal:", list(current_inv.keys()), format_func=lambda r: f"{r} - {current_inv[r]['item']} ({current_inv[r]['qty']})")
                    other_branches = [b for b in st.session_state.branches if b != branch]
                    tr_dest = st.selectbox("Cabang Tujuan:", other_branches)
                    avail_qty = current_inv[tr_rak]["qty"]
                    if avail_qty > 0:
                        tr_qty = st.number_input("Jumlah Transfer", min_value=1, max_value=avail_qty, value=1)
                        dest_inv = st.session_state.inventory.setdefault(tr_dest, {})
                        src_name_lower = current_inv[tr_rak]["item"].strip().lower()

                        matched_dest_rak = None
                        for dk, dv in dest_inv.items():
                            if dv["item"].strip().lower() == src_name_lower:
                                matched_dest_rak = dk
                                break

                        if matched_dest_rak:
                            target_rak_code = matched_dest_rak
                            st.caption(f"ℹ️ Stok akan digabungkan ke `{target_rak_code}` di {tr_dest}.")
                        elif tr_rak in dest_inv:
                            suffix_num = 2
                            while f"{tr_rak}-{suffix_num}" in dest_inv:
                                suffix_num += 1
                            target_rak_code = f"{tr_rak}-{suffix_num}"
                            st.warning(f"⚠️ Kode `{tr_rak}` di {tr_dest} sudah terpakai produk lain. Akan dibuatkan kode `{target_rak_code}`.")
                        else:
                            target_rak_code = tr_rak

                        if st.button("Kirim Stok Antar Cabang", use_container_width=True):
                            moved_batches = consume_stock_fefo(current_inv[tr_rak], tr_qty)
                            if target_rak_code not in dest_inv:
                                dest_inv[target_rak_code] = {
                                    "item": current_inv[tr_rak]["item"],
                                    "category": current_inv[tr_rak]["category"],
                                    "qty": 0,
                                    "cost": current_inv[tr_rak].get("cost", 0),
                                    "price": current_inv[tr_rak]["price"],
                                    "old_price": None,
                                    "batches": [],
                                    "battery": 100,
                                    "checked_today": False,
                                    "image": current_inv[tr_rak]["image"],
                                    "inflow": [],
                                    "outflow": [0]
                                }
                            for mb in moved_batches:
                                add_batch_stock(dest_inv[target_rak_code], mb["qty"], mb["exp"], note_str=f"Transfer dari {branch}")
                            add_log("INFO", f"[{current_user['name']}] Transfer {tr_qty} pcs {current_inv[tr_rak]['item']} ({branch} -> {tr_dest} [{target_rak_code}])")
                            st.toast("Transfer stok per batch berhasil!", icon="🚚")
                            st.rerun()
                    else:
                        st.caption("⚠️ Stok produk asal kosong (0 pcs).")

    if can_manage_prices and tier == "Pro":
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
# 6. HALAMAN DETAIL BATCH
# ==========================================
if st.session_state.page == "detail":
    rak_key = st.session_state.selected_rak
    if rak_key not in current_inv:
        st.session_state.page = "home"
        st.rerun()
    prod = current_inv[rak_key]
    ensure_batches(prod)

    if st.button("⬅️ Kembali ke Beranda"):
        st.session_state.page = "home"
        st.rerun()

    c_det1, c_det2 = st.columns([1.45, 1])
    with c_det1:
        with st.container(border=True):
            ic1, ic2 = st.columns([1, 2])
            with ic1:
                st.image(prod["image"], use_container_width=True)
            with ic2:
                st.subheader(f"{prod['item']} ({rak_key})")
                st.write(f"📂 **Kategori:** {prod['category']} | 📅 **Exp Terdekat:** `{get_nearest_exp(prod)}`")
                st.write(f"📦 **Total Stok Fisik:** {prod['qty']} Pcs ({len(prod['batches'])} Batch) | 🔋 **Baterai:** {prod.get('battery', 95)}%")
                st.write(f"🏷️ **Harga Jual:** Rp {prod['price']:,}")
                if tier in ["Premium", "Pro"] and can_view_margin:
                    cost_val = prod.get("cost", 0)
                    profit_val = prod["price"] - cost_val
                    st.write(f"💰 **Modal (HPP):** Rp {cost_val:,} | **Margin:** Rp {profit_val:,}/pcs")
                elif tier in ["Premium", "Pro"]:
                    st.caption("🔒 Informasi Modal & Margin terkunci untuk jabatan Anda.")
                if tier == "Pro":
                    if st.button("🔦 Tes Kedip LED Label Rak", use_container_width=True):
                        st.toast(f"Lampu LED pada perangkat {rak_key} berkedip hijau selama 10 detik!", icon="💡")

    with c_det2:
        st.caption("📟 **Simulasi Layar Fisik Smart Label (E-Ink):**")
        promo_tag = "🔥 DISKON" if prod.get("old_price") else "HARGA NORMAL"
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

    col_add_b, col_edit_b = st.columns([1, 1.85], gap="large")
    with col_add_b:
        with st.container(border=True):
            st.subheader("➕ Tambah Batch Baru")
            st.caption(f"Restock stok baru untuk **{prod['item']}**")
            if can_manage_batches:
                with st.form(f"form_add_batch_{branch}_{rak_key}", clear_on_submit=True):
                    new_b_qty = st.number_input("Jumlah Stok Masuk (Pcs)", min_value=1, value=10, step=1)
                    new_b_exp = st.date_input("Tanggal Kedaluwarsa (Exp Date)", value=date.today() + timedelta(days=90))
                    new_b_note = st.text_input("Keterangan Batch", placeholder="Contoh: Supplier A / Batch #2")
                    merge_opt = st.checkbox("Gabungkan jika tanggal exp sama", value=True)
                    if st.form_submit_button("📥 Simpan Batch Baru", type="primary", use_container_width=True):
                        qty_clean = safe_int(new_b_qty, 1)
                        exp_str_b = new_b_exp.strftime("%Y-%m-%d")
                        add_batch_stock(prod, qty_clean, exp_str_b, note_str=new_b_note, merge_same_exp=merge_opt)
                        add_log("SUCCESS", f"[{current_user['name']}] Tambah batch +{qty_clean} pcs untuk {prod['item']} ({rak_key} - {branch}) — Exp: {exp_str_b}")
                        st.toast(f"Batch baru +{qty_clean} pcs ditambahkan!", icon="✅")
                        st.rerun()
            else:
                st.info("🔒 Jabatan Anda tidak memiliki izin menambah atau mengubah batch stok.")

    with col_edit_b:
        with st.container(border=True):
            bh1, bh2 = st.columns([2, 1], vertical_alignment="center")
            with bh1:
                st.subheader(f"🗂️ Daftar Batch Aktif ({len(prod['batches'])} Batch)")
                st.caption("Urutan otomatis berdasarkan **FEFO** (*First Expired, First Out* — paling atas keluar lebih dulu).")
            with bh2:
                st.markdown(f"<div style='text-align:right;'><span class='badge-info'>Total: {prod['qty']} Pcs</span></div>", unsafe_allow_html=True)

            st.write("")

            if not prod["batches"]:
                st.warning("📭 Belum ada batch stok aktif untuk produk ini. Tambahkan batch baru di panel sebelah kiri.")
            else:
                for idx_b, b in enumerate(prod["batches"], start=1):
                    try:
                        exp_obj = datetime.strptime(b["exp"], "%Y-%m-%d").date()
                        d_left = (exp_obj - date.today()).days
                        sisa_pct = max(4, min(100, int((d_left / 90) * 100))) if d_left > 0 else 100
                        if d_left < 0:
                            st_badge = f"<span class='badge-low'>❌ Expired ({abs(d_left)} hr lalu)</span>"
                            bar_color = "#ef4444"
                        elif d_left <= 7:
                            st_badge = f"<span class='badge-exp'>⚠️ Dekat Exp ({d_left} hr lagi)</span>"
                            bar_color = "#f59e0b"
                        elif d_left <= 30:
                            st_badge = f"<span class='badge-info'>⏳ {d_left} hr lagi</span>"
                            bar_color = "#3b82f6"
                        else:
                            st_badge = f"<span class='badge-ok'>✔ Aman ({d_left} hr lagi)</span>"
                            bar_color = "#10b981"
                    except ValueError:
                        exp_obj = date.today() + timedelta(days=30)
                        sisa_pct = 50
                        st_badge = "<span class='badge-info'>-</span>"
                        bar_color = "#3b82f6"

                    prio_tag = "<span class='badge-pro'>#1 PRIORITAS KELUAR (FEFO)</span>" if idx_b == 1 else f"<span class='batch-chip'>Urutan #{idx_b}</span>"

                    with st.container(border=True):
                        bc1, bc2, bc3 = st.columns([1.8, 1.3, 1.1], vertical_alignment="center")
                        with bc1:
                            st.markdown(f"{prio_tag} &nbsp; {st_badge}", unsafe_allow_html=True)
                            st.markdown(f"<div style='font-size:17px; font-weight:800; margin-top:6px;'>📅 Exp: {b['exp']}</div>", unsafe_allow_html=True)
                            st.caption(f"📝 Keterangan: **{b.get('note', '-')}** • ID: `{b['id']}`")
                        with bc2:
                            st.markdown(f"<div style='font-size:20px; font-weight:800; color:{t['price_color']};'>{b['qty']} Pcs</div>", unsafe_allow_html=True)
                            st.caption("Indikator Sisa Masa Simpan:")
                            st.markdown(f"""
                            <div class="batch-prog-bg">
                                <div class="batch-prog-fill" style="width:{sisa_pct}%; background-color:{bar_color};"></div>
                            </div>
                            """, unsafe_allow_html=True)
                        with bc3:
                            if can_manage_batches:
                                with st.popover("✏️ Edit", use_container_width=True):
                                    st.markdown(f"**Edit Batch #{idx_b}**")
                                    ed_q = st.number_input("Jumlah (Pcs)", min_value=1, value=safe_int(b["qty"], 1), step=1, key=f"ed_bq_{b['id']}")
                                    ed_e = st.date_input("Exp Date", value=exp_obj, key=f"ed_be_{b['id']}")
                                    ed_n = st.text_input("Keterangan", value=b.get("note", "-"), key=f"ed_bn_{b['id']}")
                                    if st.button("💾 Simpan", type="primary", key=f"sv_b_{b['id']}", use_container_width=True):
                                        old_q = b["qty"]
                                        new_q_int = safe_int(ed_q, old_q)
                                        b["qty"] = new_q_int
                                        b["exp"] = ed_e.strftime("%Y-%m-%d")
                                        b["note"] = ed_n.strip() or "-"
                                        ensure_batches(prod)
                                        diff = new_q_int - old_q
                                        if diff > 0:
                                            prod["inflow"].append(diff)
                                        elif diff < 0:
                                            prod["outflow"].append(abs(diff))
                                        add_log("INFO", f"[{current_user['name']}] Edit batch {prod['item']} ({rak_key}) -> {new_q_int} pcs, Exp {b['exp']}")
                                        st.toast("Batch diperbarui!", icon="✅")
                                        st.rerun()

                                if st.button("🗑️ Hapus", key=f"del_b_{b['id']}", use_container_width=True):
                                    rem_qty = b["qty"]
                                    prod["batches"] = [x for x in prod["batches"] if x["id"] != b["id"]]
                                    ensure_batches(prod)
                                    prod["outflow"].append(rem_qty)
                                    add_log("WARNING", f"[{current_user['name']}] Menghapus batch {rem_qty} pcs (Exp {b['exp']}) dari {prod['item']}")
                                    st.toast("Batch dihapus!", icon="🗑️")
                                    st.rerun()
                            else:
                                st.caption("🔒 Read-Only")

    st.write("")
    if tier in ["Premium", "Pro"]:
        st.subheader("📈 Pergerakan Stok (Masuk vs Terjual)")
        max_len = max(len(prod["inflow"]), len(prod["outflow"]), 1)
        in_padded = prod["inflow"] + [0] * (max_len - len(prod["inflow"]))
        out_padded = prod["outflow"] + [0] * (max_len - len(prod["outflow"]))

        df_chart = pd.DataFrame({
            "Periode": [f"Ke-{i+1}" for i in range(max_len)] * 2,
            "Urutan": list(range(1, max_len + 1)) * 2,
            "Kategori": ["Stok Masuk"] * max_len + ["Terjual"] * max_len,
            "Jumlah (Pcs)": in_padded + out_padded
        })

        chart_bg = "#ffffff" if not is_dark else "#0f172a"
        chart_text = "#0f172a" if not is_dark else "#f8fafc"
        chart_muted = "#64748b" if not is_dark else "#94a3b8"
        chart_grid = "#e2e8f0" if not is_dark else "#1e293b"
        color_range = ["#059669", "#2563eb"] if not is_dark else ["#34d399", "#60a5fa"]

        line_chart = (
            alt.Chart(df_chart)
            .mark_line(point=alt.OverlayMarkDef(size=85, filled=True), strokeWidth=3)
            .encode(
                x=alt.X("Urutan:O", title="Periode Mutasi", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Jumlah (Pcs):Q", title="Jumlah (Pcs)", scale=alt.Scale(zero=True)),
                color=alt.Color(
                    "Kategori:N",
                    scale=alt.Scale(domain=["Stok Masuk", "Terjual"], range=color_range),
                    legend=alt.Legend(title="Keterangan", orient="top")
                ),
                tooltip=["Periode", "Kategori", "Jumlah (Pcs)"]
            )
            .properties(height=280, background=chart_bg)
            .configure_view(stroke=chart_grid, fill=chart_bg)
            .configure_axis(
                labelColor=chart_muted,
                titleColor=chart_text,
                gridColor=chart_grid,
                domainColor=chart_grid
            )
            .configure_legend(
                labelColor=chart_text,
                titleColor=chart_text
            )
        )

        with st.container(border=True):
            st.altair_chart(line_chart, use_container_width=True)
    else:
        st.info("🔒 Upgrade ke paket Premium/Pro untuk melihat grafik riwayat stok.")
    st.stop()

# ==========================================
# 7. SISTEM TAB DINAMIS SESUAI MENU AKSES JABATAN
# ==========================================
notif_badge = f" ({len(active_notifs)})" if active_notifs else ""

dynamic_tabs_config = []
if can_menu_monitoring:
    dynamic_tabs_config.append(("monitoring", "📦 Monitoring Rak & Batch Stok"))
if can_menu_notif:
    dynamic_tabs_config.append(("notif", f"📩 Notifikasi & Chat{notif_badge}"))
if can_menu_history:
    dynamic_tabs_config.append(("history", "📊 History & Laporan"))
if can_menu_team:
    dynamic_tabs_config.append(("team", "👥 Manajemen Akun & Jabatan"))

if not dynamic_tabs_config:
    st.error("🚫 Jabatan Anda saat ini belum memiliki akses ke menu dashboard mana pun. Hubungi Owner atau Manager.")
    st.stop()

created_tabs = st.tabs([label for _, label in dynamic_tabs_config])
tab_map = {key: tab_obj for (key, _), tab_obj in zip(dynamic_tabs_config, created_tabs)}

# ------------------------------------------
# TAB 1: BERANDA — TAMBAH PRODUK & MONITORING RAK
# ------------------------------------------
if "monitoring" in tab_map:
    with tab_map["monitoring"]:
        inv_list = list(current_inv.values())
        low_raks = [k for k, v in current_inv.items() if v["qty"] <= 5]
        checked_count = sum(1 for v in inv_list if v.get("checked_today", False))
        near_exp_raks = [k for k, v in current_inv.items() if len(get_exp_alert_batches(v, 7)) > 0]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Rak Aktif", f"{len(inv_list)} Rak")
        m2.metric("Total Stok Fisik", f"{sum(d['qty'] for d in inv_list)} Pcs")
        m3.metric("Nilai Aset Barang", f"Rp {sum(d['qty'] * d['price'] for d in inv_list):,}")
        m4.metric("Cek Fisik (Opname)", f"{checked_count} / {len(inv_list)} Rak", delta=f"{len(low_raks)} stok tipis" if low_raks else "Semua aman", delta_color="inverse")

        if tier in ["Premium", "Pro"] and near_exp_raks:
            st.warning(f"📅 **Peringatan Batch Kedaluwarsa (≤7 Hari):** Terdapat batch mendekati kedaluwarsa pada **{', '.join(near_exp_raks)}**. Klik **📊 Detail Batch** untuk mengatur batch.", icon="⏳")

        if can_manage_products:
            with st.expander("➕ Tambah Produk & Label Rak Baru di Beranda", expanded=False):
                with st.form(f"form_add_product_home_{branch}", clear_on_submit=True):
                    p_c1, p_c2, p_c3 = st.columns([1, 1.5, 1.2])
                    with p_c1:
                        new_rak = st.text_input("Kode Rak", value=f"Rak E{len(current_inv)+1}")
                        new_qty = st.number_input("Stok Batch Awal (Pcs)", min_value=1, value=15, step=1)
                    with p_c2:
                        new_item = st.text_input("Nama Produk", placeholder="Contoh: Susu UHT Cokelat 250ml")
                        existing_cats = sorted(list(set(d["category"] for d in current_inv.values()))) if current_inv else ["Minuman", "Makanan", "Rumah Tangga"]
                        cat_choice = st.selectbox("Kategori Produk", existing_cats + ["+ Kategori Baru"])
                    with p_c3:
                        if can_view_margin:
                            new_cost = st.number_input("Harga Modal / HPP (Rp)", min_value=0, value=5500, step=500)
                        else:
                            new_cost = 0
                            st.text_input("Harga Modal / HPP", value="🔒 Terkunci oleh Izin Jabatan", disabled=True)
                        new_price = st.number_input("Harga Jual E-Paper (Rp)", min_value=0, value=7500, step=500)

                    p_c4, p_c5, p_c6 = st.columns([1.2, 1.5, 1.2])
                    with p_c4:
                        new_exp = st.date_input("Exp Date Batch Awal", value=date.today() + timedelta(days=60))
                    with p_c5:
                        new_cat_custom = st.text_input("Jika '+ Kategori Baru', tulis di sini:", placeholder="Contoh: Produk Susu")
                    with p_c6:
                        url_in = st.text_input("URL Gambar Produk", value="https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300")

                    up_file = st.file_uploader("Atau Upload Foto Produk dari Perangkat (Opsional)", type=["png", "jpg", "jpeg"])

                    if st.form_submit_button("💾 Simpan Produk & Pasang Smart Label", type="primary", use_container_width=True):
                        rk_clean = new_rak.strip()
                        it_clean = new_item.strip()
                        if not rk_clean or not it_clean:
                            st.error("Kode Rak dan Nama Produk wajib diisi.")
                        elif rk_clean in current_inv:
                            st.warning(f"Kode Rak **{rk_clean}** sudah terpakai. Gunakan kode rak lain atau kelola produk yang ada.")
                        else:
                            final_cat = new_cat_custom.strip() if (cat_choice == "+ Kategori Baru" and new_cat_custom.strip()) else (cat_choice if cat_choice != "+ Kategori Baru" else "Umum")
                            final_img = url_in.strip() or "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300"
                            if up_file:
                                b64 = base64.b64encode(up_file.getvalue()).decode("utf-8")
                                final_img = f"data:image/jpeg;base64,{b64}"

                            exp_init = new_exp.strftime("%Y-%m-%d")
                            qty_init_int = safe_int(new_qty, 1)
                            cost_init_int = safe_int(new_cost, 0)
                            price_init_int = safe_int(new_price, 0)

                            current_inv[rk_clean] = {
                                "item": it_clean, "category": final_cat, "qty": qty_init_int,
                                "cost": cost_init_int, "price": price_init_int, "old_price": None,
                                "batches": [{"id": gen_bid(), "qty": qty_init_int, "exp": exp_init, "note": "Batch Awal"}],
                                "battery": 100, "checked_today": True,
                                "image": final_img, "inflow": [qty_init_int], "outflow": [0]
                            }
                            add_log("SUCCESS", f"[{current_user['name']}] Menambah produk baru {it_clean} di {rk_clean} ({branch}) — Batch Exp: {exp_init}")
                            st.toast(f"Produk {it_clean} berhasil ditambahkan ke {rk_clean}!", icon="✅")
                            st.rerun()

        fc1, fc2, fc3, fc4 = st.columns([1.3, 1.3, 1.8, 1])
        with fc1:
            cats = ["Semua Kategori"] + sorted(list(set(d["category"] for d in inv_list)))
            sel_cat = st.selectbox("Kategori", cats, label_visibility="collapsed")
        with fc2:
            status_opts = ["Semua Status", "Stok Menipis (≤5)", "Belum Cek Fisik"]
            if tier in ["Premium", "Pro"]:
                status_opts.append("Ada Batch Dekat Exp")
            sel_status = st.selectbox("Status", status_opts, label_visibility="collapsed")
        with fc3:
            search_q = st.text_input("Cari", placeholder="🔍 Cari nama barang atau kode rak...", label_visibility="collapsed")
        with fc4:
            export_rows = []
            for k, v in current_inv.items():
                ensure_batches(v)
                batch_summary = "; ".join([f"{b['qty']} pcs (Exp {b['exp']})" for b in v["batches"]]) if v["batches"] else "-"
                export_rows.append({
                    "Cabang": branch, "Kode Rak": k, "Produk": v["item"], "Kategori": v["category"],
                    "Total Stok": v["qty"], "Harga": v["price"], "Rincian Batch & Exp": batch_summary
                })
            df_export = pd.DataFrame(export_rows)
            st.download_button("📥 Export CSV", df_export.to_csv(index=False).encode("utf-8"), f"stok_{branch}.csv", "text/csv", use_container_width=True)

        if tier in ["Premium", "Pro"] and current_inv:
            b_tool1, b_tool2 = st.columns(2)
            with b_tool1:
                if can_manage_prices:
                    with st.expander("📝 Edit Harga Massal (Bulk Price Editor)"):
                        if can_view_margin:
                            bulk_df = pd.DataFrame([
                                {"Kode Rak": k, "Produk": v["item"], "Total Stok": v["qty"], "Harga Modal": v.get("cost", 0), "Harga Jual": v["price"]}
                                for k, v in current_inv.items()
                            ])
                            col_cfg = {
                                "Harga Modal": st.column_config.NumberColumn("Harga Modal (HPP)", min_value=0, step=500, format="Rp %d"),
                                "Harga Jual": st.column_config.NumberColumn("Harga Jual E-Paper", min_value=0, step=500, format="Rp %d"),
                            }
                        else:
                            bulk_df = pd.DataFrame([
                                {"Kode Rak": k, "Produk": v["item"], "Total Stok": v["qty"], "Harga Jual": v["price"]}
                                for k, v in current_inv.items()
                            ])
                            col_cfg = {
                                "Harga Jual": st.column_config.NumberColumn("Harga Jual E-Paper", min_value=0, step=500, format="Rp %d"),
                            }

                        edited_df = st.data_editor(
                            bulk_df,
                            disabled=["Kode Rak", "Produk", "Total Stok"],
                            use_container_width=True,
                            hide_index=True,
                            column_config=col_cfg,
                            key=f"bulk_{branch}"
                        )
                        if st.button("💾 Terapkan Semua Perubahan Harga", type="primary"):
                            for _, row in edited_df.iterrows():
                                rk = row["Kode Rak"]
                                if rk in current_inv:
                                    if can_view_margin and "Harga Modal" in row and pd.notna(row["Harga Modal"]):
                                        current_inv[rk]["cost"] = safe_int(row["Harga Modal"], current_inv[rk].get("cost", 0))
                                    if pd.notna(row["Harga Jual"]):
                                        current_inv[rk]["price"] = safe_int(row["Harga Jual"], current_inv[rk]["price"])
                            add_log("SUCCESS", f"[{current_user['name']}] Melakukan Bulk Edit harga massal di {branch}")
                            st.toast("Semua perubahan harga berhasil disimpan!", icon="✅")
                            st.rerun()
            with b_tool2:
                with st.expander("🖨️ Katalog Daftar Harga Meja Kasir"):
                    cat_rows = [
                        f"<td><code>{k}</code></td><td><b>{v['item']}</b></td><td><span class='badge-info'>{v['category']}</span></td><td class='grid-num'>Rp {v['price']:,}</td>"
                        for k, v in current_inv.items()
                    ]
                    render_modern_table(["Kode Rak", "Nama Produk", "Kategori", "Harga Resmi"], cat_rows)

        st.write("")

        if not current_inv:
            st.info(f"Belum ada produk terdaftar di **{branch}**.")
        else:
            for rak_id, data in list(current_inv.items()):
                ensure_batches(data)
                if sel_cat != "Semua Kategori" and data["category"] != sel_cat:
                    continue
                if sel_status == "Stok Menipis (≤5)" and data["qty"] > 5:
                    continue
                if sel_status == "Belum Cek Fisik" and data.get("checked_today", False):
                    continue
                if sel_status == "Ada Batch Dekat Exp" and rak_id not in near_exp_raks:
                    continue
                if search_q.lower() not in data["item"].lower() and search_q.lower() not in rak_id.lower():
                    continue

                with st.container(border=True):
                    c_img, c_inf, c_stk, c_prc, c_act = st.columns([0.8, 2.2, 1.5, 1.5, 2], vertical_alignment="center")
                    with c_img:
                        st.image(data["image"], use_container_width=True)
                    with c_inf:
                        st.markdown(f"**📍 {rak_id} — {data['item']}**")
                        bat = data.get("battery", 95)
                        bat_icon = "🪫" if bat < 80 else "🔋"
                        st.caption(f"📂 {data['category']} | {bat_icon} {bat}% | 🗂️ {len(data['batches'])} Batch Aktif")

                        if data["batches"]:
                            chips_html = []
                            for b_item in data["batches"]:
                                try:
                                    d_rem = (datetime.strptime(b_item["exp"], "%Y-%m-%d").date() - date.today()).days
                                    is_soon = d_rem <= 7
                                except ValueError:
                                    is_soon = False
                                cls_chip = "batch-chip-exp" if (tier in ["Premium", "Pro"] and is_soon) else "batch-chip"
                                chips_html.append(f"<span class='{cls_chip}'>📦 {b_item['qty']} pcs • Exp: {b_item['exp']}</span>")
                            st.markdown("".join(chips_html), unsafe_allow_html=True)
                        else:
                            st.caption("⚠️ Semua batch stok habis (0 pcs)")

                        chk = st.checkbox(
                            "Sudah cek fisik hari ini",
                            value=data.get("checked_today", False),
                            disabled=(not can_opname),
                            key=f"chk_{branch}_{rak_id}"
                        )
                        if can_opname and chk != data.get("checked_today", False):
                            current_inv[rak_id]["checked_today"] = chk
                            add_log("INFO", f"[{current_user['name']}] Cek fisik {rak_id} ({branch}): {'Sudah' if chk else 'Batal'}")
                            st.rerun()

                    with c_stk:
                        st.write(f"📦 **Total: {data['qty']} Pcs**")
                        badges = []
                        if data["qty"] <= 5:
                            badges.append("<span class='badge-low'>⚠️ Stok Tipis</span>")
                        else:
                            badges.append("<span class='badge-ok'>✔ Aman</span>")
                        if tier in ["Premium", "Pro"] and rak_id in near_exp_raks:
                            badges.append("<span class='badge-exp'>⏳ Batch Dekat Exp</span>")
                        st.markdown(" ".join(badges), unsafe_allow_html=True)

                    with c_prc:
                        old_html = f"<span class='old-price'>Rp {data['old_price']:,}</span><br>" if data.get("old_price") else ""
                        st.markdown(f"{old_html}<span class='price-text'>Rp {data['price']:,}</span>", unsafe_allow_html=True)
                        if tier in ["Premium", "Pro"] and can_view_margin and data.get("cost", 0) > 0:
                            profit = data["price"] - data["cost"]
                            st.caption(f"💰 Margin: Rp {profit:,}")

                    with c_act:
                        b_c1, b_c2 = st.columns(2)
                        with b_c1:
                            if st.button("📊 Detail Batch", key=f"det_{branch}_{rak_id}", type="primary", use_container_width=True):
                                st.session_state.selected_rak = rak_id
                                st.session_state.page = "detail"
                                st.rerun()
                        with b_c2:
                            if st.button("🛒 -1 Terjual", key=f"sell_{branch}_{rak_id}", use_container_width=True, disabled=(data["qty"] == 0 or not can_sell)):
                                used = consume_stock_fefo(current_inv[rak_id], 1)
                                exp_used = used[0]["exp"] if used else "-"
                                item_profit = data["price"] - data.get("cost", 0)
                                st.session_state.sales_history.insert(0, {
                                    "time": get_ts(), "branch": branch, "rak": rak_id, "item": data["item"],
                                    "qty": 1, "total": data["price"], "profit": item_profit, "cashier": current_user["name"]
                                })
                                add_log("INFO", f"[{current_user['name']}] Terjual 1 pcs {data['item']} ({rak_id} - {branch}, Batch Exp: {exp_used})")
                                st.rerun()

                        if can_manage_prices or can_manage_products:
                            with st.popover("🏷️ Kelola Harga & Rak", use_container_width=True):
                                if can_manage_prices:
                                    new_p = st.number_input("Harga Jual (Rp)", min_value=0, value=safe_int(data["price"], 0), step=500, key=f"p_{branch}_{rak_id}")
                                    if tier in ["Premium", "Pro"] and can_view_margin:
                                        new_c = st.number_input("Harga Modal / HPP (Rp)", min_value=0, value=safe_int(data.get("cost", 0), 0), step=500, key=f"c_{branch}_{rak_id}")
                                    else:
                                        new_c = safe_int(data.get("cost", 0), 0)

                                    if tier in ["Premium", "Pro"]:
                                        st.caption("Diskon Cepat Per Produk:")
                                        d1, d2, d3, d4 = st.columns(4)
                                        for col_d, pct in zip([d1, d2, d3], [10, 20, 50]):
                                            if col_d.button(f"-{pct}%", key=f"d{pct}_{branch}_{rak_id}", use_container_width=True):
                                                base_p = data["old_price"] if data.get("old_price") else data["price"]
                                                current_inv[rak_id]["old_price"] = base_p
                                                current_inv[rak_id]["price"] = int(base_p * (1 - pct/100))
                                                add_log("INFO", f"[{current_user['name']}] Diskon {pct}% pada {rak_id} ({branch})")
                                                st.rerun()
                                        if d4.button("Reset", key=f"rst_{branch}_{rak_id}", use_container_width=True):
                                            if data.get("old_price"):
                                                current_inv[rak_id]["price"] = data["old_price"]
                                                current_inv[rak_id]["old_price"] = None
                                                st.rerun()

                                    if st.button("💾 Simpan Harga", type="primary", key=f"sv_{branch}_{rak_id}", use_container_width=True):
                                        final_p = safe_int(new_p, data["price"])
                                        final_c = safe_int(new_c, data.get("cost", 0))
                                        current_inv[rak_id]["price"] = final_p
                                        current_inv[rak_id]["cost"] = final_c
                                        add_log("INFO", f"[{current_user['name']}] Update harga {rak_id} ({branch}) -> Rp {final_p:,}")
                                        st.rerun()

                                if can_manage_products:
                                    if st.button("🗑️ Hapus Rak", key=f"del_{branch}_{rak_id}", use_container_width=True):
                                        del current_inv[rak_id]
                                        add_log("ERROR", f"[{current_user['name']}] Menghapus {rak_id} ({branch})")
                                        st.rerun()

# ------------------------------------------
# TAB 2: NOTIFIKASI RESTOCK & CHAT TIM
# ------------------------------------------
if "notif" in tab_map:
    with tab_map["notif"]:
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
                            "qty": safe_int(req_qty, 1), "by": current_user["name"], "note": req_note.strip() or "-",
                            "status": "Belum", "created_at": get_ts(), "resolved_at": "-", "resolved_by": "-"
                        })
                        add_log("WARNING", f"[{current_user['name']}] Mengirim notifikasi restock {sel_rak_req} ({branch})")
                        st.toast("Notifikasi restock terkirim!", icon="🔔")
                        time.sleep(0.25)
                        st.rerun()
                else:
                    st.info("Tambahkan produk terlebih dahulu di beranda cabang ini.")

            st.write(f"**Antrean Notifikasi Masuk ({len(active_notifs)}):**")
            if not active_notifs:
                st.success("✨ Tidak ada notifikasi tertunda.")
            else:
                for req in active_notifs:
                    with st.container(border=True):
                        r_c1, r_c2 = st.columns([2.2, 1.2], vertical_alignment="center")
                        with r_c1:
                            st.markdown(f"**📦 {req['rak']} — {req['item']}** (`{req['qty']} Pcs`)")
                            st.caption(f"🕒 **Waktu Kirim:** {req['created_at']} | 👤 **Oleh:** {req['by']}")
                            st.caption(f"📝 **Catatan:** {req['note']}")
                        with r_c2:
                            if can_approve_restock:
                                if st.button("✅ Sudah", key=f"done_{req['id']}", type="primary", use_container_width=True):
                                    req["status"] = "Sudah"
                                    req["resolved_at"] = get_ts()
                                    req["resolved_by"] = current_user["name"]
                                    add_log("SUCCESS", f"[{current_user['name']}] Menyelesaikan notifikasi restock {req['rak']} ({branch})")
                                    st.toast("Restock selesai!", icon="✅")
                                    time.sleep(0.25)
                                    st.rerun()
                            else:
                                st.warning("⏳ Belum")

        with col_chat:
            st.subheader("💬 Kontak Chat Tim (Gudang ↔ Manager)")
            with st.container(border=True, height=380):
                for chat in st.session_state.team_chat:
                    is_me = chat["sender"] == current_user["name"]
                    align_icon = "🧑‍💼" if get_role_level(chat["role"]) >= 5 else "👷"
                    with st.chat_message("user" if is_me else "assistant", avatar=align_icon):
                        st.markdown(f"**{chat['sender']}** `{chat['role']}` • <span style='font-size:11px; opacity:0.7;'>{chat['time']}</span>", unsafe_allow_html=True)
                        st.write(chat["msg"])

            with st.form("chat_form", clear_on_submit=True):
                c_in1, c_in2 = st.columns([4, 1])
                with c_in1:
                    chat_msg = st.text_input("Ketik pesan...", placeholder="Tulis pesan untuk tim...", label_visibility="collapsed")
                with c_in2:
                    sent = st.form_submit_button("Kirim", type="primary", use_container_width=True)
                if sent and chat_msg.strip():
                    st.session_state.team_chat.append({
                        "sender": current_user["name"], "role": u_role,
                        "msg": chat_msg.strip(), "time": get_ts()
                    })
                    st.rerun()

# ------------------------------------------
# TAB 3: HISTORY & LAPORAN OPERASIONAL
# ------------------------------------------
if "history" in tab_map:
    with tab_map["history"]:
        st.subheader(f"📊 Riwayat & Laporan Operasional ({branch})")

        branch_sales = [s for s in st.session_state.sales_history if s.get("branch", "Cabang Utama") == branch]
        total_omzet = sum(s["total"] for s in branch_sales)
        total_profit = sum(s.get("profit", 0) for s in branch_sales)
        total_sold_pcs = sum(s["qty"] for s in branch_sales)

        hm1, hm2, hm3 = st.columns(3)
        hm1.metric("Total Omzet Tercatat", f"Rp {total_omzet:,}")
        if tier in ["Premium", "Pro"] and can_view_margin:
            hm2.metric("Estimasi Profit Kotor", f"Rp {total_profit:,}")
        elif not can_view_margin:
            hm2.metric("Estimasi Profit Kotor", "🔒 Terkunci oleh Izin Jabatan")
        else:
            hm2.metric("Estimasi Profit Kotor", "🔒 Paket Premium/Pro")
        hm3.metric("Total Barang Terjual", f"{total_sold_pcs} Pcs")

        st.divider()

        if tier == "Pro" and len(st.session_state.branches) > 1:
            st.markdown("### 🏢 Ringkasan Seluruh Cabang (Pro)")
            branch_rows = []
            for b_name in st.session_state.branches:
                b_inv = st.session_state.inventory.get(b_name, {})
                b_sales_total = sum(s["total"] for s in st.session_state.sales_history if s.get("branch") == b_name)
                branch_rows.append(
                    f"<td><b>🏢 {b_name}</b></td>"
                    f"<td><span class='badge-info'>{len(b_inv)} Rak</span></td>"
                    f"<td class='grid-num'>{sum(d['qty'] for d in b_inv.values())} Pcs</td>"
                    f"<td class='grid-num'>Rp {sum(d['qty'] * d['price'] for d in b_inv.values()):,}</td>"
                    f"<td class='grid-num' style='color:#10b981;'>Rp {b_sales_total:,}</td>"
                )
            render_modern_table(["Nama Cabang", "Rak Aktif", "Total Stok Fisik", "Nilai Aset Barang", "Total Penjualan"], branch_rows)
            st.divider()

        st.markdown("### ✅ Pencatatan Permintaan Restock (Sudah Diproses)")
        if not history_reqs:
            st.info("Belum ada riwayat permintaan restock yang ditandai 'Sudah' di cabang ini.")
        else:
            hist_rows = []
            for r in history_reqs:
                hist_rows.append(
                    f"<td><code>{r['rak']}</code></td>"
                    f"<td><b>{r['item']}</b><span class='grid-sub'>📝 {r['note']}</span></td>"
                    f"<td class='grid-num'>{r['qty']} Pcs</td>"
                    f"<td><b>{r['by']}</b><span class='grid-sub'>🕒 {r['created_at']}</span></td>"
                    f"<td><b>{r['resolved_by']}</b><span class='grid-sub'>✅ {r['resolved_at']}</span></td>"
                    f"<td><span class='badge-ok'>✔ Selesai</span></td>"
                )
            render_modern_table(["Rak", "Produk & Catatan", "Jumlah", "Permintaan Masuk", "Diproses Oleh", "Status"], hist_rows)

            df_hist_csv = pd.DataFrame([
                {
                    "Waktu Permintaan": r["created_at"], "Waktu Selesai": r["resolved_at"],
                    "Kode Rak": r["rak"], "Produk": r["item"], "Jumlah (Pcs)": r["qty"],
                    "Diminta Oleh": r["by"], "Diproses Oleh": r["resolved_by"], "Catatan": r["note"]
                }
                for r in history_reqs
            ])
            st.download_button(
                "📥 Download Pencatatan Restock (CSV)",
                df_hist_csv.to_csv(index=False).encode("utf-8"),
                f"pencatatan_restock_{branch}.csv",
                "text/csv"
            )

        st.divider()

        col_h_sales, col_h_logs = st.columns([1.15, 1])
        with col_h_sales:
            st.markdown("### 🛒 Pencatatan Barang Terjual")
            if branch_sales:
                sales_rows = []
                for s in branch_sales:
                    profit_sub = f"<span class='grid-sub'>Margin: +Rp {s.get('profit', 0):,}</span>" if (tier in ["Premium", "Pro"] and can_view_margin) else ""
                    sales_rows.append(
                        f"<td><code>{s['rak']}</code></td>"
                        f"<td><b>{s['item']}</b><span class='grid-sub'>🕒 {s['time']} • Kasir: {s['cashier']}</span></td>"
                        f"<td class='grid-num'>{s['qty']} Pcs</td>"
                        f"<td class='grid-num'>Rp {s['total']:,}{profit_sub}</td>"
                    )
                render_modern_table(["Rak", "Produk & Waktu", "Qty", "Total Transaksi"], sales_rows)
            else:
                st.info("Belum ada pencatatan penjualan di cabang ini.")

        with col_h_logs:
            st.markdown("### 📜 Log Aktivitas & Mutasi Stok")
            log_rows = []
            for l in st.session_state.logs[:15]:
                l_type = l["type"]
                if l_type == "SUCCESS":
                    b_cls = "badge-ok"
                elif l_type == "WARNING":
                    b_cls = "badge-exp"
                elif l_type == "ERROR":
                    b_cls = "badge-low"
                else:
                    b_cls = "badge-info"
                log_rows.append(
                    f"<td><span class='{b_cls}'>{l_type}</span><span class='grid-sub'>{l['time']}</span></td>"
                    f"<td>{l['action']}</td>"
                )
            render_modern_table(["Status & Waktu", "Detail Aktivitas Sistem"], log_rows)

# ------------------------------------------
# TAB 4: MANAJEMEN AKUN TIM & CUSTOM JABATAN LENGKAP
# ------------------------------------------
if "team" in tab_map:
    with tab_map["team"]:
        sub_acc, sub_role = st.tabs(["👤 Daftar Akun Karyawan", "🛡️ Custom Jabatan (Nama, Menu & Hak Akses)"])

        # SUB-TAB 1: AKUN KARYAWAN
        with sub_acc:
            st.subheader(f"👥 Daftar Akun Karyawan ({len(st.session_state.accounts)} Akun Aktif)")
            st.caption("ℹ️ Berpindah ke jabatan dengan Level lebih rendah/setara langsung tanpa password. Berpindah ke jabatan dengan Level lebih tinggi wajib verifikasi password.")

            col_acc_list, col_acc_add = st.columns([1.5, 1])

            with col_acc_list:
                for idx, acc in enumerate(st.session_state.accounts):
                    acc_lvl = get_role_level(acc["role"])
                    with st.container(border=True):
                        ac1, ac2, ac3 = st.columns([2.3, 1.2, 0.9], vertical_alignment="center")
                        with ac1:
                            st.markdown(f"**{acc['name']}** ({acc['email']})")
                            st.caption(f"Jabatan: `{acc['role']}` • **Level Hierarki: {acc_lvl}**")
                        with ac2:
                            if idx == st.session_state.current_user_idx:
                                st.success("Aktif")
                            else:
                                req_pw = needs_password_to_switch(u_role, acc["role"])
                                btn_lbl = "🔒 Login" if req_pw else "🔓 Login"
                                if st.button(btn_lbl, key=f"sw_{idx}", use_container_width=True):
                                    if not req_pw:
                                        st.session_state.current_user_idx = idx
                                        st.session_state.switch_target_idx = None
                                        add_log("INFO", f"{current_user['name']} berpindah ke akun {acc['name']} ({acc['role']})")
                                        st.rerun()
                                    else:
                                        st.session_state.switch_target_idx = idx
                        with ac3:
                            is_only_owner = (acc["role"] == "OWNER" and sum(1 for a in st.session_state.accounts if a["role"] == "OWNER") <= 1)
                            if can_manage_roles and idx != st.session_state.current_user_idx and not is_only_owner:
                                if st.button("🗑️ Hapus", key=f"del_acc_{idx}", use_container_width=True):
                                    active_acc = st.session_state.accounts[st.session_state.current_user_idx]
                                    st.session_state.accounts.pop(idx)
                                    st.session_state.current_user_idx = st.session_state.accounts.index(active_acc)
                                    st.session_state.switch_target_idx = None
                                    st.rerun()

                        if st.session_state.switch_target_idx == idx and idx != st.session_state.current_user_idx:
                            st.divider()
                            pw_c1, pw_c2, pw_c3 = st.columns([2.2, 1, 0.8], vertical_alignment="center")
                            with pw_c1:
                                in_pw = st.text_input(f"Password untuk {acc['name']} ({acc['role']})", type="password", key=f"pw_in_{idx}", label_visibility="collapsed", placeholder=f"Masukkan password {acc['name']}...")
                            with pw_c2:
                                if st.button("Masuk", type="primary", key=f"pw_ok_{idx}", use_container_width=True):
                                    if in_pw == acc.get("password", ""):
                                        st.session_state.current_user_idx = idx
                                        st.session_state.switch_target_idx = None
                                        add_log("INFO", f"Pergantian akun terverifikasi ke {acc['name']} ({acc['role']})")
                                        st.rerun()
                                    else:
                                        st.error("Password salah!")
                            with pw_c3:
                                if st.button("Batal", key=f"pw_cancel_{idx}", use_container_width=True):
                                    st.session_state.switch_target_idx = None
                                    st.rerun()

            with col_acc_add:
                with st.container(border=True):
                    st.markdown("**➕ Tambah Akun Baru**")
                    if can_manage_roles:
                        available_roles = sorted(
                            list(st.session_state.roles_config.keys()),
                            key=lambda r: get_role_level(r),
                            reverse=True
                        )
                        role_choices = available_roles + ["➕ Ketik Jabatan Custom Baru..."]

                        new_acc_name = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
                        new_acc_email = st.text_input("Email", placeholder="budi@storify.id")
                        new_acc_role_sel = st.selectbox(
                            "Pilih Jabatan (Role)",
                            role_choices,
                            format_func=lambda r: r if r.startswith("➕") else f"{r} (Level {get_role_level(r)})"
                        )

                        is_custom_role = (new_acc_role_sel == "➕ Ketik Jabatan Custom Baru...")
                        custom_role_input = ""
                        custom_role_lvl = 3
                        custom_preset = "Kasir / Staf Lapangan"

                        if is_custom_role:
                            custom_role_input = st.text_input(
                                "Nama Jabatan Custom",
                                placeholder="Contoh: KASIR / KEPALA GUDANG / SUPERVISOR / ADMIN"
                            )
                            c_r1, c_r2 = st.columns([1, 1.3])
                            with c_r1:
                                custom_role_lvl = st.number_input("Level (1–9)", min_value=1, max_value=9, value=3, step=1)
                            with c_r2:
                                custom_preset = st.selectbox(
                                    "Template Hak Akses",
                                    ["Kasir / Staf Lapangan", "Supervisor / Kepala Gudang", "Manajer Operasional", "Hanya Lihat (Read-Only)"]
                                )
                            st.caption("ℹ️ Izin menu & aksi detail jabatan ini bisa diatur ulang kapan saja di tab **Custom Jabatan**.")

                        new_acc_pass = st.text_input("Password Akun", type="password", placeholder="Minimal 4 karakter")

                        if st.button("Daftarkan Akun", type="primary", use_container_width=True):
                            if not new_acc_name.strip() or not new_acc_email.strip() or len(new_acc_pass.strip()) < 4:
                                st.warning("Nama, email, dan password (min. 4 karakter) wajib diisi.")
                            elif any(a["email"].lower() == new_acc_email.strip().lower() for a in st.session_state.accounts):
                                st.warning("Email tersebut sudah terdaftar.")
                            elif is_custom_role and not custom_role_input.strip():
                                st.warning("Nama jabatan custom wajib diisi.")
                            else:
                                if is_custom_role:
                                    final_role = custom_role_input.strip().upper()
                                    if final_role not in st.session_state.roles_config:
                                        if custom_preset == "Manajer Operasional":
                                            preset_perms = {k: True for k in ALL_PERMISSIONS}
                                            preset_perms["act_manage_roles"] = False
                                        elif custom_preset == "Supervisor / Kepala Gudang":
                                            preset_perms = {
                                                "menu_monitoring": True, "menu_notif_chat": True, "menu_history": True, "menu_team": False,
                                                "act_sell": True, "act_opname": True, "act_manage_batches": True, "act_manage_products": True,
                                                "act_manage_prices": False, "act_view_margin": False, "act_approve_restock": True,
                                                "act_manage_branches": False, "act_manage_roles": False
                                            }
                                        elif custom_preset == "Kasir / Staf Lapangan":
                                            preset_perms = {
                                                "menu_monitoring": True, "menu_notif_chat": True, "menu_history": False, "menu_team": False,
                                                "act_sell": True, "act_opname": True, "act_manage_batches": False, "act_manage_products": False,
                                                "act_manage_prices": False, "act_view_margin": False, "act_approve_restock": False,
                                                "act_manage_branches": False, "act_manage_roles": False
                                            }
                                        else:
                                            preset_perms = {
                                                "menu_monitoring": True, "menu_notif_chat": True, "menu_history": True, "menu_team": False,
                                                "act_sell": False, "act_opname": False, "act_manage_batches": False, "act_manage_products": False,
                                                "act_manage_prices": False, "act_view_margin": False, "act_approve_restock": False,
                                                "act_manage_branches": False, "act_manage_roles": False
                                            }

                                        st.session_state.roles_config[final_role] = {
                                            "level": safe_int(custom_role_lvl, 3),
                                            "core": False,
                                            "desc": f"Jabatan custom ({custom_preset}).",
                                            "perms": preset_perms
                                        }
                                else:
                                    final_role = new_acc_role_sel

                                st.session_state.accounts.append({
                                    "name": new_acc_name.strip(),
                                    "role": final_role,
                                    "email": new_acc_email.strip(),
                                    "password": new_acc_pass.strip()
                                })
                                add_log("SUCCESS", f"[{current_user['name']}] Menambahkan akun baru: {new_acc_name.strip()} ({final_role})")
                                st.success(f"Akun {new_acc_name.strip()} dengan jabatan {final_role} berhasil dibuat!")
                                time.sleep(0.35)
                                st.rerun()
                    else:
                        st.info("🔒 Jabatan Anda tidak memiliki izin untuk menambahkan akun baru.")

        # SUB-TAB 2: BUAT & CUSTOM JABATAN LENGKAP
        with sub_role:
            st.subheader("🛡️ Custom Jabatan: Menu yang Diakses & Aksi yang Bisa Dilakukan")
            st.caption("Buat atau modifikasi jabatan sesuai kebutuhan operasional toko Anda. Anda bebas mengatur **Nama Jabatan**, **Deskripsi Peran**, **Level Hierarki (1–9)**, **Menu Dashboard yang Muncul**, dan **Aksi yang Diizinkan**.")

            col_r_list, col_r_create = st.columns([1.55, 1], gap="large")

            with col_r_list:
                sorted_roles = sorted(
                    st.session_state.roles_config.items(),
                    key=lambda item: item[1]["level"],
                    reverse=True
                )

                role_table_rows = []
                for r_name, r_data in sorted_roles:
                    menus_on = [lbl.replace(" Menu: ", " ") for k_m, lbl in ALL_MENU_ACCESS.items() if r_data["perms"].get(k_m)]
                    acts_on = [lbl.split(": ")[1] for k_a, lbl in ALL_ACTION_PERMISSIONS.items() if r_data["perms"].get(k_a)]

                    menu_html = " ".join([f"<span class='badge-info'>{m}</span>" for m in menus_on]) if menus_on else "<span class='grid-sub'>Tidak ada menu</span>"
                    act_html = " ".join([f"<span class='batch-chip'>✔ {a}</span>" for a in acts_on]) if acts_on else "<span class='grid-sub'>Hanya Lihat (Read-Only)</span>"

                    role_table_rows.append(
                        f"<td><b>{r_name}</b><span class='grid-sub'>{r_data.get('desc', '-')}</span></td>"
                        f"<td><span class='badge-pro'>Lv.{r_data['level']}</span></td>"
                        f"<td>{menu_html}<div style='margin-top:6px;'>{act_html}</div></td>"
                    )
                render_modern_table(["Nama & Deskripsi Jabatan", "Level", "Menu Diakses & Aksi Diizinkan"], role_table_rows)

                if can_manage_roles:
                    st.markdown("#### ⚙️ Custom Edit Jabatan yang Ada")
                    editable_roles = [r for r, d in sorted_roles if not d.get("core", False)]
                    if editable_roles:
                        sel_edit_role = st.selectbox("Pilih Jabatan untuk Diubah:", editable_roles, key="sel_edit_role_box")
                        target_r_obj = st.session_state.roles_config[sel_edit_role]

                        with st.container(border=True):
                            er_c1, er_c2 = st.columns([1.3, 1])
                            with er_c1:
                                upd_role_name = st.text_input("Nama Jabatan", value=sel_edit_role, key=f"rname_{sel_edit_role}")
                                upd_role_desc = st.text_input("Deskripsi Tugas Jabatan", value=target_r_obj.get("desc", ""), key=f"rdesc_{sel_edit_role}")
                            with er_c2:
                                upd_level = st.slider(
                                    "Tingkat Level Hierarki (1–9)",
                                    min_value=1, max_value=9,
                                    value=min(9, int(target_r_obj["level"])),
                                    key=f"lvl_slider_{sel_edit_role}"
                                )
                                st.caption("Level lebih tinggi memerlukan password saat pindah akun.")

                            st.divider()
                            st.markdown("**1. Daftar Menu Dashboard yang Bisa Diakses:**")
                            upd_perms = {}
                            m_cols = st.columns(2)
                            for idx_m, (m_key, m_label) in enumerate(ALL_MENU_ACCESS.items()):
                                with m_cols[idx_m % 2]:
                                    upd_perms[m_key] = st.checkbox(
                                        m_label,
                                        value=bool(target_r_obj["perms"].get(m_key, True)),
                                        key=f"edit_m_{sel_edit_role}_{m_key}"
                                    )

                            st.markdown("**2. Aksi Operasional yang Bisa Dilakukan:**")
                            a_cols = st.columns(2)
                            for idx_a, (a_key, a_label) in enumerate(ALL_ACTION_PERMISSIONS.items()):
                                with a_cols[idx_a % 2]:
                                    upd_perms[a_key] = st.checkbox(
                                        a_label,
                                        value=bool(target_r_obj["perms"].get(a_key, False)),
                                        key=f"edit_a_{sel_edit_role}_{a_key}"
                                    )

                            eb1, eb2 = st.columns([2, 1])
                            with eb1:
                                if st.button("💾 Simpan Perubahan Jabatan", type="primary", key=f"save_role_btn_{sel_edit_role}", use_container_width=True):
                                    clean_new_rname = upd_role_name.strip().upper()
                                    if not clean_new_rname:
                                        st.error("Nama jabatan tidak boleh kosong.")
                                    elif clean_new_rname != sel_edit_role and clean_new_rname in st.session_state.roles_config:
                                        st.warning(f"Nama jabatan **{clean_new_rname}** sudah dipakai jabatan lain.")
                                    else:
                                        new_role_payload = {
                                            "level": int(upd_level),
                                            "core": False,
                                            "desc": upd_role_desc.strip() or "-",
                                            "perms": upd_perms
                                        }
                                        if clean_new_rname != sel_edit_role:
                                            del st.session_state.roles_config[sel_edit_role]
                                            st.session_state.roles_config[clean_new_rname] = new_role_payload
                                            for acc_item in st.session_state.accounts:
                                                if acc_item["role"] == sel_edit_role:
                                                    acc_item["role"] = clean_new_rname
                                            add_log("SUCCESS", f"[{current_user['name']}] Mengubah jabatan {sel_edit_role} -> {clean_new_rname} (Lv.{upd_level})")
                                        else:
                                            st.session_state.roles_config[sel_edit_role] = new_role_payload
                                            add_log("SUCCESS", f"[{current_user['name']}] Memperbarui izin jabatan {sel_edit_role} (Lv.{upd_level})")
                                        st.toast(f"Konfigurasi jabatan {clean_new_rname} disimpan!", icon="✅")
                                        st.rerun()
                            with eb2:
                                in_use = any(a["role"] == sel_edit_role for a in st.session_state.accounts)
                                if st.button("🗑️ Hapus Jabatan", key=f"del_role_btn_{sel_edit_role}", disabled=in_use, use_container_width=True, help="Tidak bisa menghapus jabatan yang masih dipakai akun aktif"):
                                    del st.session_state.roles_config[sel_edit_role]
                                    add_log("WARNING", f"[{current_user['name']}] Menghapus jabatan {sel_edit_role}")
                                    st.rerun()
                else:
                    st.info("🔒 Anda tidak memiliki izin untuk mengubah konfigurasi jabatan.")

            with col_r_create:
                with st.container(border=True):
                    st.markdown("### ➕ Buat Jabatan Custom Baru")
                    if can_manage_roles:
                        with st.form("form_create_custom_role", clear_on_submit=True):
                            new_r_name = st.text_input("Nama Jabatan Baru", placeholder="Contoh: KASIR / KEPALA GUDANG / AUDITOR")
                            new_r_desc = st.text_input("Deskripsi Peran", placeholder="Contoh: Bertugas mengecek batch exp dan kasir")
                            new_r_level = st.slider("Tentukan Tinggi Level Jabatan", min_value=1, max_value=9, value=4)
                            st.caption("Lv.1–3: Staf Operasional | Lv.4–7: Koordinator/Supervisor | Lv.8–9: Manajerial")
                            st.divider()

                            new_r_perms = {}
                            st.markdown("**1. Menu yang Bisa Diakses:**")
                            for m_key, m_label in ALL_MENU_ACCESS.items():
                                new_r_perms[m_key] = st.checkbox(m_label, value=(m_key in ["menu_monitoring", "menu_notif_chat"]), key=f"new_m_{m_key}")

                            st.markdown("**2. Aksi yang Bisa Dilakukan:**")
                            for a_key, a_label in ALL_ACTION_PERMISSIONS.items():
                                new_r_perms[a_key] = st.checkbox(a_label, value=(a_key in ["act_sell", "act_opname"]), key=f"new_a_{a_key}")

                            if st.form_submit_button("✨ Buat Jabatan Custom", type="primary", use_container_width=True):
                                clean_r = new_r_name.strip().upper()
                                if not clean_r:
                                    st.error("Nama jabatan wajib diisi.")
                                elif clean_r in st.session_state.roles_config:
                                    st.warning(f"Jabatan **{clean_r}** sudah ada.")
                                else:
                                    st.session_state.roles_config[clean_r] = {
                                        "level": int(new_r_level),
                                        "core": False,
                                        "desc": new_r_desc.strip() or "Jabatan custom operasional.",
                                        "perms": new_r_perms
                                    }
                                    add_log("SUCCESS", f"[{current_user['name']}] Membuat jabatan custom baru: {clean_r} (Level {new_r_level})")
                                    st.toast(f"Jabatan {clean_r} (Level {new_r_level}) berhasil dibuat!", icon="🎉")
                                    st.rerun()
                    else:
                        st.info("🔒 Hanya jabatan berizin yang dapat membuat jabatan baru.")
