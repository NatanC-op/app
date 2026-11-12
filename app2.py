import streamlit as st
import time
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Storify - Smart Label & Dynamic Pricing", layout="wide", page_icon="🏷️")

# ==========================================
# 2. INISIALISASI STATE
# ==========================================
if "app_tier" not in st.session_state:
    st.session_state.app_tier = None  # None = Belum pilih paket

if "lang" not in st.session_state:
    st.session_state.lang = "ID"

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

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
# 3. SISTEM TEMA & CSS DINAMIS (UI ULTRA-PREMIUM)
# ==========================================
theme = st.session_state.theme
if theme == "Dark":
    c_bg = "#090d16"
    c_card = "#111827"
    c_text = "#f8fafc"
    c_subtext = "#94a3b8"
    c_border = "#1f2937"
    c_input_bg = "#1f2937"
    c_input_text = "#ffffff"
    c_primary = "#3b82f6"
    c_popover = "#0f172a"
    glow_pro = "0 0 30px rgba(59, 130, 246, 0.15)"
else:
    c_bg = "#f4f7fb"
    c_card = "#ffffff"
    c_text = "#0f172a"
    c_subtext = "#64748b"
    c_border = "#e2e8f0"
    c_input_bg = "#ffffff"
    c_input_text = "#0f172a"
    c_primary = "#2563eb"
    c_popover = "#ffffff"
    glow_pro = "0 10px 30px rgba(37, 99, 235, 0.15)"

st.markdown(f"""
<style>
    /* Global App Background */
    .stApp {{ background-color: {c_bg}; font-family: 'Inter', sans-serif; }}
    h1, h2, h3, h4, h5, h6, p, label, span {{ color: {c_text} !important; }}
    
    /* Memperbaiki Semua Input & Popover agar selalu terlihat jelas */
    [data-baseweb="input"] {{ background-color: {c_input_bg} !important; border-color: {c_border} !important; border-radius: 10px !important; }}
    [data-baseweb="input"] input {{ color: {c_input_text} !important; -webkit-text-fill-color: {c_input_text} !important; }}
    
    [data-baseweb="select"] > div {{ background-color: {c_input_bg} !important; color: {c_input_text} !important; border-color: {c_border} !important; border-radius: 10px !important; }}
    [data-baseweb="select"] span {{ color: {c_input_text} !important; }}
    
    [data-baseweb="popover"] > div {{ background-color: {c_popover} !important; border-radius: 12px; }}
    [data-baseweb="menu"] {{ background-color: {c_card} !important; border: 1px solid {c_border} !important; }}
    [data-baseweb="option"] {{ color: {c_text} !important; background-color: transparent !important; }}
    [data-baseweb="option"]:hover {{ background-color: {c_primary} !important; color: white !important; }}

    button[aria-haspopup="dialog"], .stPopover > button {{
        background-color: {c_input_bg} !important;
        border: 1px solid {c_border} !important;
        color: {c_input_text} !important;
        border-radius: 10px !important;
    }}
    button[aria-haspopup="dialog"] p, .stPopover > button p {{ color: {c_input_text} !important; }}
    
    /* Tombol Utama Streamlit */
    .stButton > button {{
        border-radius: 10px !important;
        border: 1px solid {c_border} !important;
        background-color: {c_card} !important;
        font-weight: 600;
        transition: all 0.25s ease;
    }}
    .stButton > button:hover {{ border-color: {c_primary} !important; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2); transform: translateY(-1px); }}
    
    /* CSS Kartu Produk di Dashboard */
    .saas-card {{
        background: {c_card}; padding: 24px; border-radius: 16px; border: 1px solid {c_border};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 20px; transition: 0.3s;
    }}
    .saas-card:hover {{ border-color: {c_primary}; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08); transform: translateY(-2px); }}
    
    .price-tag {{
        background: rgba(59,130,246,0.1); color: {c_primary}; padding: 8px 16px;
        border-radius: 8px; font-weight: 800; font-size: 18px; border: 1px solid {c_border}; display: inline-block;
    }}

    /* CSS Khusus Halaman Pricing / Pemilihan Paket */
    .tier-box {{
        background: {c_card}; border: 1px solid {c_border}; padding: 35px 25px; border-radius: 24px;
        text-align: left; height: 100%; display: flex; flex-direction: column; position: relative;
        transition: transform 0.3s, box-shadow 0.3s;
    }}
    .tier-box:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
    .tier-box.pro {{ border: 2px solid {c_primary}; box-shadow: {glow_pro}; }}
    
    ul.feat-list {{ list-style-type: none; padding-left: 0; margin-top: 20px; flex-grow: 1; }}
    ul.feat-list li {{ margin-bottom: 12px; font-size: 15px; color: {c_text}; display: flex; align-items: start; gap: 10px; line-height: 1.4; }}
    .feat-list .check {{ color: #10b981; font-weight: bold; font-size: 16px; }}
    .feat-list .cross {{ color: #ef4444; font-weight: bold; font-size: 16px; opacity: 0.5; }}
    
    .badge-populer {{
        position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
        background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white;
        padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; letter-spacing: 1px;
    }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. ROUTING: HALAMAN PILIH PAKET (LANDING)
# ==========================================
if st.session_state.app_tier is None:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-top: 20px;'>Pilih Paket Storify Anda 🚀</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.1rem; color: {c_subtext}; margin-bottom: 30px;'>Solusi manajemen stok dan e-paper cerdas untuk segala ukuran bisnis.</p>", unsafe_allow_html=True)
    
    # Toggle Siklus Tagihan
    col_t1, col_t2, col_t3 = st.columns([1, 2, 1])
    with col_t2:
        billing_cycle = st.radio(
            "Siklus Tagihan", 
            ["Mingguan", "Bulanan", "Tahunan"], 
            horizontal=True, 
            label_visibility="collapsed"
        )
    st.write("") # Spacer

    # Harga Dinamis berdasarkan Pilihan Toggle
    p_std = {"Mingguan": "35.000", "Bulanan": "125.000", "Tahunan": "1.400.000"}[billing_cycle]
    p_prm = {"Mingguan": "50.000", "Bulanan": "230.000", "Tahunan": "2.500.000"}[billing_cycle]
    p_pro = {"Mingguan": "100.000", "Bulanan": "350.000", "Tahunan": "4.000.000"}[billing_cycle]
    sfx = {"Mingguan": "/mgg", "Bulanan": "/bln", "Tahunan": "/thn"}[billing_cycle]

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
        <div class="tier-box">
            <h2 style="margin:0; font-size:1.5rem;">Standard</h2>
            <p style="color:{c_subtext}; margin:5px 0 15px 0; font-size:14px;">Untuk toko skala kecil & UMKM</p>
            <h1 style="color:{c_text}; font-size:2.2rem; margin:0;">Rp {p_std}<span style="font-size:1rem; color:{c_subtext}; font-weight:normal;">{sfx}</span></h1>
            <ul class="feat-list">
                <li><span class="check">✔</span> Manajemen Stok & Rak Dasar</li>
                <li><span class="check">✔</span> Ubah Harga Manual E-Paper</li>
                <li><span class="check">✔</span> Multi-User (Owner & Staff)</li>
                <li><span class="cross">✖</span> Fitur Flash Sale Massal</li>
                <li><span class="cross">✖</span> Terminal Audit Log Keamanan</li>
                <li><span class="cross">✖</span> AI Smart Advisor</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Standard", use_container_width=True, key="btn_std"):
            st.session_state.app_tier = "Standard"
            st.rerun()

    with c2:
        st.markdown(f"""
        <div class="tier-box">
            <h2 style="margin:0; font-size:1.5rem; color:{c_primary};">Premium</h2>
            <p style="color:{c_subtext}; margin:5px 0 15px 0; font-size:14px;">Untuk minimarket berkembang</p>
            <h1 style="color:{c_text}; font-size:2.2rem; margin:0;">Rp {p_prm}<span style="font-size:1rem; color:{c_subtext}; font-weight:normal;">{sfx}</span></h1>
            <ul class="feat-list">
                <li><span class="check">✔</span> <b>Semua fitur Standard</b></li>
                <li><span class="check">✔</span> Fitur Flash Sale Massal Otomatis</li>
                <li><span class="check">✔</span> Akses Terminal Audit Log</li>
                <li><span class="check">✔</span> Laporan Grafik Interaktif</li>
                <li><span class="cross">✖</span> AI Smart Advisor</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Premium", use_container_width=True, key="btn_prm"):
            st.session_state.app_tier = "Premium"
            st.rerun()

    with c3:
        st.markdown(f"""
        <div class="tier-box pro">
            <div class="badge-populer">PALING POPULER</div>
            <h2 style="margin:0; font-size:1.5rem;">Pro <span style="font-size:14px; font-weight:normal; background:rgba(59,130,246,0.2); padding:2px 8px; border-radius:10px; color:{c_primary};">Enterprise</span></h2>
            <p style="color:{c_subtext}; margin:5px 0 15px 0; font-size:14px;">Untuk skala besar & manajemen AI</p>
            <h1 style="color:{c_text}; font-size:2.2rem; margin:0;">Rp {p_pro}<span style="font-size:1rem; color:{c_subtext}; font-weight:normal;">{sfx}</span></h1>
            <ul class="feat-list">
                <li><span class="check">✔</span> <b>Semua fitur Premium</b></li>
                <li><span class="check">✔</span> <b>AI Smart Advisor (Saran Pintar)</b></li>
                <li><span class="check">✔</span> Deteksi & Rekomendasi Restock Otomatis</li>
                <li><span class="check">✔</span> Prioritas Sinkronisasi Cloud (0 Delay)</li>
                <li><span class="check">✔</span> Kostumisasi Dashboard Penuh</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Pilih Pro", type="primary", use_container_width=True, key="btn_pro"):
            st.session_state.app_tier = "Pro"
            st.rerun()
            
    st.stop() # Hentikan skrip di sini sebelum paket dipilih

# ==========================================
# 5. APLIKASI UTAMA (SETELAH PILIH PAKET)
# ==========================================

# Auto Restore Flash Sale
current_time_epoch = time.time()
if st.session_state.flash_sale_active and current_time_epoch > st.session_state.flash_sale_end:
    for rak, orig_p in st.session_state.original_prices.items():
        if rak in st.session_state.inventory:
            st.session_state.inventory[rak]["price"] = orig_p
    st.session_state.flash_sale_active = False
    st.session_state.original_prices = {}
    st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Flash Sale otomatis berakhir. Harga normal direstorasi."})

# HEADER APLIKASI
col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.title(f"🏷️ {st.session_state.store_name}")
    tier_badge_color = "#64748b" if st.session_state.app_tier == "Standard" else ("#3b82f6" if st.session_state.app_tier == "Premium" else "#8b5cf6")
    st.markdown(f"**Paket Aktif:** <span style='color:white; background:{tier_badge_color}; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:bold; letter-spacing:0.5px;'>STORIFY {st.session_state.app_tier.upper()}</span>", unsafe_allow_html=True)
with col_h2:
    sc1, sc2 = st.columns(2)
    with sc1:
        sel_lang = st.selectbox("Bahasa", ["ID", "EN"], index=0 if st.session_state.lang=="ID" else 1, key="lang_sel")
        if sel_lang != st.session_state.lang: st.session_state.lang = sel_lang; st.rerun()
    with sc2:
        sel_theme = st.selectbox("Tema UI", ["Light", "Dark"], index=0 if st.session_state.theme=="Light" else 1, key="thm_sel")
        if sel_theme != st.session_state.theme: st.session_state.theme = sel_theme; st.rerun()

# SIDEBAR CONTROL PANEL
st.sidebar.header("⚙️ Control Panel")

with st.sidebar.expander("🏪 Profil Toko & Tagihan", expanded=False):
    new_store_name = st.text_input("Nama Cabang", st.session_state.store_name)
    if st.button("Simpan Nama"):
        st.session_state.store_name = new_store_name
        st.rerun()
    st.divider()
    if st.button("🔄 Upgrade / Ganti Paket"):
        st.session_state.app_tier = None
        st.rerun()

with st.sidebar.expander("👤 Ganti Akun Pengguna", expanded=False):
    acc = st.selectbox("Login Sebagai", ["Beatrix (Owner)", "Natannael (Developer)", "Walden (Developer)", "Nathalee (Staff Gudang)"])
    if "Beatrix" in acc: st.session_state.user = {"name": "Beatrix", "role": "OWNER", "email": "beatrix@storify.id"}
    elif "Natannael" in acc: st.session_state.user = {"name": "Natannael", "role": "DEVELOPER", "email": "natannael@storify.id"}
    elif "Walden" in acc: st.session_state.user = {"name": "Walden", "role": "DEVELOPER", "email": "walden@storify.id"}
    else: st.session_state.user = {"name": "Nathalee", "role": "STAFF", "email": "nathalee@storify.id"}
    if st.button("Terapkan Akun"): st.rerun()

# Hak Akses
is_privileged = st.session_state.user["role"] in ["OWNER", "DEVELOPER", "MANAGER"]

if is_privileged:
    with st.sidebar.expander("➕ Tambah Produk Baru", expanded=False):
        target_rak = st.text_input("Kode Rak", "Rak E5")
        item_name = st.text_input("Nama Produk", "Produk Baru")
        img_source = st.radio("Sumber Foto", ["Gunakan Link URL", "Upload File Lokal"])
        final_img = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300"
        
        if img_source == "Upload File Lokal":
            uploaded_file = st.file_uploader("Pilih Foto (PNG/JPG)", type=["png", "jpg", "jpeg"])
            if uploaded_file is not None:
                import base64
                base64_str = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                final_img = f"data:image/jpeg;base64,{base64_str}"
        else:
            url_input = st.text_input("URL Foto", final_img)
            if url_input: final_img = url_input
            
        qty_val = st.number_input("Stok Awal", min_value=0, value=10)
        price_val = st.number_input("Harga (Rp)", min_value=0, value=10000, step=1000)
        
        if st.button("Simpan ke Database"):
            st.session_state.inventory[target_rak] = {"item": item_name, "category": "General", "qty": qty_val, "price": price_val, "image": final_img, "inflow": [qty_val], "outflow": [0]}
            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "SUCCESS", "action": f"Produk baru: {item_name} ditambahkan ke {target_rak}"})
            st.rerun()

    if st.session_state.app_tier in ["Premium", "Pro"]:
        with st.sidebar.expander("⚡ Flash Sale Massal", expanded=False):
            disc_percent = st.slider("Diskon Semua Produk (%)", 5, 50, 15, 5)
            duration_sec = st.selectbox("Durasi (Detik)", [15, 30, 60, 120])
            
            if not st.session_state.flash_sale_active:
                if st.button("🚀 Eksekusi Flash Sale"):
                    st.session_state.original_prices = {r: d["price"] for r, d in st.session_state.inventory.items()}
                    for r in st.session_state.inventory:
                        st.session_state.inventory[r]["price"] = int(st.session_state.inventory[r]["price"] * (1 - disc_percent / 100))
                    st.session_state.flash_sale_active = True
                    st.session_state.flash_sale_end = time.time() + duration_sec
                    st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "WARNING", "action": f"Flash Sale {disc_percent}% Dieksekusi."})
                    st.rerun()
            else:
                st.warning(f"⏳ Aktif! Sisa Waktu: {int(st.session_state.flash_sale_end - time.time())}s")
                if st.button("Batalkan Flash Sale"):
                    for r, op in st.session_state.original_prices.items():
                        if r in st.session_state.inventory: st.session_state.inventory[r]["price"] = op
                    st.session_state.flash_sale_active = False
                    st.session_state.original_prices = {}
                    st.rerun()
    else:
        st.sidebar.info("🔒 Fitur Flash Sale Massal eksklusif untuk Paket Premium & Pro.")
else:
    st.sidebar.info("ℹ️ Mode Staff: Anda masuk sebagai staf gudang. Hanya diizinkan untuk update stok.")

# ==========================================
# 6. HALAMAN DETAIL PRODUK
# ==========================================
if st.session_state.page == "detail":
    rak_key = st.session_state.selected_rak
    if rak_key not in st.session_state.inventory:
        st.session_state.page = "home"; st.rerun()
        
    prod = st.session_state.inventory[rak_key]
    
    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page = "home"; st.rerun()
        
    st.markdown(f"## 📊 Data Analitik: {rak_key}")
    dc1, dc2 = st.columns([1, 2])
    with dc1:
        st.image(prod.get("image"), use_container_width=True)
    with dc2:
        st.markdown(f"### {prod['item']}")
        st.write(f"📦 **Stok Tersedia:** {prod['qty']} Pcs")
        st.write(f"🏷️ **Harga Display IoT:** Rp {prod['price']:,}")
    
    st.divider()
    if st.session_state.app_tier in ["Premium", "Pro"]:
        st.subheader("📈 Analisis Arus Stok (Inflow vs Outflow)")
        st.line_chart({"Stok Masuk": prod.get("inflow"), "Stok Terjual": prod.get("outflow")})
    else:
        st.info("🔒 Grafik penjualan komprehensif tersedia di paket Premium & Pro.")
    st.stop()

# ==========================================
# 7. DASHBOARD UTAMA
# ==========================================

# EKSKLUSIF PRO: AI Smart Advisor
if st.session_state.app_tier == "Pro":
    low_stock = [k for k, v in st.session_state.inventory.items() if v['qty'] <= 5]
    if low_stock:
        ai_msg = f"⚠️ **AI ALERT:** Segera lakukan restock untuk <b>{', '.join(low_stock)}</b>. Algoritma memprediksi barang akan habis dalam 24 jam."
        bg_ai = "#fee2e2" if st.session_state.theme == "Light" else "rgba(239, 68, 68, 0.1)"
        border_ai = "#ef4444"
        text_ai = "#991b1b" if st.session_state.theme == "Light" else "#fca5a5"
    else:
        ai_msg = "✨ **AI INSIGHT:** Tingkat inventaris ideal. Berdasarkan tren historis, hari ini adalah waktu yang tepat untuk menjalankan Flash Sale 15%."
        bg_ai = "#dcfce7" if st.session_state.theme == "Light" else "rgba(34, 197, 94, 0.1)"
        border_ai = "#22c55e"
        text_ai = "#166534" if st.session_state.theme == "Light" else "#86efac"
        
    st.markdown(f"""
    <div style="background:{bg_ai}; border:1px solid {border_ai}; padding:18px 24px; border-radius:16px; margin-bottom:24px; color:{text_ai};">
        <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:24px;">🧠</span>
            <div>
                <strong style="font-size:16px; display:block; margin-bottom:4px; color:{text_ai};">Storify AI Advisor</strong>
                <span style="font-size:14px;">{ai_msg}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Filter & Search
fc1, fc2 = st.columns([2, 2])
with fc1:
    cats = ["Semua Kategori"] + list(set(d.get("category", "General") for d in st.session_state.inventory.values()))
    sel_cat = st.selectbox("Kategori Produk", cats)
with fc2:
    search_q = st.text_input("Pencarian Produk...", "", placeholder="Ketik nama atau rak...")

st.divider()

if not st.session_state.inventory:
    st.info("📦 Toko masih kosong. Silakan tambah produk melalui menu di sebelah kiri.")
else:
    for rak_id, data in st.session_state.inventory.items():
        if sel_cat != "Semua Kategori" and data.get("category", "General") != sel_cat: continue
        if search_q.lower() not in data["item"].lower() and search_q.lower() not in rak_id.lower(): continue
        
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        c_img, c1, c2, c3, c4 = st.columns([1, 2, 2, 2, 2])
        
        with c_img: 
            st.image(data.get("image"), use_container_width=True)
        with c1:
            st.markdown(f"<h4 style='margin-bottom:4px; color:{c_text};'>📍 {rak_id}</h4>", unsafe_allow_html=True)
            st.write(f"**{data['item']}**")
        with c2:
            st.write(f"📦 Stok: {data['qty']} Pcs")
            if data['qty'] <= 5: 
                st.markdown("<span style='color:#ef4444; font-weight:bold; background:rgba(239,68,68,0.1); padding:2px 8px; border-radius:8px;'>⚠️ Menipis</span>", unsafe_allow_html=True)
            else: 
                st.markdown("<span style='color:#10b981; font-weight:bold; background:rgba(16,185,129,0.1); padding:2px 8px; border-radius:8px;'>✔ Aman</span>", unsafe_allow_html=True)
        with c3:
            st.write("🏷️ Harga Aktif")
            st.markdown(f'<div class="price-tag">Rp {data["price"]:,}</div>', unsafe_allow_html=True)
        with c4:
            if st.button("🔍 Detail", key=f"det_{rak_id}", use_container_width=True):
                st.session_state.selected_rak = rak_id
                st.session_state.page = "detail"
                st.rerun()
                
            with st.popover("⚙️ Kelola", use_container_width=True):
                new_q = st.number_input(f"Stok Fisik", min_value=0, value=data["qty"], key=f"q_{rak_id}")
                if is_privileged:
                    new_p = st.number_input(f"Harga Baru (Rp)", min_value=0, value=int(data["price"]), step=500, key=f"p_{rak_id}")
                    if st.button("💾 Terapkan Perubahan", key=f"sv_{rak_id}", use_container_width=True):
                        st.session_state.inventory[rak_id]["qty"] = new_q
                        st.session_state.inventory[rak_id]["price"] = new_p
                        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": f"[{st.session_state.user['name']}] Update {rak_id} sukses."})
                        st.rerun()
                    st.divider()
                    if st.button("🗑️ Hapus", type="primary", key=f"del_{rak_id}", use_container_width=True):
                        del st.session_state.inventory[rak_id]
                        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "ERROR", "action": f"[{st.session_state.user['name']}] Menghapus rak {rak_id}."})
                        st.rerun()
                else:
                    if st.button("💾 Simpan Restock", key=f"sv_{rak_id}", use_container_width=True):
                        st.session_state.inventory[rak_id]["qty"] = new_q
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. TERMINAL AUDIT LOG (Premium & Pro)
# ==========================================
if st.session_state.app_tier in ["Premium", "Pro"]:
    st.divider()
    st.markdown(f"<h3 style='color:{c_text};'>📜 Terminal Audit Log (Keamanan)</h3>", unsafe_allow_html=True)
    if is_privileged:
        t_text = "".join([f"{l['time']} [{l.get('type', 'INFO'):<9}] >> {l['action']}\n" for l in st.session_state.logs[:15]])
        st.markdown(f'<div style="background:#020617; color:#38bdf8; padding:18px; border-radius:12px; font-family:monospace; font-size:13px; max-height:220px; overflow-y:auto; border:1px solid #1e293b;">{t_text}</div>', unsafe_allow_html=True)
    else:
        st.error("Akses Ditolak: Fitur Audit Log eksklusif untuk level Owner, Manager, dan Developer.")
