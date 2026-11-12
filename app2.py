import streamlit as st
import time
from datetime import datetime

# Configuration
st.set_page_config(page_title="Storify - Smart Label & Dynamic Pricing", layout="wide", page_icon="🏷️")

# ==========================================
# 1. INISIALISASI STATE
# ==========================================
if "app_tier" not in st.session_state:
    st.session_state.app_tier = None  # None = Belum pilih paket

if "lang" not in st.session_state:
    st.session_state.lang = "ID"

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "store_name" not in st.session_state:
    st.session_state.store_name = "Storify - Cabang Utama"

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_rak" not in st.session_state:
    st.session_state.selected_rak = None

if "user" not in st.session_state:
    st.session_state.user = {"name": "Beatrix", "role": "OWNER", "email": "beatrix@storify.id"}

if "logs" not in st.session_state:
    st.session_state.logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Storify IoT & E-Paper Cloud system initialized."}
    ]

if "original_prices" not in st.session_state:
    st.session_state.original_prices = {}

if "flash_sale_active" not in st.session_state:
    st.session_state.flash_sale_active = False

if "flash_sale_end" not in st.session_state:
    st.session_state.flash_sale_end = 0.0

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rak A1": {"item": "Kopi Sachet 25g", "category": "Makanan & Minuman", "qty": 20, "price": 15000, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300", "inflow": [5, 10, 15, 20], "outflow": [3, 8, 12, 18]},
        "Rak B2": {"item": "Keripik Singkong 100g", "category": "Makanan & Minuman", "qty": 4, "price": 12000, "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300", "inflow": [2, 5, 8, 10], "outflow": [4, 7, 9, 14]},
        "Rak C3": {"item": "Air Mineral 600ml", "category": "Makanan & Minuman", "qty": 15, "price": 5000, "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300", "inflow": [10, 20, 25, 30], "outflow": [8, 15, 22, 25]},
        "Rak D4": {"item": "Deterjen Bubuk 800g", "category": "Kebutuhan Rumah Tangga", "qty": 8, "price": 25000, "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300", "inflow": [3, 6, 9, 12], "outflow": [2, 5, 7, 10]},
    }

# ==========================================
# 2. SISTEM TEMA & CSS (BUG FIX TOTAL)
# ==========================================
theme = st.session_state.theme
if theme == "Dark":
    c_bg = "#0f172a"
    c_card = "#1e293b"
    c_text = "#f8fafc"
    c_subtext = "#94a3b8"
    c_border = "#334155"
    c_input_bg = "#334155"
    c_input_text = "#ffffff"
    c_primary = "#3b82f6"
    c_popover = "#0f172a"
else:
    c_bg = "#f8fafc"
    c_card = "#ffffff"
    c_text = "#0f172a"
    c_subtext = "#64748b"
    c_border = "#e2e8f0"
    c_input_bg = "#ffffff"
    c_input_text = "#0f172a"
    c_primary = "#2563eb"
    c_popover = "#ffffff"

st.markdown(f"""
<style>
    /* Global App Background */
    .stApp {{ background-color: {c_bg}; }}
    h1, h2, h3, h4, h5, h6, p, label, span {{ color: {c_text} !important; }}
    
    /* Fix Input, Selectbox, Number Input agar teks tidak hilang */
    [data-baseweb="input"] {{ background-color: {c_input_bg} !important; border-color: {c_border} !important; }}
    [data-baseweb="input"] input {{ color: {c_input_text} !important; -webkit-text-fill-color: {c_input_text} !important; }}
    
    [data-baseweb="select"] > div {{ background-color: {c_input_bg} !important; color: {c_input_text} !important; border-color: {c_border} !important; }}
    [data-baseweb="select"] span {{ color: {c_input_text} !important; }}
    
    [data-baseweb="popover"] > div {{ background-color: {c_popover} !important; }}
    [data-baseweb="menu"] {{ background-color: {c_card} !important; border: 1px solid {c_border} !important; }}
    [data-baseweb="option"] {{ color: {c_text} !important; background-color: transparent !important; }}
    [data-baseweb="option"]:hover {{ background-color: {c_primary} !important; color: white !important; }}

    /* Fix Popover Button Background */
    button[aria-haspopup="dialog"], .stPopover > button {{
        background-color: {c_input_bg} !important;
        border: 1px solid {c_border} !important;
        color: {c_input_text} !important;
    }}
    button[aria-haspopup="dialog"] p, .stPopover > button p {{ color: {c_input_text} !important; }}
    
    /* Tombol Utama */
    .stButton > button {{
        border-radius: 8px !important;
        border: 1px solid {c_border} !important;
        background-color: {c_card} !important;
        transition: all 0.2s;
    }}
    .stButton > button:hover {{ border-color: {c_primary} !important; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2); }}
    
    /* Komponen Kustom UI */
    .saas-card {{
        background: {c_card}; padding: 24px; border-radius: 16px; border: 1px solid {c_border};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; transition: 0.3s;
    }}
    .saas-card:hover {{ border-color: {c_primary}; transform: translateY(-2px); }}
    .price-tag {{
        background: rgba(59,130,246,0.1); color: {c_primary}; padding: 8px 16px;
        border-radius: 8px; font-weight: 800; font-size: 18px; border: 1px solid {c_border}; display: inline-block;
    }}
    .tier-box {{
        background: {c_card}; border: 2px solid {c_border}; padding: 30px; border-radius: 20px;
        text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: space-between;
    }}
    .tier-box.pro {{ border-color: {c_primary}; box-shadow: 0 10px 25px rgba(59,130,246,0.2); }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. ROUTING: HALAMAN PILIH PAKET (LANDING)
# ==========================================
if st.session_state.app_tier is None:
    st.markdown("<h1 style='text-align: center; margin-bottom: 10px; font-size: 3rem;'>Pilih Paket Storify Anda 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; margin-bottom: 40px;'>Pilih fitur yang paling sesuai dengan skala bisnis retail Anda.</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
        <div class="tier-box">
            <h2 style="color:{c_text};">Standard</h2>
            <h3 style="color:{c_subtext};">Gratis</h3>
            <hr>
            <p align="left">✅ Manajemen Stok & Rak<br>✅ Ubah Harga Manual<br>✅ Multi-User Basic<br>❌ Flash Sale Massal<br>❌ Terminal Audit Log<br>❌ AI Smart Suggestions</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Standard", use_container_width=True, key="btn_std"):
            st.session_state.app_tier = "Standard"
            st.rerun()

    with c2:
        st.markdown(f"""
        <div class="tier-box">
            <h2 style="color:{c_text};">Premium</h2>
            <h3 style="color:{c_primary};">Rp 199.000<span style="font-size:14px;">/bln</span></h3>
            <hr>
            <p align="left">✅ <b>Semua fitur Standard</b><br>✅ Fitur Flash Sale Massal<br>✅ Terminal Audit Log<br>✅ Laporan Grafik Interaktif<br>❌ AI Smart Suggestions</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Premium", use_container_width=True, key="btn_prm"):
            st.session_state.app_tier = "Premium"
            st.rerun()

    with c3:
        st.markdown(f"""
        <div class="tier-box pro">
            <div style="background:{c_primary}; color:white; padding:4px 10px; border-radius:20px; font-size:12px; display:inline-block; margin-bottom:10px;">PALING POPULER</div>
            <h2 style="color:{c_text};">Pro</h2>
            <h3 style="color:{c_primary};">Rp 499.000<span style="font-size:14px;">/bln</span></h3>
            <hr>
            <p align="left">✅ <b>Semua fitur Premium</b><br>✅ <b>AI Smart Advisor</b><br>✅ Rekomendasi Restock Pintar<br>✅ Prioritas Cloud Sync<br>✅ Custom Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Pro", type="primary", use_container_width=True, key="btn_pro"):
            st.session_state.app_tier = "Pro"
            st.rerun()
            
    st.stop() # Hentikan eksekusi script sampai paket dipilih

# ==========================================
# 4. APLIKASI UTAMA (SETELAH PILIH PAKET)
# ==========================================
lang = st.session_state.lang

# Auto Restore Flash Sale
current_time_epoch = time.time()
if st.session_state.flash_sale_active and current_time_epoch > st.session_state.flash_sale_end:
    for rak, orig_p in st.session_state.original_prices.items():
        if rak in st.session_state.inventory:
            st.session_state.inventory[rak]["price"] = orig_p
    st.session_state.flash_sale_active = False
    st.session_state.original_prices = {}
    st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Flash Sale otomatis berakhir. Harga normal direstorasi."})

# HEADER
col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title(f"🏷️ {st.session_state.store_name}")
    tier_badge = "gray" if st.session_state.app_tier == "Standard" else ("blue" if st.session_state.app_tier == "Premium" else "orange")
    st.markdown(f"**Paket Aktif:** <span style='color:white; background:{tier_badge}; padding:2px 8px; border-radius:10px; font-size:12px;'>{st.session_state.app_tier.upper()}</span>", unsafe_allow_html=True)
with col_h2:
    sc1, sc2 = st.columns(2)
    with sc1:
        sel_lang = st.selectbox("Bahasa", ["ID", "EN"], index=0 if lang=="ID" else 1)
        if sel_lang != st.session_state.lang: st.session_state.lang = sel_lang; st.rerun()
    with sc2:
        sel_theme = st.selectbox("Tema", ["Light", "Dark"], index=0 if theme=="Light" else 1)
        if sel_theme != st.session_state.theme: st.session_state.theme = sel_theme; st.rerun()

# SIDEBAR CONTROL PANEL
st.sidebar.header("⚙️ Storify Control Panel")

with st.sidebar.expander("🏪 Profil Toko & Paket", expanded=False):
    new_store_name = st.text_input("Nama Cabang", st.session_state.store_name)
    if st.button("Simpan Nama"):
        st.session_state.store_name = new_store_name
        st.rerun()
    st.divider()
    if st.button("🔄 Ganti Paket Fitur (Upgrade/Downgrade)"):
        st.session_state.app_tier = None
        st.rerun()

with st.sidebar.expander("👤 Ganti Akun Karyawan", expanded=False):
    acc = st.selectbox("Akun Login", ["Beatrix (Owner)", "Natannael (Developer)", "Walden (Developer)", "Nathalee (Staff Gudang)"])
    if "Beatrix" in acc: st.session_state.user = {"name": "Beatrix", "role": "OWNER", "email": "beatrix@storify.id"}
    elif "Natannael" in acc: st.session_state.user = {"name": "Natannael", "role": "DEVELOPER", "email": "natannael@storify.id"}
    elif "Walden" in acc: st.session_state.user = {"name": "Walden", "role": "DEVELOPER", "email": "walden@storify.id"}
    else: st.session_state.user = {"name": "Nathalee", "role": "STAFF", "email": "nathalee@storify.id"}
    if st.button("Terapkan Akun"): st.rerun()

is_privileged = st.session_state.user["role"] in ["OWNER", "DEVELOPER", "MANAGER"]

if is_privileged:
    with st.sidebar.expander("➕ Tambah Produk", expanded=False):
        target_rak = st.text_input("Kode Rak", "Rak E5")
        item_name = st.text_input("Nama Produk", "Produk Baru")
        img_source = st.radio("Sumber Foto", ["Gunakan Link URL", "Upload File Lokal"])
        final_img = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300"
        
        if img_source == "Upload File Lokal":
            uploaded_file = st.file_uploader("Pilih Foto", type=["png", "jpg", "jpeg"])
            if uploaded_file is not None:
                import base64
                base64_str = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                final_img = f"data:image/jpeg;base64,{base64_str}"
        else:
            url_input = st.text_input("URL Foto", final_img)
            if url_input: final_img = url_input
            
        qty_val = st.number_input("Stok Awal", min_value=0, value=10)
        price_val = st.number_input("Harga (Rp)", min_value=0, value=10000, step=1000)
        
        if st.button("Simpan Produk"):
            st.session_state.inventory[target_rak] = {"item": item_name, "category": "General", "qty": qty_val, "price": price_val, "image": final_img, "inflow": [qty_val], "outflow": [0]}
            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "SUCCESS", "action": f"Produk ditambahkan: {item_name} di {target_rak}"})
            st.rerun()

    if st.session_state.app_tier in ["Premium", "Pro"]:
        with st.sidebar.expander("⚡ Flash Sale Massal (Premium/Pro)", expanded=False):
            disc_percent = st.slider("Diskon (%)", 5, 50, 15, 5)
            duration_sec = st.selectbox("Durasi (Detik)", [15, 30, 60])
            
            if not st.session_state.flash_sale_active:
                if st.button("Jalankan Flash Sale"):
                    st.session_state.original_prices = {r: d["price"] for r, d in st.session_state.inventory.items()}
                    for r in st.session_state.inventory:
                        st.session_state.inventory[r]["price"] = int(st.session_state.inventory[r]["price"] * (1 - disc_percent / 100))
                    st.session_state.flash_sale_active = True
                    st.session_state.flash_sale_end = time.time() + duration_sec
                    st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "WARNING", "action": f"Flash Sale {disc_percent}% aktif!"})
                    st.rerun()
            else:
                st.warning(f"Sisa Waktu: {int(st.session_state.flash_sale_end - time.time())}s")
                if st.button("Batalkan Flash Sale"):
                    for r, op in st.session_state.original_prices.items():
                        if r in st.session_state.inventory: st.session_state.inventory[r]["price"] = op
                    st.session_state.flash_sale_active = False
                    st.session_state.original_prices = {}
                    st.rerun()
    else:
        st.sidebar.info("🔒 Flash Sale Massal hanya tersedia di paket Premium & Pro.")
else:
    st.sidebar.info("ℹ️ Mode Staff: Anda hanya memiliki akses untuk Restock barang.")

# ==========================================
# 5. HALAMAN DETAIL PRODUK
# ==========================================
if st.session_state.page == "detail":
    rak_key = st.session_state.selected_rak
    if rak_key not in st.session_state.inventory:
        st.session_state.page = "home"; st.rerun()
        
    prod = st.session_state.inventory[rak_key]
    
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page = "home"; st.rerun()
        
    st.markdown(f"## 📊 Analitik Produk: {rak_key}")
    dc1, dc2 = st.columns([1, 2])
    with dc1:
        st.image(prod.get("image"), use_container_width=True)
    with dc2:
        st.markdown(f"### {prod['item']}")
        st.write(f"📦 **Stok Saat Ini:** {prod['qty']} Pcs")
        st.write(f"🏷️ **Harga Sinkron E-Paper:** Rp {prod['price']:,}")
    
    st.divider()
    if st.session_state.app_tier in ["Premium", "Pro"]:
        st.subheader("📈 Grafik Arus Stok (Inflow vs Outflow)")
        st.line_chart({"Masuk (Inflow)": prod.get("inflow"), "Keluar (Outflow)": prod.get("outflow")})
    else:
        st.info("🔒 Grafik analitik Lanjutan hanya tersedia di paket Premium & Pro.")
    st.stop()

# ==========================================
# 6. DASHBOARD UTAMA
# ==========================================

# EKSKLUSIF PRO: AI Smart Advisor
if st.session_state.app_tier == "Pro":
    low_stock = [k for k, v in st.session_state.inventory.items() if v['qty'] <= 5]
    if low_stock:
        ai_msg = f"⚠️ **AI ALERT:** Segera lakukan restock untuk {', '.join(low_stock)} untuk menghindari kehilangan potensi penjualan."
        bg_ai = "#fee2e2"
        border_ai = "#ef4444"
        text_ai = "#991b1b"
    else:
        ai_msg = "✨ **AI INSIGHT:** Stok toko dalam kondisi prima. Waktu yang tepat untuk mengaktifkan Flash Sale akhir pekan."
        bg_ai = "#dcfce7"
        border_ai = "#22c55e"
        text_ai = "#166534"
        
    if theme == "Dark": bg_ai = "#1e293b"; text_ai = "#e2e8f0"
        
    st.markdown(f"""
    <div style="background:{bg_ai}; border:1px solid {border_ai}; padding:15px 20px; border-radius:12px; margin-bottom:20px; color:{text_ai};">
        <b>💡 Storify AI Advisor (Pro Feature):</b><br>{ai_msg}
    </div>
    """, unsafe_allow_html=True)

fc1, fc2 = st.columns([2, 2])
with fc1:
    cats = ["Semua Kategori"] + list(set(d.get("category", "General") for d in st.session_state.inventory.values()))
    sel_cat = st.selectbox("Filter Kategori", cats)
with fc2:
    search_q = st.text_input("Cari Produk...", "")

st.divider()

if not st.session_state.inventory:
    st.info("Belum ada produk terdaftar.")
else:
    for rak_id, data in st.session_state.inventory.items():
        if sel_cat != "Semua Kategori" and data.get("category", "General") != sel_cat: continue
        if search_q.lower() not in data["item"].lower() and search_q.lower() not in rak_id.lower(): continue
        
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        c_img, c1, c2, c3, c4 = st.columns([1, 2, 2, 2, 2])
        
        with c_img: st.image(data.get("image"), use_container_width=True)
        with c1:
            st.markdown(f"#### 📍 {rak_id}")
            st.write(f"**{data['item']}**")
        with c2:
            st.write(f"📦 Stok: {data['qty']} Pcs")
            if data['qty'] <= 5: st.markdown("<span style='color:#ef4444; font-weight:bold;'>⚠️ Stok Menipis</span>", unsafe_allow_html=True)
            else: st.markdown("<span style='color:#10b981; font-weight:bold;'>✔ Aman</span>", unsafe_allow_html=True)
        with c3:
            st.write("🏷️ Harga E-Paper")
            st.markdown(f'<div class="price-tag">Rp {data["price"]:,}</div>', unsafe_allow_html=True)
        with c4:
            if st.button("🔍 Detail", key=f"det_{rak_id}"):
                st.session_state.selected_rak = rak_id
                st.session_state.page = "detail"
                st.rerun()
                
            with st.popover("⚙️ Kelola (Manage)"):
                new_q = st.number_input(f"Ubah Stok ({rak_id})", min_value=0, value=data["qty"], key=f"q_{rak_id}")
                if is_privileged:
                    new_p = st.number_input(f"Ubah Harga (Rp)", min_value=0, value=int(data["price"]), step=1000, key=f"p_{rak_id}")
                    if st.button("💾 Simpan Perubahan", key=f"sv_{rak_id}"):
                        st.session_state.inventory[rak_id]["qty"] = new_q
                        st.session_state.inventory[rak_id]["price"] = new_p
                        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": f"[{st.session_state.user['name']}] Update {rak_id} sukses."})
                        st.rerun()
                    if st.button("🗑️ Hapus Produk", type="primary", key=f"del_{rak_id}"):
                        del st.session_state.inventory[rak_id]
                        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "ERROR", "action": f"[{st.session_state.user['name']}] Menghapus {rak_id}."})
                        st.rerun()
                else:
                    if st.button("💾 Simpan Stok", key=f"sv_{rak_id}"):
                        st.session_state.inventory[rak_id]["qty"] = new_q
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 7. TERMINAL AUDIT LOG (Premium & Pro Only)
# ==========================================
if st.session_state.app_tier in ["Premium", "Pro"]:
    st.divider()
    st.subheader("📜 Terminal Audit Log")
    if is_privileged:
        t_text = "".join([f"{l['time']} [{l.get('type', 'INFO'):<9}] >> {l['action']}\n" for l in st.session_state.logs[:15]])
        st.markdown(f'<div class="log-terminal">{t_text}</div>', unsafe_allow_html=True)
    else:
        st.warning("Akses Ditolak: Hanya Owner & Developer yang dapat membaca Log Audit.")
