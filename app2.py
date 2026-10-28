import streamlit as st
import time

# Configuration
st.set_page_config(page_title="Smart Label & Stock Management", layout="wide", page_icon="🏷️")

# Inisialisasi Bahasa di Session State
if "lang" not in st.session_state:
    st.session_state.lang = "ID"

# ----------------- TERJEMAHAN KATA (DICTIONARY) -----------------
t = {
    "ID": {
        "title": "🏷️ Smart Label & Stock Management",
        "caption": "Solusi Retail Modern: Manajemen Stok & Dynamic Pricing via Smart Label",
        "sidebar_title": "⚙️ Pengaturan & Manajemen Produk",
        "lang_label": "Pilih Bahasa / Language",
        "m1": "Status Sistem", "m1_sub": "Online",
        "m2": "Total Produk", "m2_sub": "Rak Aktif",
        "m3": "Status Rak", "m3_sub": "Semua Aman",
        "m4": "Auto-Pricing", "m4_sub": "Aktif",
        "section_shelf": "📦 Live Monitoring Rak & Smart Label",
        "weight_label": "Stok Aktual",
        "price_label": "Harga Label (E-Paper)",
        "status_ok": "NORMAL",
        "status_err": "PERHATIAN",
    },
    "EN": {
        "title": "🏷️ Smart Label & Stock Management",
        "caption": "Modern Retail Solution: Stock Management & Dynamic Pricing via Smart Labels",
        "sidebar_title": "⚙️ Product Settings & Management",
        "lang_label": "Select Language",
        "m1": "System Status", "m1_sub": "Online",
        "m2": "Total Products", "m2_sub": "Active Shelves",
        "m3": "Shelf Status", "m3_sub": "All Clear",
        "m4": "Auto-Pricing", "m4_sub": "Active",
        "section_shelf": "📦 Live Shelf Monitoring & Smart Labels",
        "weight_label": "Actual Stock",
        "price_label": "Smart Label Price",
        "status_ok": "NORMAL",
        "status_err": "ATTENTION",
    }
}

lang = st.session_state.lang

# Custom CSS styling untuk UI yang bersih & modern
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
    .badge-ok {
        background-color: #10b981; color: white; padding: 6px 12px;
        border-radius: 6px; font-weight: bold; font-size: 13px; display: inline-block;
    }
    .price-tag {
        font-size: 18px; font-weight: bold; color: #1e293b;
        background: #f1f5f9; padding: 6px 12px; border-radius: 8px; display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# State Management (Data Produk, Stok, & Harga)
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rak A1": {"item": "Kopi Sachet 25g", "qty": 20, "price": 15000, "status": "OK", "note": "Normal"},
        "Rak B2": {"item": "Keripik Singkong 100g", "qty": 10, "price": 12000, "status": "OK", "note": "Normal"},
        "Rak C3": {"item": "Air Mineral 600ml", "qty": 5, "price": 5000, "status": "OK", "note": "Normal"},
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

# Sidebar: Fitur Tambah / Edit / Rename Produk, Stok, dan Harga Langsung dari App
st.sidebar.header(t[lang]["sidebar_title"])

with st.sidebar.expander("➕ Tambah Rak / Produk Baru", expanded=False):
    new_rak_id = st.text_input("Nama/Kode Rak (Cth: Rak D4)", "Rak D4")
    new_item_name = st.text_input("Nama Produk", "Teh Botol 350ml")
    new_qty = st.number_input("Jumlah Stok", min_value=0, value=15, step=1)
    new_price = st.number_input("Harga (Rp)", min_value=0, value=4000, step=500)
    
    if st.button("Simpan Produk Baru"):
        if new_rak_id:
            st.session_state.inventory[new_rak_id] = {
                "item": new_item_name,
                "qty": new_qty,
                "price": new_price,
                "status": "OK",
                "note": "Baru ditambahkan"
            }
            st.sidebar.success(f"Rak {new_rak_id} berhasil ditambahkan!")
            time.sleep(0.5)
            st.rerun()

with st.sidebar.expander("✏️ Edit / Rename Produk & Harga", expanded=True):
    if st.session_state.inventory:
        target_rak = st.selectbox("Pilih Rak yang Ingin Diedit", list(st.session_state.inventory.keys()))
        
        current_data = st.session_state.inventory[target_rak]
        edited_item_name = st.text_input("Ubah Nama Produk", current_data["item"])
        edited_qty = st.number_input("Ubah Jumlah Stok", min_value=0, value=current_data["qty"], step=1)
        edited_price = st.number_input("Ubah Harga (Rp)", min_value=0, value=current_data["price"], step=500)
        
        if st.button("Perbarui Data Rak"):
            st.session_state.inventory[target_rak]["item"] = edited_item_name
            st.session_state.inventory[target_rak]["qty"] = edited_qty
            st.session_state.inventory[target_rak]["price"] = edited_price
            st.sidebar.success(f"Data {target_rak} berhasil diperbarui!")
            time.sleep(0.5)
            st.rerun()
            
        if st.button("🗑️ Hapus Rak Ini", type="secondary"):
            del st.session_state.inventory[target_rak]
            st.sidebar.warning(f"Rak {target_rak} telah dihapus.")
            time.sleep(0.5)
            st.rerun()
    else:
        st.sidebar.info("Belum ada data rak.")

# Ringkasan Metrik Atas
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cloud Sync", t[lang]["m1_sub"], "Active")
c2.metric(t[lang]["m2"], f"{len(st.session_state.inventory)} Rak", t[lang]["m2_sub"])
c3.metric(t[lang]["m3"], "Normal", t[lang]["m3_sub"])
c4.metric(t[lang]["m4"], "E-Paper Ready", "Sync OK")

st.divider()

# Live Monitoring Shelf & Smart Label
st.subheader(t[lang]["section_shelf"])

if not st.session_state.inventory:
    st.info("Belum ada rak/produk tersedia. Silakan tambahkan melalui sidebar di sebelah kiri.")
else:
    for rak_id, data in st.session_state.inventory.items():
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                st.markdown(f"### 📍 {rak_id}")
                st.write(f"**Produk:** {data['item']}")
                
            with col2:
                st.write(f"📦 **{t[lang]['weight_label']}:** {data['qty']} Pcs")
                st.caption(f"Status: {data['note']}")
                
            with col3:
                st.write(f"🏷️ **{t[lang]['price_label']}**")
                st.markdown(f'<div class="price-tag">Rp {data["price"]:,}</div>', unsafe_allow_html=True)
                
            with col4:
                st.write("")
                st.markdown(f'<span class="badge-ok">{t[lang]["status_ok"]}</span>', unsafe_allow_html=True)
                    
            st.markdown('</div>', unsafe_allow_html=True)
