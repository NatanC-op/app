import streamlit as st
import time
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(page_title="Storify - Smart Label & Dynamic Pricing", layout="wide", page_icon="🏷️")

# ==========================================
# 2. INISIALISASI STATE (DATABASE SEMENTARA)
# ==========================================
if "app_tier" not in st.session_state:
    st.session_state.app_tier = None  # None = Halaman Landing Pemilihan Paket

if "store_name" not in st.session_state:
    st.session_state.store_name = "Storify - Cabang Utama"

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_rak" not in st.session_state:
    st.session_state.selected_rak = None

if "user" not in st.session_state:
    st.session_state.user = {"name": "Beatrix", "role": "OWNER", "email": "beatrix@storify.id"}

if "logs" not in st.session_state:
    st.session_state.logs = [{"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Storify Core System Initialized."}]

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
# 3. CSS KUSTOM RINGAN (Hanya untuk Badge, Tidak merusak Dark Mode)
# ==========================================
st.markdown("""
<style>
    .badge-pro { background: linear-gradient(90deg, #3b82f6, #8b5cf6); color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .badge-aman { background-color: rgba(16, 185, 129, 0.15); color: #10b981; padding: 4px 10px; border-radius: 8px; font-weight: bold; }
    .badge-bahaya { background-color: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 4px 10px; border-radius: 8px; font-weight: bold; }
    .price-text { color: #3b82f6; font-size: 24px; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. HALAMAN LANDING: PEMILIHAN PAKET SAAS
# ==========================================
if st.session_state.app_tier is None:
    st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>Pilih Paket Berlangganan Storify 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; opacity: 0.7; margin-bottom: 40px;'>Solusi manajemen harga dinamis dan stok retail untuk segala skala bisnis.</p>", unsafe_allow_html=True)
    
    # Toggle Siklus Tagihan
    col_t1, col_t2, col_t3 = st.columns([1, 2, 1])
    with col_t2:
        billing_cycle = st.radio("Pilih Siklus Tagihan:", ["Mingguan", "Bulanan", "Tahunan"], horizontal=True, label_visibility="collapsed")
    st.write("") # Spacer

    # Database Harga Sesuai Permintaan
    pricing = {
        "Standard": {"Mingguan": "35.000", "Bulanan": "125.000", "Tahunan": "1.400.000"},
        "Premium": {"Mingguan": "50.000", "Bulanan": "230.000", "Tahunan": "2.500.000"},
        "Pro": {"Mingguan": "100.000", "Bulanan": "350.000", "Tahunan": "4.000.000"}
    }
    sfx = {"Mingguan": "/ minggu", "Bulanan": "/ bulan", "Tahunan": "/ tahun"}[billing_cycle]

    # Kartu Paket Menggunakan Native Container (Anti Bug UI)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        with st.container(border=True):
            st.subheader("Standard")
            st.caption("Cocok untuk toko kecil & UMKM")
            st.markdown(f"<h1 style='color:#3b82f6;'>Rp {pricing['Standard'][billing_cycle]}<span style='font-size:16px; color:gray;'> {sfx}</span></h1>", unsafe_allow_html=True)
            st.divider()
            st.markdown("""
            - ✔️ Manajemen Stok & Rak Dasar
            - ✔️ Ubah Harga Manual E-Paper
            - ✔️ Manajemen Multi-User
            - ❌ *Flash Sale Massal Otomatis*
            - ❌ *Terminal Log Keamanan*
            - ❌ *AI Smart Advisor*
            """)
            st.write("")
            if st.button("Pilih Standard", use_container_width=True, key="p_std"):
                st.session_state.app_tier = "Standard"; st.rerun()

    with c2:
        with st.container(border=True):
            st.subheader("Premium")
            st.caption("Untuk minimarket berkembang")
            st.markdown(f"<h1 style='color:#3b82f6;'>Rp {pricing['Premium'][billing_cycle]}<span style='font-size:16px; color:gray;'> {sfx}</span></h1>", unsafe_allow_html=True)
            st.divider()
            st.markdown("""
            - ✔️ **Semua fitur Standard**
            - ✔️ **Flash Sale Massal Otomatis**
            - ✔️ **Terminal Audit Log Sistem**
            - ✔️ Laporan Grafik Interaktif
            - ❌ *AI Smart Advisor*
            - ❌ *Prediksi Restock AI*
            """)
            st.write("")
            if st.button("Pilih Premium", use_container_width=True, key="p_prm"):
                st.session_state.app_tier = "Premium"; st.rerun()

    with c3:
        with st.container(border=True):
            st.markdown("<span class='badge-pro'>🌟 PALING POPULER & CANGGIH</span>", unsafe_allow_html=True)
            st.subheader("Pro (Enterprise)")
            st.caption("Manajemen skala besar bertenaga AI")
            st.markdown(f"<h1 style='color:#8b5cf6;'>Rp {pricing['Pro'][billing_cycle]}<span style='font-size:16px; color:gray;'> {sfx}</span></h1>", unsafe_allow_html=True)
            st.divider()
            st.markdown("""
            - ✔️ **Semua fitur Premium**
            - ✔️ **AI Smart Advisor (Asisten AI)**
            - ✔️ **Prediksi Restock Otomatis**
            - ✔️ Prioritas Sinkronisasi E-Paper
            - ✔️ Kustomisasi Akses Penuh
            """)
            st.write("")
            if st.button("Pilih Pro", type="primary", use_container_width=True, key="p_pro"):
                st.session_state.app_tier = "Pro"; st.rerun()
                
    st.stop() # Hentikan rendering aplikasi utama sebelum paket dipilih

# ==========================================
# 5. APLIKASI UTAMA STORIFY (DASHBOARD)
# ==========================================

# Sistem Auto-Restore Harga Flash Sale
if st.session_state.flash_sale_active and time.time() > st.session_state.flash_sale_end:
    for rak, orig_p in st.session_state.original_prices.items():
        if rak in st.session_state.inventory:
            st.session_state.inventory[rak]["price"] = orig_p
    st.session_state.flash_sale_active = False
    st.session_state.original_prices = {}
    st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Waktu Flash Sale habis. Harga dikembalikan normal."})

# HEADER DASHBOARD UTAMA
col_title, col_info = st.columns([3, 1])
with col_title:
    st.title(f"🏷️ {st.session_state.store_name}")
    st.caption("Solusi Retail Phygital Modern & Dynamic Pricing Terintegrasi")
with col_info:
    tier_color = "normal" if st.session_state.app_tier == "Standard" else ("primary" if st.session_state.app_tier == "Premium" else "error")
    st.info(f"**Paket Aktif:** STORIFY {st.session_state.app_tier.upper()}")

# ==========================================
# 6. SIDEBAR - PANEL KONTROL
# ==========================================
with st.sidebar:
    st.header("⚙️ Control Panel")
    
    with st.container(border=True):
        st.markdown(f"**👤 {st.session_state.user['name']}**")
        st.caption(f"Role: {st.session_state.user['role']} | {st.session_state.user['email']}")
    
    with st.expander("👤 Ganti Akun Karyawan"):
        acc = st.selectbox("Pilih Akun:", ["Beatrix (Owner)", "Natannael (Developer)", "Walden (Developer)", "Nathalee (Staff Gudang)"])
        if "Beatrix" in acc: st.session_state.user = {"name": "Beatrix", "role": "OWNER", "email": "beatrix@storify.id"}
        elif "Natannael" in acc: st.session_state.user = {"name": "Natannael", "role": "DEVELOPER", "email": "natannael@storify.id"}
        elif "Walden" in acc: st.session_state.user = {"name": "Walden", "role": "DEVELOPER", "email": "walden@storify.id"}
        else: st.session_state.user = {"name": "Nathalee", "role": "STAFF", "email": "nathalee@storify.id"}
        if st.button("Masuk (Login)", use_container_width=True): st.rerun()

    with st.expander("🏪 Pengaturan Toko"):
        new_store_name = st.text_input("Nama Toko/Cabang", st.session_state.store_name)
        if st.button("Ubah Nama", use_container_width=True):
            st.session_state.store_name = new_store_name; st.rerun()
        st.divider()
        if st.button("🔄 Ganti Paket Fitur", use_container_width=True):
            st.session_state.app_tier = None; st.rerun()

    # HAK AKSES SISTEM
    is_privileged = st.session_state.user["role"] in ["OWNER", "DEVELOPER", "MANAGER"]

    if is_privileged:
        with st.expander("➕ Tambah Produk Baru"):
            target_rak = st.text_input("Kode Rak", "Rak E5")
            item_name = st.text_input("Nama Produk", "Cokelat Batang")
            
            img_source = st.radio("Sumber Foto Produk:", ["Upload Foto Lokal", "Gunakan Link URL"])
            final_img = "https://images.unsplash.com/photo-1542841791-1925b02a2bf5?w=300"
            
            if img_source == "Upload Foto Lokal":
                uploaded_file = st.file_uploader("Pilih File (JPG/PNG)", type=["png", "jpg", "jpeg"])
                if uploaded_file is not None:
                    import base64
                    base64_str = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
                    final_img = f"data:image/jpeg;base64,{base64_str}"
            else:
                url_input = st.text_input("Tempel URL Foto", final_img)
                if url_input: final_img = url_input
                
            qty_val = st.number_input("Stok Awal Fisik", min_value=0, value=25)
            price_val = st.number_input("Harga Label (Rp)", min_value=0, value=15000, step=500)
            
            if st.button("Simpan ke Database", type="primary", use_container_width=True):
                st.session_state.inventory[target_rak] = {"item": item_name, "category": "General", "qty": qty_val, "price": price_val, "image": final_img, "inflow": [qty_val], "outflow": [0]}
                st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "SUCCESS", "action": f"[{st.session_state.user['name']}] Menambah {item_name} di {target_rak}"})
                st.rerun()

        if st.session_state.app_tier in ["Premium", "Pro"]:
            with st.expander("⚡ Flash Sale Massal Otomatis"):
                disc_percent = st.slider("Besaran Diskon (%)", 5, 75, 20, 5)
                duration_sec = st.selectbox("Durasi (Detik)", [15, 30, 60, 120])
                
                if not st.session_state.flash_sale_active:
                    if st.button("🚀 Eksekusi Flash Sale", type="primary", use_container_width=True):
                        st.session_state.original_prices = {r: d["price"] for r, d in st.session_state.inventory.items()}
                        for r in st.session_state.inventory:
                            st.session_state.inventory[r]["price"] = int(st.session_state.inventory[r]["price"] * (1 - disc_percent / 100))
                        st.session_state.flash_sale_active = True
                        st.session_state.flash_sale_end = time.time() + duration_sec
                        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "WARNING", "action": f"[{st.session_state.user['name']}] Mengeksekusi Flash Sale {disc_percent}%"})
                        st.rerun()
                else:
                    st.warning(f"⏳ Flash Sale Berjalan! Sisa Waktu: {int(st.session_state.flash_sale_end - time.time())}s")
                    if st.button("Batalkan Flash Sale", use_container_width=True):
                        for r, op in st.session_state.original_prices.items():
                            if r in st.session_state.inventory: st.session_state.inventory[r]["price"] = op
                        st.session_state.flash_sale_active = False
                        st.session_state.original_prices = {}
                        st.rerun()
        else:
            st.info("🔒 Flash Sale Massal tersedia mulai dari paket Premium.")
    else:
        st.info("ℹ️ Anda login sebagai Staff. Hak akses dibatasi hanya untuk Restock barang.")

# ==========================================
# 7. ROUTING HALAMAN DETAIL PRODUK
# ==========================================
if st.session_state.page == "detail":
    rak_key = st.session_state.selected_rak
    if rak_key not in st.session_state.inventory:
        st.session_state.page = "home"; st.rerun()
        
    prod = st.session_state.inventory[rak_key]
    
    if st.button("⬅️ Kembali ke Menu Utama"):
        st.session_state.page = "home"; st.rerun()
        
    st.markdown(f"## 📊 Laporan Analitik: {rak_key}")
    with st.container(border=True):
        dc1, dc2 = st.columns([1, 3])
        with dc1:
            st.image(prod.get("image"), use_container_width=True)
        with dc2:
            st.markdown(f"### {prod['item']}")
            st.write(f"📦 **Stok Fisik Tersedia:** {prod['qty']} Pcs")
            st.write(f"🏷️ **Harga Sinkron E-Paper:** Rp {prod['price']:,}")
    
    if st.session_state.app_tier in ["Premium", "Pro"]:
        st.subheader("📈 Pergerakan Stok (Inflow vs Outflow)")
        st.line_chart({"Barang Masuk": prod.get("inflow"), "Barang Terjual": prod.get("outflow")})
    else:
        st.warning("🔒 Laporan Grafik Interaktif hanya tersedia di paket Premium & Pro.")
    st.stop()

# ==========================================
# 8. HALAMAN UTAMA (MONITORING RAK)
# ==========================================

# Fitur Eksklusif PRO: AI Smart Advisor
if st.session_state.app_tier == "Pro":
    low_stock = [k for k, v in st.session_state.inventory.items() if v['qty'] <= 5]
    if low_stock:
        st.error(f"🧠 **AI Advisor Alert:** Stok rak **{', '.join(low_stock)}** kritis! Segera hubungi supplier hari ini untuk menghindari kerugian stok kosong (Out-of-Stock Loss).", icon="⚠️")
    else:
        st.success("🧠 **AI Advisor Insight:** Distribusi stok optimal. Berdasarkan data cuaca hari ini, menaikkan sedikit harga produk minuman dingin berpotensi menaikkan margin 5%.", icon="✨")

# Search & Filter
f_col1, f_col2 = st.columns([1, 1])
with f_col1:
    cats = ["Tampilkan Semua Kategori"] + list(set(d.get("category", "General") for d in st.session_state.inventory.values()))
    sel_cat = st.selectbox("Kategori Produk", cats, label_visibility="collapsed")
with f_col2:
    search_q = st.text_input("Cari", "", placeholder="🔍 Ketik nama produk atau kode rak...", label_visibility="collapsed")

st.write("") # Spacer

if not st.session_state.inventory:
    st.info("📦 Toko masih kosong. Silakan tambah produk melalui menu di sebelah kiri.")
else:
    for rak_id, data in st.session_state.inventory.items():
        if sel_cat != "Tampilkan Semua Kategori" and data.get("category", "General") != sel_cat: continue
        if search_q.lower() not in data["item"].lower() and search_q.lower() not in rak_id.lower(): continue
        
        # Native Container Design (Responsif dan 100% Bebas Bug Warna)
        with st.container(border=True):
            col_img, col_info, col_stock, col_price, col_action = st.columns([1, 2, 2, 2, 2], vertical_alignment="center")
            
            with col_img: 
                st.image(data.get("image"), use_container_width=True)
            
            with col_info:
                st.markdown(f"#### 📍 {rak_id}")
                st.write(f"**{data['item']}**")
            
            with col_stock:
                st.write("📦 **Stok Tersedia**")
                st.write(f"{data['qty']} Pcs")
                if data['qty'] <= 5: 
                    st.markdown("<span class='badge-bahaya'>⚠️ Menipis</span>", unsafe_allow_html=True)
                else: 
                    st.markdown("<span class='badge-aman'>✔ Aman</span>", unsafe_allow_html=True)
            
            with col_price:
                st.write("🏷️ **Harga E-Paper**")
                st.markdown(f"<span class='price-text'>Rp {data['price']:,}</span>", unsafe_allow_html=True)
            
            with col_action:
                if st.button("🔍 Lihat Grafik", key=f"det_{rak_id}", use_container_width=True):
                    st.session_state.selected_rak = rak_id
                    st.session_state.page = "detail"
                    st.rerun()
                    
                with st.popover("⚙️ Kelola Barang", use_container_width=True):
                    new_q = st.number_input(f"Update Stok ({rak_id})", min_value=0, value=data["qty"], key=f"q_{rak_id}")
                    if is_privileged:
                        new_p = st.number_input(f"Update Harga (Rp)", min_value=0, value=int(data["price"]), step=1000, key=f"p_{rak_id}")
                        if st.button("💾 Simpan Perubahan", type="primary", key=f"sv_{rak_id}", use_container_width=True):
                            st.session_state.inventory[rak_id]["qty"] = new_q
                            st.session_state.inventory[rak_id]["price"] = new_p
                            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": f"[{st.session_state.user['name']}] Edit {rak_id}: Qty={new_q}, Harga={new_p}"})
                            st.rerun()
                        st.divider()
                        if st.button("🗑️ Hapus Rak Ini", key=f"del_{rak_id}", use_container_width=True):
                            del st.session_state.inventory[rak_id]
                            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "ERROR", "action": f"[{st.session_state.user['name']}] Menghapus data {rak_id}."})
                            st.rerun()
                    else:
                        if st.button("💾 Simpan Restock Fisik", type="primary", key=f"sv_{rak_id}", use_container_width=True):
                            st.session_state.inventory[rak_id]["qty"] = new_q
                            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": f"[{st.session_state.user['name']}] Update stok {rak_id} menjadi {new_q}"})
                            st.rerun()

# ==========================================
# 9. TERMINAL AUDIT LOG KEAMANAN
# ==========================================
if st.session_state.app_tier in ["Premium", "Pro"]:
    st.divider()
    st.subheader("📜 Terminal Audit Log Sistem")
    if is_privileged:
        with st.container(border=True):
            for log in st.session_state.logs[:10]:
                icon = "🟢" if log["type"] == "SUCCESS" else ("🔴" if log["type"] == "ERROR" else "🔵")
                st.text(f"{log['time']} {icon} [{log.get('type', 'INFO')}] >> {log['action']}")
    else:
        st.warning("🔒 Akses Ditolak: Fitur Audit Log eksklusif untuk tingkat Owner dan Developer.")
