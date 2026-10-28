import streamlit as st
import time
from datetime import datetime

# Configuration
st.set_page_config(page_title="Smart Label & Dynamic Pricing", layout="wide", page_icon="🏷️")

# Inisialisasi State
if "lang" not in st.session_state:
    st.session_state.lang = "ID"

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "page" not in st.session_state:
    st.session_state.page = "home"  # Pilihan: 'home' atau 'detail'

if "selected_rak" not in st.session_state:
    st.session_state.selected_rak = None

if "logs" not in st.session_state:
    st.session_state.logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Sistem IoT & E-Paper Cloud berhasil diinisialisasi."}
    ]

if "original_prices" not in st.session_state:
    st.session_state.original_prices = {}

if "flash_sale_active" not in st.session_state:
    st.session_state.flash_sale_active = False

if "flash_sale_end" not in st.session_state:
    st.session_state.flash_sale_end = 0.0

# ----------------- TERJEMAHAN KATA (DICTIONARY) -----------------
t = {
    "ID": {
        "title": "🏷️ Smart Label & Dynamic Pricing",
        "caption": "Solusi Retail Phygital Modern: Manajemen Harga Otomatis & E-Paper IoT Dashboard",
        "sidebar_title": "⚙️ Panel Kontrol & Pengaturan",
        "lang_label": "Pilih Bahasa / Language",
        "theme_label": "Mode Tampilan",
        "section_shelf": "📦 Live Monitoring Rak & Smart Label",
        "section_log": "📜 Terminal Log Aktivitas Sistem (Audit Trail)",
        "weight_label": "Stok Aktual",
        "price_label": "Harga E-Paper",
        "cat_label": "Filter Kategori",
        "all_cat": "Semua Kategori",
        "search_label": "Cari Produk...",
        "guide_title": "ℹ️ Panduan Presentasi & Cara Pakai Aplikasi",
        "btn_back": "⬅️ Kembali ke Beranda",
    },
    "EN": {
        "title": "🏷️ Smart Label & Dynamic Pricing",
        "caption": "Modern Phygital Retail Solution: Automated Pricing & E-Paper IoT Dashboard",
        "sidebar_title": "⚙️ Control Panel & Settings",
        "lang_label": "Language",
        "theme_label": "Theme Mode",
        "section_shelf": "📦 Live Shelf Monitoring & Smart Labels",
        "section_log": "📜 System Audit Trail Terminal",
        "weight_label": "Actual Stock",
        "price_label": "E-Paper Price",
        "cat_label": "Filter Category",
        "all_cat": "All Categories",
        "search_label": "Search products...",
        "guide_title": "ℹ️ Presentation Guide & How to Use",
        "btn_back": "⬅️ Back to Dashboard",
    }
}

lang = st.session_state.lang
theme = st.session_state.theme

# Dynamic CSS Styling berdasarkan Theme (Light / Dark)
if theme == "Dark":
    bg_color = "#0f172a"
    card_bg = "#1e293b"
    text_color = "#f8f9fa"
    border_color = "#334155"
    price_bg = "#090d16"
else:
    bg_color = "#f8f9fa"
    card_bg = "#ffffff"
    text_color = "#1e293b"
    border_color = "#e3e6f0"
    price_bg = "#f1f5f9"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    .card {{
        background-color: {card_bg};
        padding: 18px;
        border-radius: 14px;
        border: 1px solid {border_color};
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        margin-bottom: 15px;
    }}
    .price-tag {{
        font-size: 18px; font-weight: bold; color: #3b82f6;
        background: {price_bg}; padding: 6px 12px; border-radius: 8px; display: inline-block;
    }}
    .log-terminal {{
        background-color: #090d16; color: #38bdf8; padding: 15px;
        border-radius: 10px; font-family: monospace; font-size: 13px; max-height: 200px; overflow-y: auto;
        border: 1px solid #1e293b;
    }}
</style>
""", unsafe_allow_html=True)

# State Management Default Inventory (Dilengkapi URL Gambar & Grafik Keluar Masuk)
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rak A1": {
            "item": "Kopi Sachet 25g", 
            "category": "Makanan & Minuman", 
            "qty": 20, 
            "price": 15000,
            "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300",
            "inflow": [5, 10, 15, 20],
            "outflow": [3, 8, 12, 18]
        },
        "Rak B2": {
            "item": "Keripik Singkong 100g", 
            "category": "Makanan & Minuman", 
            "qty": 4, 
            "price": 12000,
            "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300",
            "inflow": [2, 5, 8, 10],
            "outflow": [4, 7, 9, 14]
        },
        "Rak C3": {
            "item": "Air Mineral 600ml", 
            "category": "Makanan & Minuman", 
            "qty": 15, 
            "price": 5000,
            "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300",
            "inflow": [10, 20, 25, 30],
            "outflow": [8, 15, 22, 25]
        },
        "Rak D4": {
            "item": "Deterjen Bubuk 800g", 
            "category": "Kebutuhan Rumah Tangga", 
            "qty": 8, 
            "price": 25000,
            "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300",
            "inflow": [3, 6, 9, 12],
            "outflow": [2, 5, 7, 10]
        },
    }

# Cek Timer Flash Sale otomatis habis
current_time_epoch = time.time()
if st.session_state.flash_sale_active and current_time_epoch > st.session_state.flash_sale_end:
    for rak, orig_p in st.session_state.original_prices.items():
        if rak in st.session_state.inventory:
            st.session_state.inventory[rak]["price"] = orig_p
    st.session_state.flash_sale_active = False
    st.session_state.original_prices = {}
    st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Waktu Flash Sale habis. Harga kembali normal."})

# Header & Kontrol Bahasa / Tema di Pojok Kanan
col_head1, col_head2 = st.columns([3, 2])
with col_head1:
    st.title(t[lang]["title"])
    st.caption(t[lang]["caption"])
with col_head2:
    sub_c1, sub_c2 = st.columns(2)
    with sub_c1:
        sel_lang = st.selectbox(t[lang]["lang_label"], ["ID", "EN"], index=0 if lang=="ID" else 1, label_visibility="collapsed")
        if sel_lang != st.session_state.lang:
            st.session_state.lang = sel_lang
            st.rerun()
    with sub_c2:
        sel_theme = st.selectbox(t[lang]["theme_label"], ["Light", "Dark"], index=0 if theme=="Light" else 1, label_visibility="collapsed")
        if sel_theme != st.session_state.theme:
            st.session_state.theme = sel_theme
            st.rerun()

# Sidebar Pengaturan
st.sidebar.header(t[lang]["sidebar_title"])

with st.sidebar.expander("➕ Tambah Produk dengan Foto", expanded=False):
    target_rak = st.text_input("Kode Rak (Cth: Rak E5)", "Rak E5")
    item_name = st.text_input("Nama Produk", "Sabun Mandi 100g")
    img_url = st.text_input("URL Foto Produk", "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300")
    
    existing_categories = list(set(d.get("category", "Umum") for d in st.session_state.inventory.values()))
    cat_mode = st.radio("Tipe Kategori", ["Pilih Ada", "Buat Baru"])
    if cat_mode == "Pilih Ada":
        category_name = st.selectbox("Kategori", existing_categories if existing_categories else ["Umum"])
    else:
        category_name = st.text_input("Nama Kategori Baru", "Perawatan Tubuh")
        
    qty_val = st.number_input("Jumlah Stok", min_value=0, value=15, step=1)
    price_val = st.number_input("Harga E-Paper (Rp)", min_value=0, value=12000, step=500)
    
    if st.button("Simpan Produk Baru"):
        if target_rak:
            st.session_state.inventory[target_rak] = {
                "item": item_name, 
                "category": category_name.strip() if category_name else "Umum", 
                "qty": qty_val, 
                "price": price_val,
                "image": img_url if img_url else "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300",
                "inflow": [5, 10],
                "outflow": [2, 4]
            }
            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "SUCCESS", "action": f"Produk baru ditambahkan: {item_name} di {target_rak}"})
            st.sidebar.success("Berhasil disimpan!")
            time.sleep(0.4)
            st.rerun()

with st.sidebar.expander("⚡ Timed Flash Sale (Diskon Massal)", expanded=False):
    disc_percent = st.slider("Besaran Diskon (%)", min_value=5, max_value=50, value=15, step=5)
    duration_sec = st.selectbox("Durasi Waktu", [15, 30, 60], format_func=lambda x: f"{x} Detik")
    
    if not st.session_state.flash_sale_active:
        if st.button("Jalankan Flash Sale"):
            st.session_state.original_prices = {r: d["price"] for r, d in st.session_state.inventory.items()}
            for r in st.session_state.inventory:
                st.session_state.inventory[r]["price"] = int(st.session_state.inventory[r]["price"] * (1 - disc_percent / 100))
            st.session_state.flash_sale_active = True
            st.session_state.flash_sale_end = time.time() + duration_sec
            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "WARNING", "action": f"Flash sale {disc_percent}% aktif selama {duration_sec} detik!"})
            st.rerun()
    else:
        rem = int(st.session_state.flash_sale_end - time.time())
        st.warning(f"Flash Sale Aktif! Sisa waktu: {max(0, rem)} detik")
        if st.button("Batalkan & Pulihkan Harga Normal"):
            for r, op in st.session_state.original_prices.items():
                if r in st.session_state.inventory:
                    st.session_state.inventory[r]["price"] = op
            st.session_state.flash_sale_active = False
            st.session_state.original_prices = {}
            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Flash sale dibatalkan manual."})
            st.rerun()

# =========================================================================
# HALAMAN 1: DETAIL PRODUK (KETIKA RAK DI-KLIK)
# =========================================================================
if st.session_state.page == "detail":
    rak_key = st.session_state.selected_rak
    if rak_key not in st.session_state.inventory:
        st.session_state.page = "home"
        st.rerun()
        
    prod = st.session_state.inventory[rak_key]
    
    if st.button(t[lang]["btn_back"]):
        st.session_state.page = "home"
        st.rerun()
        
    st.markdown(f"## 📊 Analitik & Detail Produk: {rak_key}")
    
    d_col1, d_col2 = st.columns([1, 2])
    with d_col1:
        st.image(prod.get("image", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300"), caption=prod["item"], use_container_width=True)
    with d_col2:
        st.markdown(f"### **{prod['item']}**")
        st.write(f"📂 **Kategori:** {prod.get('category', 'Umum')}")
        st.write(f"📦 **Stok Saat Ini:** {prod['qty']} Pcs")
        st.write(f"🏷️ **Harga E-Paper:** Rp {prod['price']:,}")
        
    st.divider()
    st.subheader("📈 Grafik Keluar Masuk Barang (Inflow vs Outflow)")
    
    chart_data = {
        "Barang Masuk (Inflow)": prod.get("inflow", [5, 10, 15, prod["qty"]]),
        "Barang Keluar (Outflow)": prod.get("outflow", [2, 5, 10, 12])
    }
    st.line_chart(chart_data)
    
    st.stop()  # Hentikan eksekusi agar halaman utama tidak ikut tampil

# =========================================================================
# HALAMAN 2: BERANDA / DASHBOARD UTAMA
# =========================================================================
with st.expander(t[lang]["guide_title"], expanded=False):
    st.markdown("""
    * **Klik Kartu/Tombol Detail:** Klik tombol `🔍 Lihat Detail & Grafik` pada produk untuk melihat grafik keluar-masuk barang secara mendetail.
    * **Foto Produk:** Setiap produk dilengkapi foto ilustrasi nyata.
    * **Tambah Produk & Foto:** Gunakan sidebar untuk mendaftarkan barang baru lengkap dengan URL gambarnya.
    """)

# Filter Kategori & Search Bar
filter_c1, filter_c2 = st.columns([2, 2])
with filter_c1:
    categories = [t[lang]["all_cat"]] + list(set(d.get("category", "Umum") for d in st.session_state.inventory.values()))
    selected_category = st.selectbox(t[lang]["cat_label"], categories)
with filter_c2:
    search_query = st.text_input(t[lang]["search_label"], "")

st.divider()

st.subheader(t[lang]["section_shelf"])

if not st.session_state.inventory:
    st.info("Belum ada produk terdaftar.")
else:
    filtered_inv = {}
    for k, v in st.session_state.inventory.items():
        match_cat = (selected_category == t[lang]["all_cat"] or v.get("category", "Umum") == selected_category)
        match_search = (search_query.lower() in v["item"].lower() or search_query.lower() in k.lower())
        if match_cat and match_search:
            filtered_inv[k] = v

    if not filtered_inv:
        st.warning("Produk tidak ditemukan.")
    else:
        for rak_id, data in filtered_inv.items():
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                col_img, col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 2, 1])
                
                with col_img:
                    st.image(data.get("image", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300"), use_container_width=True)
                    
                with col1:
                    st.markdown(f"### 📍 {rak_id}")
                    st.write(f"**{data['item']}**")
                    st.caption(f"📂 {data.get('category', 'Umum')}")
                    
                with col2:
                    st.write(f"📦 **{t[lang]['weight_label']}**: {data['qty']} Pcs")
                    if data['qty'] <= 5:
                        st.markdown("<span style='color: #ef4444; font-weight:bold;'>⚠️ Stok Menipis!</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color: #10b981; font-weight:bold;'>✔ Aman</span>", unsafe_allow_html=True)
                    
                with col3:
                    st.write(f"🏷️ **{t[lang]['price_label']}**")
                    st.markdown(f'<div class="price-tag">Rp {data["price"]:,}</div>', unsafe_allow_html=True)
                    
                with col4:
                    # Tombol Navigasi ke Halaman Detail (Klik Rak)
                    if st.button("🔍 Lihat Detail & Grafik", key=f"det_{rak_id}"):
                        st.session_state.selected_rak = rak_id
                        st.session_state.page = "detail"
                        st.rerun()
                        
                    restock_val = st.number_input(f"Restock", min_value=1, max_value=100, value=10, key=f"num_{rak_id}", label_visibility="collapsed")
                    if st.button("➕ Restock", key=f"rest_{rak_id}"):
                        st.session_state.inventory[rak_id]["qty"] += restock_val
                        st.session_state.inventory[rak_id]["outflow"].append(restock_val)
                        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "SUCCESS", "action": f"Restock +{restock_val} pcs untuk {data['item']} ({rak_id})"})
                        st.rerun()

                with col5:
                    st.write("")
                    if st.button("🗑️ Hapus", key=f"del_{rak_id}", type="secondary"):
                        del st.session_state.inventory[rak_id]
                        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "ERROR", "action": f"Produk pada {rak_id} dihapus."})
                        st.rerun()
                        
                st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ----------------- TERMINAL AUDIT LOG -----------------
st.subheader(t[lang]["section_log"])
terminal_text = ""
for log in st.session_state.logs[:12]:
    badge = f"[{log['type']}]"
    terminal_text += f"{log['time']} {badge:<9} >> {log['action']}\n"

st.markdown(f'<div class="log-terminal">{terminal_text}</div>', unsafe_allow_html=True)
