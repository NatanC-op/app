import streamlit as st
import time

# Configuration
st.set_page_config(page_title="AI & IoT Smart Shelf - Phygital Demo", layout="wide", page_icon="📦")

# ---> TAMBAHKAN KODE CSS INI DI SINI <---
st.markdown("""
<style>
    /* Styling utama latar belakang agar lebih lembut */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Efek Card Interaktif dengan Hover */
    .interactive-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e3e6f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: all 0.3s ease;
        margin-bottom: 12px;
    }
    
    /* Saat kursor diarahkan ke kotak (hover) */
    .interactive-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
        border-color: #4e73df;
    }
    
    /* Styling Badge Status */
    .badge-ok {
        background-color: #1cc88a;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        font-size: 14px;
    }

    .badge-error {
        background-color: #e74a3b;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)
# Custom CSS styling (Di-wrap dengan benar)
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .badge-error {
        background-color: #ef4444;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    .badge-ok {
        background-color: #10b981;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# State Management
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rak A1 (Kopi)": {"item": "Kopi Sachet 25g", "unit_weight": 25, "expected_qty": 20, "current_weight": 500, "status": "OK", "log": "Normal"},
        "Rak B2 (Snack)": {"item": "Keripik Singkong 100g", "unit_weight": 100, "expected_qty": 10, "current_weight": 1000, "status": "OK", "log": "Normal"},
        "Rak C3 (Minuman)": {"item": "Air Mineral 600ml", "unit_weight": 600, "expected_qty": 5, "current_weight": 3000, "status": "OK", "log": "Normal"},
    }

st.title("📦 Smart Shelf & AI Stock Synchronizer")
st.caption("Phygital Retail Solution: Multi-Layer Verification (IoT Weight + AI Camera OCR)")

# Control Panel
st.sidebar.header("🛠️ Panel Simulasi Presentasi")
if st.sidebar.button("🚨 Simulasikan Salah Taruh Barang (Rak B2)"):
    # Pengunjung menaruh Air Mineral (600g) di Rak Snack (100g/unit)
    st.session_state.inventory["Rak B2 (Snack)"]["current_weight"] = 1600
    st.session_state.inventory["Rak B2 (Snack)"]["status"] = "ERROR"
    st.session_state.inventory["Rak B2 (Snack)"]["log"] = "Anomali: Berat berlebih +600g (Deteksi Asing)"
    st.sidebar.error("Anomali berhasil disimulasikan!")

if st.sidebar.button("🔄 Reset Sistem"):
    st.session_state.inventory["Rak B2 (Snack)"]["current_weight"] = 1000
    st.session_state.inventory["Rak B2 (Snack)"]["status"] = "OK"
    st.session_state.inventory["Rak B2 (Snack)"]["log"] = "Normal"
    st.sidebar.info("Sistem di-reset ke normal.")

# Realtime Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Status Koneksi IoT", "Terhubung", "ESP32 Wi-Fi")
c2.metric("Akurasi Sensor", "99.4%", "HX711 Load Cell")
errors = sum(1 for v in st.session_state.inventory.values() if v["status"] == "ERROR")
c3.metric("Anomali Rak", f"{errors} Rak", delta_color="inverse" if errors > 0 else "normal")
c4.metric("Prediksi Expiry", "2 Barang", "Perlu Promo")

st.divider()

# Live IoT Shelf Table
st.subheader("📡 Live Monitoring Sensor Berat (Load Cell)")

for rak_id, data in st.session_state.inventory.items():
    col1, col2, col3 = st.columns([2, 3, 2])
    with col1:
        st.write(f"**{rak_id}**")
        st.caption(f"Item: {data['item']}")
    with col2:
        st.write(f"Berat Berat Aktual: **{data['current_weight']}g** / Target: {data['unit_weight'] * data['expected_qty']}g")
        st.caption(f"Catatan: {data['log']}")
    with col3:
        if data["status"] == "OK":
            st.markdown('<span class="badge-ok">AMMAN (OK)</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-error">DISPLACEMENT ERROR</span>', unsafe_allow_html=True)
    st.write("---")

# AI Camera Verification
st.subheader("📷 Kalibrasi & Verifikasi Kamera AI")
if st.button("🔍 Jalankan Scanning Kamera AI (Verifikasi Rak B2)"):
    if st.session_state.inventory["Rak B2 (Snack)"]["status"] == "ERROR":
        with st.spinner("AI menganalisis gambar rak via Computer Vision..."):
            time.sleep(1.5)
        st.warning("🎯 **Hasil Analisis AI Object Detection:**")
        st.json({
            "detected_objects": [
                {"class": "Keripik Singkong", "count": 10, "confidence": "0.98"},
                {"class": "Air Mineral 600ml", "count": 1, "confidence": "0.95", "flag": "MISPLACED_ITEM"}
            ],
            "recommendation": "Pindahkan Air Mineral 600ml kembali ke Rak C3."
        })
        if st.button("✅ Selesaikan & Pindahkan Barang"):
            st.session_state.inventory["Rak B2 (Snack)"]["current_weight"] = 1000
            st.session_state.inventory["Rak B2 (Snack)"]["status"] = "OK"
            st.session_state.inventory["Rak B2 (Snack)"]["log"] = "Normal (Dikalibrasi via AI)"
            st.success("Rak B2 kembali normal!")
            time.sleep(1)
            st.rerun()
    else:
        st.info("Kondisi rak normal. Tidak ada anomali yang perlu diverifikasi.")
