import streamlit as st
import time
from datetime import datetime

# Configuration
st.set_page_config(page_title="Smart Label & Dynamic Pricing", layout="wide", page_icon="🏷️")

# Inisialisasi State (Bahasa, Inventory, dan Activity Log)
if "lang" not in st.session_state:
    st.session_state.lang = "ID"

if "logs" not in st.session_state:
    st.session_state.logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "action": "Sistem diinisialisasi dan terhubung ke E-Paper cloud."}
    ]

# ----------------- TERJEMAHAN KATA (DICTIONARY) -----------------
t = {
    "ID": {
        "title": "🏷️ Smart Label & Dynamic Pricing",
        "caption": "Solusi Retail Modern: Manajemen Kategori, Log Aktivitas, & Smart Label Analytics",
        "sidebar_title": "⚙️ Pengaturan & Kontrol Toko",
        "lang_label": "Pilih Bahasa / Language",
        "section_shelf": "📦 Live Monitoring Rak & Smart Label",
        "section_log": "📜 Log Aktivitas Sistem (Audit Trail)",
        "weight_label": "Stok Aktual",
        "price_label": "Harga Label (E-Paper)",
        "cat_label": "Kategori Produk",
        "all_cat": "Semua Kategori",
    },
    "EN": {
        "title": "🏷️ Smart Label & Dynamic Pricing",
        "caption": "Modern Retail Solution: Category Management, Audit Trail, & Smart Label Analytics",
        "sidebar_title": "⚙️ Store Settings & Control",
        "lang_label": "Select Language",
        "section_shelf": "📦 Live Shelf Monitoring & Smart Labels",
        "section_log": "📜 System Audit Trail & Activity Log",
        "weight_label": "Actual Stock",
        "price_label": "Smart Label Price",
        "cat_label": "Product Category",
        "all_cat": "All Categories",
    }
}

lang = st.session_state.lang

# Custom CSS styling
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e3e6f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    .price-tag {
        font-size: 18px; font-weight: bold; color: #1e293b;
        background: #f1f5f9; padding: 6px 12px; border-radius: 8px; display: inline-block;
    }
    .log-box {
        background-color: #1e293b; color: #f8f9fa; padding: 15px;
        border-radius: 8px; font-family: monospace; font-size: 13px; max-height: 200px; overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# State Management (Data Produk dengan Kategori)
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rak A1": {"item": "Kopi Sachet 25g", "category": "Makanan & Minuman", "qty": 20, "price": 15000},
        "Rak B2": {"item": "Keripik Singkong 100g", "category": "Makanan & Minuman", "qty": 4, "price": 12000},
        "Rak C3": {"item": "Air Mineral 600ml", "category": "Makanan & Minuman", "qty": 15, "price": 5000},
        "Rak D4": {"item": "Deterjen Bubuk 800g", "category": "Kebutuhan Rumah Tangga", "qty": 8, "price": 25000},
    }

# Header & Pilihan Bahasa
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.title(t[lang]["title"])
    st.caption(t[lang]["caption"])
with col_head2:
    selected_lang = st.selectbox(t[lang]["lang_label"], ["ID", "EN"], index=0 if lang=="ID" else 1)
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

# Sidebar: Manajemen Produk, Kategori, & Diskon
st.sidebar.header(t[lang]["sidebar_title"])

with st.sidebar.expander("➕ Tambah / Edit Produk & Kategori", expanded=False):
    target_rak = st.text_input("Kode Rak (Cth: Rak E5)", "Rak E5")
    item_name = st.text_input("Nama Produk", "Sabun Mandi 100g")
    category_name = st.selectbox("Kategori", ["Makanan & Minuman", "Kebutuhan Rumah Tangga", "Elektronik", "Perawatan Tubuh"])
    qty_val = st.number_input("Jumlah Stok", min_value=0, value=12, step=1)
    price_val = st.number_input("Harga (Rp)", min_value=0, value=10000, step=500)
    
    if st.button("Simpan Produk"):
        st.session_state.inventory[target_rak] = {
            "item": item_name, "category": category_name, "qty": qty_val, "price": price_val
        }
        # Tambah ke log
        current_time = datetime.now().strftime("%H:%M:%S")
        st.session_state.logs.insert(0, {"time": current_time, "action": f"Produk baru ditambahkan: {item_name} di {target_rak}"})
        st.sidebar.success(f"Data {target_rak} berhasil disimpan!")
        time.sleep(0.5)
        st.rerun()

with st.sidebar.expander("⚡ Diskon Massal (Flash Sale)", expanded=False):
    disc_percent = st.slider("Potongan Diskon (%)", min_value=5, max_value=50, value=10, step=5)
    if st.button("Terapkan Diskon Massal"):
        for rak in st.session_state.inventory:
            st.session_state.inventory[rak]["price"] = int(st.session_state.inventory[rak]["price"] * (1 - disc_percent / 100))
        current_time = datetime.now().strftime("%H:%M:%S")
        st.session_state.logs.insert(0, {"time": current_time, "action": f"Diskon massal {disc_percent}% diterapkan ke seluruh produk."})
        st.sidebar.success(f"Diskon {disc_percent}% diterapkan!")
        time.sleep(0.5)
        st.rerun()

# Filter Berdasarkan Kategori di Halaman Utama
categories = [t[lang]["all_cat"]] + list(set(d["category"] for d in st.session_state.inventory.values()))
selected_category = st.selectbox(t[lang]["cat_label"], categories)

st.divider()

# Live Monitoring Shelf & Smart Label
st.subheader(t[lang]["section_shelf"])

filtered_inventory = {k: v for k, v in st.session_state.inventory.items() if selected_category == t[lang]["all_cat"] or v["category"] == selected_category}

if not filtered_inventory:
    st.info("Tidak ada produk dalam kategori ini.")
else:
    for rak_id, data in filtered_inventory.items():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                st.markdown(f"### 📍 {rak_id}")
                st.write(f"**Produk:** {data['item']}")
                st.caption(f"📂 Kategori: {data['category']}")
                
            with col2:
                st.write(f"📦 **{t[lang]['weight_label']}:** {data['qty']} Pcs")
                if data['qty'] <= 5:
                    st.warning("⚠️ Stok Menipis!")
                else:
                    st.success("Normal")
                
            with col3:
                st.write(f"🏷️ **{t[lang]['price_label']}**")
                st.markdown(f'<div class="price-tag">Rp {data["price"]:,}</div>', unsafe_allow_html=True)
                
            with col4:
                st.write("")
                if st.button("➕ Restock", key=f"rest_ {rak_id}"):
                    st.session_state.inventory[rak_id]["qty"] += 10
                    current_time = datetime.now().strftime("%H:%M:%S")
                    st.session_state.logs.insert(0, {"time": current_time, "action": f"Restock +10 pcs untuk {data['item']} ({rak_id})"})
                    st.rerun()
                    
            st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# Bagian Log Aktivitas Sistem (Audit Trail)
st.subheader(t[lang]["section_log"])
log_text = ""
for log in st.session_state.logs[:10]: # Tampilkan 10 log terbaru
    log_text += f"[{log['time']}] {log['action']}\n"

st.markdown(f'<div class="log-box">{log_text}</div>', unsafe_allow_html=True)
