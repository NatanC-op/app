import streamlit as st
import time

# Configuration
st.set_page_config(page_title="Smart Label & Stock Synchronizer", layout="wide", page_icon="🏷️")

# Inisialisasi Bahasa di Session State
if "lang" not in st.session_state:
    st.session_state.lang = "ID"

# ----------------- TERJEMAHAN KATA (DICTIONARY) -----------------
t = {
    "ID": {
        "title": "🏷️ Smart Label & Stock Synchronizer",
        "caption": "Solusi Retail Modern: Sinkronisasi Stok Otomatis & Dynamic Pricing via Smart Label",
        "sidebar_title": "⚙️ Panel Simulasi & Kontrol",
        "btn_sim_error": "🚨 Simulasikan Salah Taruh (Rak B2)",
        "btn_reset": "🔄 Reset Sistem",
        "lang_label": "Pilih Bahasa / Language",
        "m1": "Status Sistem", "m1_sub": "Online",
        "m2": "Total Produk", "m2_sub": "3 Rak Aktif",
        "m3": "Status Rak", "m3_sub": "Rak Aman",
        "m4": "Promo Aktif", "m4_sub": "2 Barang",
        "section_shelf": "📦 Live Monitoring Rak & Smart Label",
        "weight_label": "Stok Aktual",
        "price_label": "Harga Label (E-Paper)",
        "btn_edit_price": "✏️ Ubah Harga",
        "status_ok": "NORMAL",
        "status_err": "ANOMALI / SALAH TARUH",
        "section_ai": "📷 Verifikasi Kamera & AI Vision",
        "btn_scan": "🔍 Jalankan AI Scanner (Cek Rak B2)",
        "scan_loading": "AI sedang memindai rak via Computer Vision...",
        "ai_result": "🎯 Hasil Analisis AI:",
        "btn_resolve": "✅ Selesaikan & Sinkronkan Stok",
        "resolved_msg": "Rak B2 berhasil disinkronkan kembali!",
        "normal_msg": "Semua rak dalam kondisi normal.",
        "modal_title": "Ubah Harga Smart Label",
        "save_price": "Simpan Harga Baru"
    },
    "EN": {
        "title": "🏷️ Smart Label & Stock Synchronizer",
        "caption": "Modern Retail Solution: Automated Stock Sync & Dynamic Pricing via Smart Labels",
        "sidebar_title": "⚙️ Simulation & Control Panel",
        "btn_sim_error": "🚨 Simulate Misplacement (Shelf B2)",
        "btn_reset": "🔄 Reset System",
        "lang_label": "Select Language",
        "m1": "System Status", "m1_sub": "Online",
        "m2": "Total Products", "m2_sub": "3 Active Shelves",
        "m3": "Shelf Status", "m3_sub": "All Clear",
        "m4": "Active Promos", "m4_sub": "2 Items",
        "section_shelf": "📦 Live Shelf Monitoring & Smart Labels",
        "weight_label": "Actual Stock",
        "price_label": "Smart Label Price",
        "btn_edit_price": "✏️ Change Price",
        "status_ok": "NORMAL",
        "status_err": "ANOMALY / MISPLACED",
        "section_ai": "📷 AI Camera Verification",
        "btn_scan": "🔍 Run AI Scanner (Check Shelf B2)",
        "scan_loading": "AI is analyzing the shelf via Computer Vision...",
        "ai_result": "🎯 AI Analysis Result:",
        "btn_resolve": "✅ Resolve & Sync Stock",
        "resolved_msg": "Shelf B2 successfully synchronized!",
        "normal_msg": "All shelves are in normal condition.",
        "modal_title": "Update Smart Label Price",
        "save_price": "Save New Price"
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
    .badge-error {
        background-color: #ef4444; color: white; padding: 6px 12px;
        border-radius: 6px; font-weight: bold; font-size: 13px; display: inline-block;
    }
    .price-tag {
        font-size: 18px; font-weight: bold; color: #1e293b;
        background: #f1f5f9; padding: 6px 12px; border-radius: 8px; display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# State Management (Data Produk & Harga)
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rak A1 (Kopi)": {"item": "Kopi Sachet 25g", "qty": 20, "price": 15000, "status": "OK", "note": "Normal"},
        "Rak B2 (Snack)": {"item": "Keripik Singkong 100g", "qty": 10, "price": 12000, "status": "OK", "note": "Normal"},
        "Rak C3 (Minuman)": {"item": "Air Mineral 600ml", "qty": 5, "price": 5000, "status": "OK", "note": "Normal"},
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

# Sidebar Panel Simulasi
st.sidebar.header(t[lang]["sidebar_title"])
if st.sidebar.button(t[lang]["btn_sim_error"]):
    st.session_state.inventory["Rak B2 (Snack)"]["status"] = "ERROR"
    st.session_state.inventory["Rak B2 (Snack)"]["note"] = "Salah Taruh Barang Terdeteksi"
    st.sidebar.error("Simulasi anomali diaktifkan!")

if st.sidebar.button(t[lang]["btn_reset"]):
    st.session_state.inventory["Rak B2 (Snack)"]["status"] = "OK"
    st.session_state.inventory["Rak B2 (Snack)"]["note"] = "Normal"
    st.sidebar.info("Sistem di-reset.")

# Ringkasan Metrik Atas
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cloud Sync", t[lang]["m1_sub"], "Wi-Fi Active")
c2.metric(t[lang]["m2"], "3 Item", t[lang]["m2_sub"])
errors = sum(1 for v in st.session_state.inventory.values() if v["status"] == "ERROR")
c3.metric(t[lang]["m3"], f"{errors} Isu" if errors > 0 else "Aman", t[lang]["m3_sub"])
c4.metric(t[lang]["m4"], "2 Item", "Auto-Pricing")

st.divider()

# Live Monitoring Shelf & Smart Label
st.subheader(t[lang]["section_shelf"])

for rak_id, data in st.session_state.inventory.items():
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            st.markdown(f"### 📍 {rak_id}")
            st.write(f"**Produk:** {data['item']}")
            
        with col2:
            st.write(f"📦 **{t[lang]['weight_label']}:** {data['qty']} Pcs")
            st.caption(f"Catatan: {data['note']}")
            
        with col3:
            st.write(f"🏷️ **{t[lang]['price_label']}**")
            st.markdown(f'<div class="price-tag">Rp {data["price"]:,}</div>', unsafe_allow_html=True)
            
        with col4:
            st.write("")
            status = data["status"]
            if status == "OK":
                st.markdown(f'<span class="badge-ok">{t[lang]["status_ok"]}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span class="badge-error">{t[lang]["status_err"]}</span>', unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# AI Camera Verification & Dynamic Pricing Section
st.subheader(t[lang]["section_ai"])

if st.button(t[lang]["btn_scan"], type="primary"):
    if st.session_state.inventory["Rak B2 (Snack)"]["status"] == "ERROR":
        with st.spinner(t[lang]["scan_loading"]):
            time.sleep(1.2)
        st.warning(t[lang]["ai_result"])
        st.json({
            "detected_stock": "Keripik Singkong + 1 Barang Asing",
            "smart_label_sync": "Otomatis memperbarui harga & stok di E-Paper Display."
        })
        if st.button(t[lang]["btn_resolve"]):
            st.session_state.inventory["Rak B2 (Snack)"]["status"] = "OK"
            st.session_state.inventory["Rak B2 (Snack)"]["note"] = "Normal (Disinkronkan via AI)"
            st.success(t[lang]["resolved_msg"])
            time.sleep(0.8)
            st.rerun()
    else:
        st.info(t[lang]["normal_msg"])

# Fitur Ubah Harga Cepat untuk Smart Label
with st.expander("⚙️ Pengaturan Ubah Harga Smart Label (Dynamic Pricing)"):
    selected_rak = st.selectbox("Pilih Rak / Produk", list(st.session_state.inventory.keys()))
    new_price = st.number_input("Harga Baru (Rp)", min_value=1000, step=500, value=st.session_state.inventory[selected_rak]["price"])
    if st.button("Perbarui Harga Smart Label"):
        st.session_state.inventory[selected_rak]["price"] = new_price
        st.success(f"Harga untuk {selected_rak} berhasil diubah secara real-time ke perangkat Smart Label!")
        time.sleep(1)
        st.rerun()
