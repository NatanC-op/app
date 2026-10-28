import streamlit as st
import time

# Konfigurasi halaman
st.set_page_config(page_title="Smart Shelf & AI Stock Synchronizer", layout="wide")

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
