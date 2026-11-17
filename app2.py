import streamlit as st
import pandas as pd
import base64
import time
from datetime import datetime

# ==========================================
# 1. KONFIGURASI & INISIALISASI STATE
# ==========================================
st.set_page_config(page_title="Storify - Smart Label & Retail OS", layout="wide", page_icon="🏷️")

defaults = {
    "logged_in": False,
    "app_tier": None,
    "store_name": "Storify - Cabang Utama",
    "page": "home",
    "selected_rak": None,
    "accounts": [
        {"name": "Beatrix", "role": "OWNER", "email": "beatrix@storify.id"},
        {"name": "Natannael", "role": "DEVELOPER", "email": "natannael@storify.id"},
        {"name": "Walden", "role": "DEVELOPER", "email": "walden@storify.id"},
        {"name": "Nathalee", "role": "STAFF", "email": "nathalee@storify.id"},
    ],
    "current_user_idx": 0,
    "logs": [{"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Sistem Storify & E-Paper Gateway aktif."}],
    "restock_requests": [
        {"id": 1, "rak": "Rak B2", "item": "Keripik Singkong 100g", "qty": 20, "by": "Nathalee", "note": "Stok sisa 4 pcs, ramai pembeli.", "status": "PENDING", "time": "09:15"}
    ],
    "team_chat": [
        {"sender": "Nathalee", "role": "STAFF", "msg": "Halo kak, Rak B2 keripik singkong sudah hampir habis ya.", "time": "09:16"},
        {"sender": "Beatrix", "role": "OWNER", "msg": "Oke siap, ajukan request restock saja biar langsung saya ACC.", "time": "09:18"}
    ],
    "original_prices": {},
    "flash_sale_active": False,
    "flash_sale_end": 0.0,
    "inventory": {
        "Rak A1": {"item": "Kopi Sachet 25g", "category": "Minuman", "qty": 20, "price": 15000, "battery": "98%", "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=300", "inflow": [10, 15, 20], "outflow": [5, 12, 18]},
        "Rak B2": {"item": "Keripik Singkong 100g", "category": "Makanan", "qty": 4, "price": 12000, "battery": "85%", "image": "https://images.unsplash.com/photo-1566478989037-eec170784d0b?w=300", "inflow": [5, 8, 10], "outflow": [4, 7, 14]},
        "Rak C3": {"item": "Air Mineral 600ml", "category": "Minuman", "qty": 15, "price": 5000, "battery": "92%", "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=300", "inflow": [15, 25, 30], "outflow": [10, 20, 25]},
        "Rak D4": {"item": "Deterjen Bubuk 800g", "category": "Rumah Tangga", "qty": 8, "price": 25000, "battery": "79%", "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=300", "inflow": [6, 9, 12], "outflow": [3, 7, 10]},
    }
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def add_log(log_type, msg):
    st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": log_type, "action": msg})

current_user = st.session_state.accounts[st.session_state.current_user_idx]
is_privileged = current_user["role"] in ["OWNER", "DEVELOPER", "MANAGER"]

# CSS Ringan (100% Kompatibel Light & Dark Mode)
st.markdown("""
<style>
    .badge-pro { background: linear-gradient(90deg, #3b82f6, #8b5cf6); color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; }
    .badge-ok { background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 3px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }
    .badge-low { background: rgba(239, 68, 68, 0.15); color: #ef4444; padding: 3px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; }
    .price-text { color: #3b82f6; font-size: 20px; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HALAMAN LOGIN DEMO
# ==========================================
if not st.session_state.logged_in:
    _, col_l, _ = st.columns([1, 1.4, 1])
    with col_l:
        st.markdown("<h1 style='text-align: center; margin-top: 30px;'>🏷️ Storify Cloud</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; opacity: 0.7;'>Portal Manajemen Smart Label & Operasional Ritel</p>", unsafe_allow_html=True)
        with st.container(border=True):
            email_in = st.text_input("Email Perusahaan", "beatrix@storify.id")
            pass_in = st.text_input("Password", type="password", value="demo123")
            if st.button("Masuk ke Sistem", type="primary", use_container_width=True):
                if email_in.strip() and pass_in.strip():
                    st.session_state.logged_in = True
                    st.session_state.accounts[0]["email"] = email_in.strip()
                    st.rerun()
                else:
                    st.error("Email dan password wajib diisi.")
    st.stop()

# ==========================================
# 3. HALAMAN AKTIVASI LISENSI
# ==========================================
if st.session_state.app_tier is None:
    st.markdown("<h2 style='text-align: center;'>Aktivasi Lisensi Perangkat & Aplikasi 🎟️</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7; margin-bottom: 25px;'>Masukkan kode lisensi paket Smart Label Anda (Demo: masukkan kode apa saja).</p>", unsafe_allow_html=True)
    
    tiers = [
        ("Standard", "Dasar Operasional", "✔️ Manajemen Stok & Rak\n✔️ Update Harga E-Paper\n✔️ Request Restock & Chat Tim\n❌ Flash Sale & AI Advisor", "secondary"),
        ("Premium", "Minimarket & Ritel", "✔️ Semua Fitur Standard\n✔️ Flash Sale Massal Otomatis\n✔️ Diskon Cepat & Audit Log\n❌ AI Smart Advisor", "secondary"),
        ("Pro", "Enterprise + AI", "✔️ Semua Fitur Premium\n✔️ AI Smart Advisor\n✔️ Prediksi Restock Otomatis\n✔️ Prioritas Sync E-Paper", "primary")
    ]
    
    cols = st.columns(3)
    for idx, (name, sub, desc, btn_type) in enumerate(tiers):
        with cols[idx]:
            with st.container(border=True):
                if name == "Pro":
                    st.markdown("<span class='badge-pro'>🌟 ENTERPRISE</span>", unsafe_allow_html=True)
                st.subheader(name)
                st.caption(sub)
                st.divider()
                st.markdown(desc)
                st.write("")
                code_in = st.text_input(f"Kode Lisensi {name}", placeholder="Contoh: STR-PRO-01", key=f"code_{name}")
                if st.button(f"Aktifkan {name}", type=btn_type, use_container_width=True, key=f"act_{name}"):
                    if code_in.strip():
                        st.session_state.app_tier = name
                        add_log("SUCCESS", f"Lisensi {name} aktif (Kode: {code_in.strip()})")
                        st.rerun()
                    else:
                        st.warning("Masukkan kode lisensi terlebih dahulu.")
    st.stop()

# ==========================================
# 4. AUTO-RESTORE FLASH SALE & HEADER
# ==========================================
if st.session_state.flash_sale_active and time.time() > st.session_state.flash_sale_end:
    for r, orig_p in st.session_state.original_prices.items():
        if r in st.session_state.inventory:
            st.session_state.inventory[r]["price"] = orig_p
    st.session_state.flash_sale_active = False
    st.session_state.original_prices = {}
    add_log("INFO", "Flash Sale selesai. Harga E-Paper kembali normal.")

pending_reqs = [req for req in st.session_state.restock_requests if req["status"] == "PENDING"]

c_head1, c_head2 = st.columns([3, 1.2], vertical_alignment="center")
with c_head1:
    st.title(f"🏷️ {st.session_state.store_name}")
    st.caption(f"Paket: **STORIFY {st.session_state.app_tier.upper()}** | Login: **{current_user['name']}** (`{current_user['role']}`)")
with c_head2:
    if st.button("📡 Sync Semua E-Paper", type="primary", use_container_width=True):
        with st.spinner("Mengirim sinyal ke Smart Label..."):
            time.sleep(0.5)
        add_log("SUCCESS", f"[{current_user['name']}] Sinkronisasi massal ke {len(st.session_state.inventory)} label selesai.")
        st.toast("Semua harga E-Paper berhasil diperbarui!", icon="✅")

# Notifikasi Global untuk Atasan jika ada Request Restock dari Staff
if is_privileged and pending_reqs:
    st.warning(f"🔔 **Notifikasi Gudang:** Ada **{len(pending_reqs)} permintaan restock baru** dari staff gudang yang menunggu persetujuan Anda! Cek tab **📩 Permintaan & Chat**.", icon="📢")

# ==========================================
# 5. SIDEBAR KONTROL RINGKAS
# ==========================================
with st.sidebar:
    st.header("⚙️ Panel Kontrol")
    with st.container(border=True):
        st.markdown(f"**👤 {current_user['name']}**")
        st.caption(f"Role: `{current_user['role']}` | {current_user['email']}")

    with st.expander("🔄 Ganti Akun Login", expanded=True):
        acc_labels = [f"{a['name']} ({a['role']})" for a in st.session_state.accounts]
        sel_idx = st.selectbox("Pilih Akun:", range(len(acc_labels)), index=st.session_state.current_user_idx, format_func=lambda x: acc_labels[x])
        if st.button("Masuk Sebagai Akun Ini", use_container_width=True):
            st.session_state.current_user_idx = sel_idx
            st.rerun()

    if is_privileged:
        with st.expander("➕ Tambah Produk & Label"):
            new_rak = st.text_input("Kode Rak", f"Rak E{len(st.session_state.inventory)+1}")
            new_item = st.text_input("Nama Produk", "Susu UHT 250ml")
            existing_cats = sorted(list(set(d["category"] for d in st.session_state.inventory.values())))
            cat_choice = st.selectbox("Kategori", existing_cats + ["+ Kategori Baru"])
            new_cat = st.text_input("Nama Kategori Baru", "Produk Susu") if cat_choice == "+ Kategori Baru" else cat_choice
            
            img_opt = st.radio("Foto Produk:", ["Link URL", "Upload File"], horizontal=True)
            final_img = "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=300"
            if img_opt == "Upload File":
                up_file = st.file_uploader("Pilih Gambar", type=["png", "jpg", "jpeg"])
                if up_file:
                    b64 = base64.b64encode(up_file.getvalue()).decode("utf-8")
                    final_img = f"data:image/jpeg;base64,{b64}"
            else:
                url_in = st.text_input("URL Gambar", final_img)
                if url_in: final_img = url_in

            new_qty = st.number_input("Stok Awal", min_value=0, value=15)
            new_price = st.number_input("Harga E-Paper (Rp)", min_value=0, value=7500, step=500)

            if st.button("Simpan & Pasang Label", type="primary", use_container_width=True):
                if new_rak.strip() and new_item.strip():
                    st.session_state.inventory[new_rak.strip()] = {
                        "item": new_item.strip(), "category": new_cat.strip(), "qty": new_qty,
                        "price": new_price, "battery": "100%", "image": final_img,
                        "inflow": [new_qty, new_qty], "outflow": [0, 0]
                    }
                    add_log("SUCCESS", f"[{current_user['name']}] Menambah {new_item} di {new_rak}")
                    st.rerun()

        if st.session_state.app_tier in ["Premium", "Pro"]:
            with st.expander("⚡ Flash Sale Massal"):
                disc = st.slider("Diskon (%)", 5, 70, 15, 5)
                dur = st.selectbox("Durasi", [15, 30, 60, 120], format_func=lambda x: f"{x} Detik")
                if not st.session_state.flash_sale_active:
                    if st.button("Mulai Flash Sale", type="primary", use_container_width=True):
                        st.session_state.original_prices = {r: d["price"] for r, d in st.session_state.inventory.items()}
                        for r in st.session_state.inventory:
                            st.session_state.inventory[r]["price"] = int(st.session_state.inventory[r]["price"] * (1 - disc / 100))
                        st.session_state.flash_sale_active = True
                        st.session_state.flash_sale_end = time.time() + dur
                        add_log("WARNING", f"Flash Sale {disc}% aktif selama {dur} detik!")
                        st.rerun()
                else:
                    st.warning(f"Sisa Waktu: {max(0, int(st.session_state.flash_sale_end - time.time()))} detik")
                    if st.button("Hentikan Flash Sale", use_container_width=True):
                        for r, op in st.session_state.original_prices.items():
                            if r in st.session_state.inventory: st.session_state.inventory[r]["price"] = op
                        st.session_state.flash_sale_active = False
                        st.rerun()

    with st.expander("🏪 Pengaturan & Sesi"):
        s_name = st.text_input("Nama Toko", st.session_state.store_name)
        if st.button("Simpan Nama Toko", use_container_width=True):
            st.session_state.store_name = s_name; st.rerun()
        if st.button("🔄 Ganti Paket Lisensi", use_container_width=True):
            st.session_state.app_tier = None; st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False; st.session_state.app_tier = None; st.rerun()

# ==========================================
# 6. HALAMAN DETAIL PRODUK
# ==========================================
if st.session_state.page == "detail":
    rak_key = st.session_state.selected_rak
    if rak_key not in st.session_state.inventory:
        st.session_state.page = "home"; st.rerun()
    prod = st.session_state.inventory[rak_key]

    if st.button("⬅️ Kembali ke Dashboard"):
        st.session_state.page = "home"; st.rerun()

    with st.container(border=True):
        c1, c2 = st.columns([1, 3])
        with c1: st.image(prod["image"], use_container_width=True)
        with c2:
            st.subheader(f"{prod['item']} ({rak_key})")
            st.write(f"📂 **Kategori:** {prod['category']} | 🔋 **Baterai Smart Label:** {prod.get('battery', '95%')}")
            st.write(f"📦 **Stok Saat Ini:** {prod['qty']} Pcs | 🏷️ **Harga E-Paper:** Rp {prod['price']:,}")

    if st.session_state.app_tier in ["Premium", "Pro"]:
        st.subheader("📈 Pergerakan Stok (Masuk vs Terjual)")
        st.line_chart({"Masuk": prod["inflow"], "Terjual": prod["outflow"]})
    else:
        st.info("🔒 Upgrade ke paket Premium/Pro untuk melihat grafik riwayat stok.")
    st.stop()

# ==========================================
# 7. SISTEM TAB UTAMA DASHBOARD
# ==========================================
notif_badge = f" ({len(pending_reqs)})" if pending_reqs else ""
tab1, tab2, tab3 = st.tabs([
    "📦 Monitoring Rak & Label",
    f"📩 Permintaan Restock & Chat{notif_badge}",
    "👥 Manajemen Akun Tim"
])

# ------------------------------------------
# TAB 1: MONITORING RAK & PRODUK
# ------------------------------------------
with tab1:
    inv_list = list(st.session_state.inventory.values())
    low_raks = [k for k, v in st.session_state.inventory.items() if v["qty"] <= 5]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Rak / SKU", f"{len(inv_list)} Rak")
    m2.metric("Total Stok Fisik", f"{sum(d['qty'] for d in inv_list)} Pcs")
    m3.metric("Nilai Aset Barang", f"Rp {sum(d['qty'] * d['price'] for d in inv_list):,}")
    m4.metric("Perlu Restock", f"{len(low_raks)} Rak", delta="-Stok menipis" if low_raks else "Aman", delta_color="inverse")

    if st.session_state.app_tier == "Pro":
        if low_raks:
            st.error(f"🧠 **AI Advisor:** Stok pada **{', '.join(low_raks)}** menipis (≤5 pcs). Disarankan segera melakukan restock.")
        else:
            st.success("🧠 **AI Advisor:** Seluruh stok rak aman. Waktu ideal untuk mengaktifkan promo akhir pekan.")

    fc1, fc2, fc3 = st.columns([1.5, 2, 1])
    with fc1:
        cats = ["Semua Kategori"] + sorted(list(set(d["category"] for d in inv_list)))
        sel_cat = st.selectbox("Kategori", cats, label_visibility="collapsed")
    with fc2:
        search_q = st.text_input("Cari", placeholder="🔍 Cari nama barang atau kode rak...", label_visibility="collapsed")
    with fc3:
        df_export = pd.DataFrame([
            {"Kode Rak": k, "Produk": v["item"], "Kategori": v["category"], "Stok": v["qty"], "Harga E-Paper": v["price"]}
            for k, v in st.session_state.inventory.items()
        ])
        st.download_button("📥 Export CSV", df_export.to_csv(index=False).encode("utf-8"), "laporan_storify.csv", "text/csv", use_container_width=True)

    st.write("")

    for rak_id, data in list(st.session_state.inventory.items()):
        if sel_cat != "Semua Kategori" and data["category"] != sel_cat: continue
        if search_q.lower() not in data["item"].lower() and search_q.lower() not in rak_id.lower(): continue

        with st.container(border=True):
            c_img, c_inf, c_stk, c_prc, c_act = st.columns([0.8, 2, 1.5, 1.8, 1.8], vertical_alignment="center")
            with c_img: st.image(data["image"], use_container_width=True)
            with c_inf:
                st.markdown(f"**📍 {rak_id} — {data['item']}**")
                st.caption(f"📂 {data['category']} | 🔋 Label: {data.get('battery', '95%')}")
            with c_stk:
                st.write(f"📦 **{data['qty']} Pcs**")
                st.markdown("<span class='badge-low'>⚠️ Menipis</span>" if data["qty"] <= 5 else "<span class='badge-ok'>✔ Aman</span>", unsafe_allow_html=True)
            with c_prc:
                st.markdown(f"<span class='price-text'>Rp {data['price']:,}</span>", unsafe_allow_html=True)
            with c_act:
                if st.button("📊 Detail", key=f"det_{rak_id}", use_container_width=True):
                    st.session_state.selected_rak = rak_id
                    st.session_state.page = "detail"
                    st.rerun()

                with st.popover("⚙️ Kelola", use_container_width=True):
                    new_q = st.number_input("Stok Fisik", min_value=0, value=data["qty"], key=f"q_{rak_id}")
                    if is_privileged:
                        new_p = st.number_input("Harga E-Paper (Rp)", min_value=0, value=int(data["price"]), step=500, key=f"p_{rak_id}")
                        if st.session_state.app_tier in ["Premium", "Pro"]:
                            st.caption("Diskon Cepat:")
                            d1, d2, d3 = st.columns(3)
                            for col_d, pct in zip([d1, d2, d3], [10, 20, 50]):
                                if col_d.button(f"-{pct}%", key=f"d{pct}_{rak_id}", use_container_width=True):
                                    st.session_state.inventory[rak_id]["price"] = int(data["price"] * (1 - pct/100))
                                    add_log("INFO", f"[{current_user['name']}] Diskon {pct}% pada {rak_id}")
                                    st.rerun()

                        if st.button("💾 Simpan", type="primary", key=f"sv_{rak_id}", use_container_width=True):
                            if new_q > data["qty"]: st.session_state.inventory[rak_id]["inflow"].append(new_q - data["qty"])
                            elif new_q < data["qty"]: st.session_state.inventory[rak_id]["outflow"].append(data["qty"] - new_q)
                            st.session_state.inventory[rak_id]["qty"] = new_q
                            st.session_state.inventory[rak_id]["price"] = new_p
                            add_log("INFO", f"[{current_user['name']}] Update {rak_id}: Stok={new_q}, Harga=Rp {new_p:,}")
                            st.rerun()

                        if st.button("🗑️ Hapus Rak", key=f"del_{rak_id}", use_container_width=True):
                            del st.session_state.inventory[rak_id]
                            add_log("ERROR", f"[{current_user['name']}] Menghapus {rak_id}")
                            st.rerun()
                    else:
                        if st.button("💾 Update Stok", type="primary", key=f"sv_{rak_id}", use_container_width=True):
                            st.session_state.inventory[rak_id]["qty"] = new_q
                            add_log("INFO", f"[{current_user['name']}] Update stok {rak_id} -> {new_q} pcs")
                            st.rerun()

    if st.session_state.app_tier in ["Premium", "Pro"] and is_privileged:
        st.divider()
        with st.expander("📜 Log Aktivitas & Sinkronisasi Sistem"):
            for l in st.session_state.logs[:10]:
                st.text(f"{l['time']} [{l['type']}] >> {l['action']}")

# ------------------------------------------
# TAB 2: PERMINTAAN RESTOCK & CHAT TIM
# ------------------------------------------
with tab2:
    col_req, col_chat = st.columns([1.1, 1])

    # Kolom Kiri: Pengajuan & Approval Restock
    with col_req:
        st.subheader("📦 Permintaan Restock (Demand)")
        
        # Form pengajuan khusus (Staff bisa ajukan, Atasan juga bisa buat catatan restock)
        with st.container(border=True):
            st.markdown("**Ajukan Permintaan Barang ke Manager/Owner**")
            rak_options = list(st.session_state.inventory.keys())
            if rak_options:
                sel_rak_req = st.selectbox("Pilih Rak / Produk:", rak_options, format_func=lambda r: f"{r} - {st.session_state.inventory[r]['item']} (Sisa: {st.session_state.inventory[r]['qty']})")
                req_qty = st.number_input("Jumlah Tambahan Diminta (Pcs)", min_value=1, value=20, step=5)
                req_note = st.text_input("Catatan untuk Atasan", placeholder="Contoh: Stok menipis, butuh segera besok pagi")
                if st.button("📨 Kirim Permintaan Restock", type="primary", use_container_width=True):
                    new_id = len(st.session_state.restock_requests) + 1
                    st.session_state.restock_requests.insert(0, {
                        "id": new_id, "rak": sel_rak_req, "item": st.session_state.inventory[sel_rak_req]["item"],
                        "qty": req_qty, "by": current_user["name"], "note": req_note or "-",
                        "status": "PENDING", "time": datetime.now().strftime("%H:%M")
                    })
                    add_log("WARNING", f"[{current_user['name']}] Mengajukan restock +{req_qty} pcs untuk {sel_rak_req}")
                    st.success("Permintaan berhasil dikirim ke Manager/Owner!")
                    time.sleep(0.4)
                    st.rerun()

        st.write("**Daftar Pengajuan Restock:**")
        if not st.session_state.restock_requests:
            st.info("Belum ada pengajuan restock.")
        else:
            for req in st.session_state.restock_requests:
                with st.container(border=True):
                    r_c1, r_c2 = st.columns([2.5, 1.2], vertical_alignment="center")
                    with r_c1:
                        st.markdown(f"**{req['rak']} — {req['item']}** (`+{req['qty']} Pcs`)")
                        st.caption(f"Oleh: {req['by']} ({req['time']}) | Catatan: {req['note']}")
                    with r_c2:
                        if req["status"] == "PENDING":
                            if is_privileged:
                                if st.button("✅ Setujui", key=f"acc_{req['id']}", type="primary", use_container_width=True):
                                    req["status"] = "APPROVED"
                                    if req["rak"] in st.session_state.inventory:
                                        st.session_state.inventory[req["rak"]]["qty"] += req["qty"]
                                        st.session_state.inventory[req["rak"]]["inflow"].append(req["qty"])
                                    add_log("SUCCESS", f"[{current_user['name']}] Menyetujui restock {req['rak']} (+{req['qty']} pcs)")
                                    st.rerun()
                                if st.button("❌ Tolak", key=f"rej_{req['id']}", use_container_width=True):
                                    req["status"] = "REJECTED"
                                    st.rerun()
                            else:
                                st.warning("⏳ Menunggu ACC")
                        elif req["status"] == "APPROVED":
                            st.success("✔ Disetujui")
                        else:
                            st.error("✖ Ditolak")

    # Kolom Kanan: Kontak Chat Internal Tim
    with col_chat:
        st.subheader("💬 Kontak Chat Tim (Gudang ↔ Manager)")
        with st.container(border=True, height=380):
            for chat in st.session_state.team_chat:
                is_me = chat["sender"] == current_user["name"]
                align_icon = "🧑‍💼" if chat["role"] != "STAFF" else "👷"
                with st.chat_message("user" if is_me else "assistant", avatar=align_icon):
                    st.markdown(f"**{chat['sender']}** `{chat['role']}` • <span style='font-size:11px; opacity:0.7;'>{chat['time']}</span>", unsafe_allow_html=True)
                    st.write(chat["msg"])

        with st.form("chat_form", clear_on_submit=True):
            c_in1, c_in2 = st.columns([4, 1])
            with c_in1:
                chat_msg = st.text_input("Ketik pesan...", placeholder="Tulis pesan untuk manager atau staf gudang...", label_visibility="collapsed")
            with c_in2:
                sent = st.form_submit_button("Kirim", type="primary", use_container_width=True)
            if sent and chat_msg.strip():
                st.session_state.team_chat.append({
                    "sender": current_user["name"], "role": current_user["role"],
                    "msg": chat_msg.strip(), "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()

# ------------------------------------------
# TAB 3: MANAJEMEN AKUN TIM
# ------------------------------------------
with tab3:
    st.subheader("👥 Daftar & Pendaftaran Akun Karyawan")
    col_acc_list, col_acc_add = st.columns([1.5, 1])

    with col_acc_list:
        for idx, acc in enumerate(st.session_state.accounts):
            with st.container(border=True):
                ac1, ac2, ac3 = st.columns([2.5, 1, 1], vertical_alignment="center")
                with ac1:
                    st.markdown(f"**{acc['name']}** ({acc['email']})")
                    st.caption(f"Hak Akses: `{acc['role']}`")
                with ac2:
                    if idx == st.session_state.current_user_idx:
                        st.success("Aktif")
                    else:
                        if st.button("Login", key=f"sw_{idx}", use_container_width=True):
                            st.session_state.current_user_idx = idx
                            st.rerun()
                with ac3:
                    if is_privileged and idx != st.session_state.current_user_idx and len(st.session_state.accounts) > 1:
                        if st.button("🗑️ Hapus", key=f"del_acc_{idx}", use_container_width=True):
                            st.session_state.accounts.pop(idx)
                            if st.session_state.current_user_idx >= len(st.session_state.accounts):
                                st.session_state.current_user_idx = 0
                            st.rerun()

    with col_acc_add:
        with st.container(border=True):
            st.markdown("**➕ Tambah Akun Baru**")
            if is_privileged:
                new_acc_name = st.text_input("Nama Lengkap", placeholder="Contoh: Budi Santoso")
                new_acc_email = st.text_input("Email", placeholder="budi@storify.id")
                new_acc_role = st.selectbox("Jabatan (Role)", ["STAFF", "MANAGER", "DEVELOPER", "OWNER"])
                if st.button("Daftarkan Akun", type="primary", use_container_width=True):
                    if new_acc_name.strip() and new_acc_email.strip():
                        st.session_state.accounts.append({
                            "name": new_acc_name.strip(),
                            "role": new_acc_role,
                            "email": new_acc_email.strip()
                        })
                        add_log("SUCCESS", f"[{current_user['name']}] Menambahkan akun baru: {new_acc_name} ({new_acc_role})")
                        st.success(f"Akun {new_acc_name} berhasil dibuat!")
                        time.sleep(0.4)
                        st.rerun()
                    else:
                        st.warning("Nama dan email wajib diisi.")
            else:
                st.info("🔒 Hanya Owner, Manager, atau Developer yang dapat menambahkan akun baru.")
