# ==========================================
# 3. HALAMAN AKTIVASI LISENSI PAKET
# ==========================================
if st.session_state.app_tier is None:
    _, _, col_t2 = st.columns([5, 1, 1.1])
    with col_t2:
        render_theme_toggle("license")

    st.markdown(f"""
    <div style='text-align: center; padding-top: 4px; margin-bottom: 24px;'>
        <span class='hero-pill'>🎟️ Portal Aktivasi Lisensi</span>
        <h1 style='font-size: 36px; margin: 4px 0;'>Aktivasi Paket <span class='gradient-title'>Storify</span></h1>
        <p style='color: {t['text_muted']}; font-size: 15px; max-width: 650px; margin: 0 auto;'>
            Semua paket bebas batasan jumlah rak & akun tim. Masukkan kode lisensi paket Anda untuk mengaktifkan sistem (min. 4 karakter).
        </p>
    </div>
    """, unsafe_allow_html=True)

    tiers_info = [
        (
            "Standard", "Operasional Toko Lengkap",
            "✔️ **Unlimited Rak & Unlimited Akun Tim**\n"
            "✔️ Update Harga & Stok Smart Label\n"
            "✔️ Kasir Cepat (-1 Terjual) & Export CSV\n"
            "✔️ Stock Opname / Cek Fisik Harian\n"
            "✔️ Absensi Karyawan & Jadwal Shift\n"
            "✔️ Notifikasi Restock & Chat Tim",
            "secondary"
        ),
        (
            "Premium", "Otomasi Promo & Profit",
            "✔️ **Semua Fitur Standard**\n"
            "✔️ **Kalkulator Harga & Margin Profit**\n"
            "✔️ **Bulk Edit Harga & Stok Massal**\n"
            "✔️ **Flash Sale Otomatis & Diskon Coret**\n"
            "✔️ **Tracker Kedaluwarsa (Expired Alert)**\n"
            "✔️ **Cetak Daftar Harga & Grafik Stok**",
            "secondary"
        ),
        (
            "Pro", "Prioritas & Multi-Cabang",
            "✔️ **Semua Fitur Premium**\n"
            "✔️ **Manajemen Multi-Cabang & Transfer Stok**\n"
            "✔️ **Ringkasan Perbandingan Semua Cabang**\n"
            "✔️ **Kustomisasi Tema Layar E-Paper**\n"
            "✔️ **LED Locator (Tes Kedip Label Rak)**\n"
            "✔️ **Handover Shift Terverifikasi & Priority Sync**",
            "primary"
        )
    ]

    cols = st.columns(3, gap="large")
    for idx, (name, sub, desc, btn_type) in enumerate(tiers_info):
        with cols[idx]:
            with st.container(border=True):
                if name == "Pro":
                    st.markdown("<span class='badge-pro'>⭐ PRIORITAS ENTERPRISE</span>", unsafe_allow_html=True)
                elif name == "Premium":
                    st.markdown("<span class='badge-prm'>POPULER</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='badge-std'>DASAR</span>", unsafe_allow_html=True)

                st.markdown(f"""
                <h3 style='margin: 12px 0 2px 0; font-size: 24px; color: {t['text_main']};'>{name}</h3>
                <p style='color: {t['text_muted']}; font-size: 13px; margin-bottom: 8px;'>{sub}</p>
                """, unsafe_allow_html=True)
                st.divider()
                st.markdown(desc)
                st.write("")
                code_in = st.text_input(f"Kode Lisensi {name}", placeholder=f"Contoh: STR-{name[:3].upper()}-8492", key=f"code_{name}")
                if st.button(f"Aktifkan {name}", type=btn_type, use_container_width=True, key=f"act_{name}"):
                    clean_code = code_in.strip()
                    if len(clean_code) >= 4:
                        st.session_state.app_tier = name
                        add_log("SUCCESS", f"Lisensi {name} diaktifkan (Kode: {clean_code})")
                        st.rerun()
                    else:
                        st.warning("Masukkan kode lisensi yang valid (minimal 4 karakter).")
    st.stop()
