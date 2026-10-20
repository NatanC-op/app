import streamlit as st
import pandas as pd
import time

# Set up halaman utama
st.set_page_config(page_title="IoT & AI Smart Shelf - Business Plan", layout="wide", page_icon="🛍️")

st.title("🛍️ IoT-Smart Shelf & AI Stock Synchronizer")
st.subheader("Dashboard Verifikasi & Monitoring Stok Real-time (SMA Business Plan Demo)")
st.caption("Prototipe Dummy: Integrasi Sensor Berat Rak & AI Camera Verifikator untuk Mencegah Human Error")

# --- DATABASE DUMMY (State Management agar interaktif) ---
if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "Rak A1 (Kopi)": {"barang_seharusnya": "Kopi Sachet", "berat_satuan": 100, "stok_tercatat": 15, "berat_sekarang": 1500, "status": "Aman", "detail": "Semua barang sesuai tempat."},
        "Rak B2 (Snack)": {"barang_seharusnya": "Keripik Singkong", "berat_satuan": 200, "stok_tercatat": 8, "berat_sekarang": 1600, "status": "Aman", "detail": "Semua barang sesuai tempat."},
        "Rak C3 (Minuman)": {"barang_seharusnya": "Air Mineral 600ml", "berat_satuan": 600, "stok_tercatat": 10, "berat_sekarang": 6000, "status": "Aman", "detail": "Semua barang sesuai tempat."},
    }

# --- BAGIAN SIMULATOR MASALAH (HUMAN ERROR) ---
st.sidebar.header("🛠️ Panel Simulator (Untuk Presentasi Juri)")
st.sidebar.write("Gunakan tombol ini untuk mensimulasikan masalah pembeli yang menaruh barang sembarangan.")

if st.sidebar.button("🚨 Simulasikan Pembeli Salah Taruh Barang"):
    # Pengunjung menaruh botol air mineral (600g) di rak Snack yang seharusnya berisi Keripik (200g)
    st.session_state.inventory["Rak B2 (Snack)"]["berat_sekarang"] = 2200 # 1600g (Keripik) + 600g (Air Mineral)
    st.session_state.inventory["Rak B2 (Snack)"]["status"] = "ERROR (Berat Tidak Cocok)"
    st.session_state.inventory["Rak B2 (Snack)"]["detail"] = "Anomali terdeteksi! Berat rak bertambah 600g, namun pola beban/dimensi tidak cocok dengan Keripik Singkong."
    st.sidebar.success("Masalah disimulasikan! Rak B2 sekarang mengalami anomali berat.")

if st.sidebar.button("🔄 Reset ke Kondisi Normal"):
    st.session_state.inventory["Rak B2 (Snack)"]["berat_sekarang"] = 1600
    st.session_state.inventory["Rak B2 (Snack)"]["status"] = "Aman"
    st.session_state.inventory["Rak B2 (Snack)"]["detail"] = "Semua barang sesuai tempat."
    st.sidebar.info("Dashboard dikembalikan ke kondisi normal.")

# --- BARIS 1: METRIKS UTAMA ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rak Terkoneksi", "3 Rak", "Aktif (IoT)")
with col2:
    st.metric("Kecepatan Update Sensor", "0.5 Detik", "Lokal Edge Connection")
with col3:
    # Cek apakah ada error
    error_count = sum(1 for item in st.session_state.inventory.values() if "ERROR" in item["status"])
    if error_count > 0:
        st.metric("Status Sistem", "PERLU PENGECEKAN", f"Ada {error_count} Anomali Rak!", delta_color="inverse")
    else:
        st.metric("Status Sistem", "KONDISI NORMAL", "0 Masalah")

st.write("---")

# --- BARIS 2: TABEL STATUS RAK (LIVE SENSOR) ---
st.subheader("📶 Live Status Rak Pintar (Data IoT Sensor)")

# Tampilkan data dengan gaya visually appealing
for rak, data in st.session_state.inventory.items():
    col_status, col_det = st.columns([1, 3])
    
    with col_status:
        if data["status"] == "Aman":
            st.success(f"🟢 **{rak}**")
            st.write(f"Barang: {data['barang_seharusnya']}")
            st.write(f"Estimasi Jumlah: {int(data['berat_sekarang']/data['berat_satuan'])} pcs")
        else:
            st.error(f"🚨 **{rak}**")
            st.write(f"Barang: {data['barang_seharusnya']}")
            st.write(f"**DATA ERROR!** Muatan Berlebih.")
            
    with col_det:
        st.info(f"**Data Berat Aktual:** {data['berat_sekarang']} gram (Berat Satuan Seharusnya: {data['berat_satuan']}g)")
        st.write(f"💬 *Keterangan:* {data['detail']}")
    st.write("")

st.write("---")

# --- BARIS 3: FITUR VERIFIKASI CAMERA AI (ANTI-HUMAN ERROR) ---
st.subheader("📷 Kamera AI Verifikator (Solusi Anti-Human Error)")
st.write("Ketika sensor IoT pada rak mendeteksi adanya kelebihan muatan/anomali, staf tidak perlu menghitung manual. Cukup arahkan Kamera Smartphone (AI) untuk melakukan kalibrasi instan.")

# Tombol untuk memicu pemindaian kamera
if st.button("🔍 Jalankan Verifikasi AI Camera (Scan Rak B2)"):
    if st.session_state.inventory["Rak B2 (Snack)"]["status"] == "ERROR (Berat Tidak Cocok)":
        with st.spinner("AI sedang menganalisis gambar rak..."):
            time.sleep(2) # Simulasi loading AI
            
        st.warning("🎯 **Hasil Analisis Kamera AI (Visual Object Detection):**")
        
        # Tampilan Simulasi AI
        st.image("https://via.placeholder.com/600x200/ff3333/ffffff?text=AI+DETECTION:+[1x+Botol+Air+Mineral]+Salah+Letak+di+Rak+Keripik!", use_container_width=True)
        
        st.write("""
        **🔍 Detail Temuan AI:**
        - **8x Keripik Singkong** (Terdeteksi Cocok - 1.600 gram)
        - **1x Air Mineral 600ml** (Terdeteksi SALAH LETAK - 600 gram) 🔴 *Penyebab Anomali*
        """)
        
        # Opsi Solusi Jasa/Sistem
        if st.button("✅ Konfirmasi & Pindahkan Barang (Selesaikan Error)"):
            st.session_state.inventory["Rak B2 (Snack)"]["berat_sekarang"] = 1600
            st.session_state.inventory["Rak B2 (Snack)"]["status"] = "Aman"
            st.session_state.inventory["Rak B2 (Snack)"]["detail"] = "Semua barang sesuai tempat (Telah dikalibrasi via AI Camera)."
            st.success("Sukses! Barang asing telah dipindahkan. Sensor rak kembali normal.")
            time.sleep(1)
            st.rerun()
            
    else:
        st.success("Semua rak dalam kondisi normal! Tidak diperlukan pemindaian AI saat ini.")

# Footer presentasi
st.write("---")
st.caption("Aplikasi dummy ini dirancang untuk demonstrasi fungsionalitas sistem Phygital (Hardware IoT + Software AI) dalam mengatasi Product Displacement Error.")
