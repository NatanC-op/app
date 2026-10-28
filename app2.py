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
        font-size: 18px; font-weight:
