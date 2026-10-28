import streamlit as st
import time
from datetime import datetime

# Configuration
st.set_page_config(page_title="Storify - Smart Label & Dynamic Pricing", layout="wide", page_icon="🏷️")

# Inisialisasi State
if "lang" not in st.session_state:
    st.session_state.lang = "ID"

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "store_name" not in st.session_state:
    st.session_state.store_name = "Storify - Cabang Utama"

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_rak" not in st.session_state:
    st.session_state.selected_rak = None

if "user" not in st.session_state:
    st.session_state.user = {"name": "James Arthur", "role": "OWNER", "email": "james.arthur@gmail.com"}

if "logs" not in st.session_state:
    st.session_state.logs = [
        {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": "Storify IoT & E-Paper Cloud system successfully initialized."}
    ]

if "original_prices" not in st.session_state:
    st.session_state.original_prices = {}

if "flash_sale_active" not in st.session_state:
    st.session_state.flash_sale_active = False

if "flash_sale_end" not in st.session_state:
    st.session_state.flash_sale_end = 0.0

# ----------------- TERJEMAHAN KATA MENYELURUH (DICTIONARY) -----------------
t = {
    "ID": {
        "caption": "Solusi Retail Phygital Modern: Manajemen Harga Otomatis & E-Paper IoT Dashboard",
        "sidebar_title": "⚙️ Panel Kontrol Storify",
        "lang_label": "Bahasa / Language",
        "theme_label": "Mode Tema",
        "section_shelf": "📦 Live Monitoring Rak & Smart Label",
        "section_log": "📜 Terminal Log Aktivitas Sistem (Audit Trail)",
        "weight_label": "Stok Aktual",
        "price_label": "Harga E-Paper",
        "cat_label": "Filter Kategori",
        "all_cat": "Semua Kategori",
        "search_label": "Cari Produk...",
        "btn_back": "⬅️ Kembali ke Beranda",
        "access_denied": "Akses Dibatasi: Hanya Owner dan Manager yang dapat melihat Audit Log & Pengaturan Lanjutan.",
    },
    "EN": {
        "caption": "Modern Phygital Retail Solution: Automated Pricing & E-Paper IoT Dashboard",
        "sidebar_title": "⚙️ Storify Control Panel",
        "lang_label": "Language",
        "theme_label": "Theme Mode",
        "section_shelf": "📦 Live Shelf Monitoring & Smart Labels",
        "section_log": "📜 System Audit Trail Terminal",
        "weight_label": "Actual Stock",
        "price_label": "E-Paper Price",
        "cat_label": "Filter Category",
        "all_cat": "All Categories",
        "search_label": "Search products...",
        "btn_back": "⬅️ Back to Dashboard",
        "access_denied": "Access Restricted: Only Owners and Managers can view Audit Logs & Advanced Settings.",
    }
}

lang = st.session_state.lang
theme = st.session_state.theme

# Dynamic CSS Styling Premium (Fix Total Tombol & Input di Dark Mode)
if theme == "Dark":
    bg_color = "#090d16"
    card_bg = "#111827"
    text_color = "#f9fafb"
    subtext_color = "#9ca3af"
    border_color = "#374151"
    price_bg = "#1f2937"
    input_bg = "#1f2937"
    input_text = "#ffffff"
    btn_bg = "#2563eb"
    btn_text = "#ffffff"
else:
    bg_color = "#f8fafc"
    card_bg = "#ffffff"
    text_color = "#0f172a"
    subtext_color = "#475569"
    border_color = "#cbd5e1"
    price_bg = "#f1f5f9"
    input_bg = "#ffffff"
    input_text = "#0f172a"
    btn_bg = "#eff6ff"
    btn_text = "#1e3a8a"

st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_color}; }}
    
    /* Paksa seluruh teks & label agar konsisten */
    h1, h2, h3, h4, h5, h6, p, span, label, div, .stMarkdown {{
        color: {text_color} !important;
    }}
    
    /* Perbaikan total kontras input & selectbox Streamlit */
    input, textarea, div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
        -webkit-text-fill-color: {input_text} !important;
        border-color: {border_color} !important;
        border-radius: 8px !important;
    }}
    
    /* Styling Tombol Standar Agar Selalu Cantik dan Kontras */
    .stButton > button {{
        background-color: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1px solid {border_color} !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        border-color: #3b82f6 !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }}
    
    .card {{
        background-color: {card_bg};
        padding: 22px;
        border-radius: 16px;
        border: 1px solid {border_color};
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }}
    .card:hover {{
        border-color: #3b82f6;
        box-shadow: 0 15px 30px -5px rgba(59, 130, 246, 0.15);
    }}
    .price-tag {{
        font-size: 19px; font-weight: 800; color: #2563eb;
        background: {price_bg}; padding: 8px 14px; border-radius: 10px; display: inline-block;
        border: 1px solid {border_color};
    }}
    .log-terminal {{
        background-color: #030712; color: #38bdf8; padding: 18px;
        border-radius: 12px; font-family: monospace; font-size: 13px; max-height: 220px; overflow-y: auto;
        border: 1px solid #1f2937;
    }}
    .user-badge {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        padding: 16px 20px;
        border-radius: 14px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }}
</style>
""", unsafe_allow_html=True)

# State Management Default Inventory
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

# Cek Timer Flash Sale Massal otomatis habis
current_time_epoch = time.time()
if st.session_state.flash_sale_active and current_time_epoch > st.session_state.flash_sale_end:
    for rak, orig_p in st.session_state.original_prices.items():
        if rak in st.session_state.inventory:
            st.session_state.inventory[rak]["price"] = orig_p
    st.session_state.flash_sale_active = False
    st.session_state.original_prices = {}
    msg = "Bulk Flash Sale ended. Prices restored to normal." if lang == "EN" else "Waktu Flash Sale Massal habis. Harga kembali normal."
    st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": msg})

# Header & Kontrol Atas
col_head1, col_head2 = st.columns([3, 2])
with col_head1:
    st.title(f"🏷️ {st.session_state.store_name}")
    st.caption(t[lang]["caption"])
with col_head2:
    sub_c1, sub_c2 = st.columns(2)
    with sub_c1:
        sel_lang = st.selectbox(t[lang]["lang_label"], ["ID", "EN"], index=0 if lang=="ID" else 1)
        if sel_lang != st.session_state.lang:
            st.session_state.lang = sel_lang
            st.rerun()
    with sub_c2:
        sel_theme = st.selectbox(t[lang]["theme_label"], ["Light", "Dark"], index=0 if theme=="Light" else 1)
        if sel_theme != st.session_state.theme:
            st.session_state.theme = sel_theme
            st.rerun()

# Widget Profil Akun
current_role_display = st.session_state.user['role']
st.markdown(f"""
<div class="user-badge">
    <div>
        👤 <b style="color: {text_color};">{st.session_state.user['name']}</b> <span style="color:#3b82f6; font-size:12px; font-weight:bold;">[{current_role_display}]</span><br>
        <span style="font-size:12px; color:{subtext_color};">{st.session_state.user['email']}</span>
    </div>
    <div style="font-size:12px; background:#10b981; color:white; padding:6px 12px; border-radius:20px; font-weight:bold;">
        🟢 Storify Active Session
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Pengaturan
st.sidebar.header(t[lang]["sidebar_title"])

# Rename Store
with st.sidebar.expander("🏪 Ubah Nama Toko (Rename Store)", expanded=False):
    new_store_name = st.text_input("Nama Toko / Cabang", st.session_state.store_name)
    if st.button("Perbarui Nama Toko"):
        st.session_state.store_name = new_store_name
        st.sidebar.success("Nama toko berhasil diubah!")
        time.sleep(0.3)
        st.rerun()

with st.sidebar.expander("👤 Switch User Account", expanded=False):
    selected_account = st.selectbox("Select Account", ["James Arthur (Owner)", "Sarah Connor (Manager)", "William Alexander (Staff Gudang)"])
    if "James" in selected_account:
        st.session_state.user = {"name": "James Arthur", "role": "OWNER", "email": "james.arthur@gmail.com"}
    elif "Sarah" in selected_account:
        st.session_state.user = {"name": "Sarah Connor", "role": "MANAGER", "email": "sarah.connor@gmail.com"}
    else:
        st.session_state.user = {"name": "William Alexander", "role": "STAFF", "email": "williamalexander@gmail.com"}
    if st.button("Apply Account"):
        st.sidebar.success(f"Logged in as {st.session_state.user['name']}")
        st.rerun()

is_privileged = st.session_state.user["role"] in ["OWNER", "MANAGER"]

if is_privileged:
    # FITUR TAMBAH PRODUK DENGAN UPLOAD FOTO SENDIRI
    with st.sidebar.expander("➕ Add New Product & Upload Image", expanded=False):
        target_rak = st.text_input("Shelf Code (e.g., Shelf E5)", "Rak E5")
        item_name = st.text_input("Product Name", "Body Soap 100g")
        
        # Pilihan input foto: URL atau Upload File Lokal
        img_source = st.radio("Sumber Foto", ["Upload File Gambar", "Gunakan Link URL"])
        final_img = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300"
        
        if img_source == "Upload File Gambar":
            uploaded_file = st.file_uploader("Pilih Foto Produk", type=["png", "jpg", "jpeg"])
            if uploaded_file is not None:
                # Simpan gambar sebagai data stream / temporary string
                import base64
                bytes_data = uploaded_file.getvalue()
                base64_str = base64.b64encode(bytes_data).decode("utf-8")
                final_img = f"data:image/jpeg;base64,{base64_str}"
        else:
            url_input = st.text_input("URL Foto", "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300")
            if url_input:
                final_img = url_input
        
        existing_categories = list(set(d.get("category", "General") for d in st.session_state.inventory.values()))
        cat_mode = st.radio("Category Type", ["Select Existing", "Create New"])
        if cat_mode == "Select Existing":
            category_name = st.selectbox("Category", existing_categories if existing_categories else ["General"])
        else:
            category_name = st.text_input("New Category Name", "Personal Care")
            
        qty_val = st.number_input("Stock Quantity", min_value=0, value=15, step=1)
        price_val = st.number_input("E-Paper Price (Rp)", min_value=0, value=12000, step=500)
        
        if st.button("Save New Product"):
            if target_rak:
                st.session_state.inventory[target_rak] = {
                    "item": item_name, 
                    "category": category_name.strip() if category_name else "General", 
                    "qty": qty_val, 
                    "price": price_val,
                    "image": final_img,
                    "inflow": [5, 10],
                    "outflow": [2, 4]
                }
                log_msg = f"[{st.session_state.user['name']}] Added product: {item_name} at {target_rak}"
                st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "SUCCESS", "action": log_msg})
                st.sidebar.success("Saved successfully!")
                time.sleep(0.4)
                st.rerun()

    with st.sidebar.expander("⚡ Bulk Flash Sale (All Products)", expanded=False):
        disc_percent = st.slider("Discount Percentage (%)", min_value=5, max_value=50, value=15, step=5)
        duration_sec = st.selectbox("Duration", [15, 30, 60], format_func=lambda x: f"{x} Seconds")
        
        if not st.session_state.flash_sale_active:
            if st.button("Run Bulk Flash Sale"):
                st.session_state.original_prices = {r: d["price"] for r, d in st.session_state.inventory.items()}
                for r in st.session_state.inventory:
                    st.session_state.inventory[r]["price"] = int(st.session_state.inventory[r]["price"] * (1 - disc_percent / 100))
                st.session_state.flash_sale_active = True
                st.session_state.flash_sale_end = time.time() + duration_sec
                log_msg = f"[{st.session_state.user['name']}] Storify Bulk Flash Sale {disc_percent}% activated ({duration_sec}s)!"
                st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "WARNING", "action": log_msg})
                st.rerun()
        else:
            rem = int(st.session_state.flash_sale_end - time.time())
            st.warning(f"Flash Sale Active! Remaining: {max(0, rem)}s")
            if st.button("Cancel & Restore Normal Prices"):
                for r, op in st.session_state.original_prices.items():
                    if r in st.session_state.inventory:
                        st.session_state.inventory[r]["price"] = op
                st.session_state.flash_sale_active = False
                st.session_state.original_prices = {}
                log_msg = f"[{st.session_state.user['name']}] Bulk Flash Sale cancelled."
                st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": log_msg})
                st.rerun()
else:
    st.sidebar.info("ℹ️ Staff Mode: You have permission to manage stock (Restock). Advanced settings & logs are restricted to Owner & Manager.")

# =========================================================================
# HALAMAN 1: DETAIL PRODUK
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
        
    st.markdown(f"## 📊 Storify Analytics & Product Detail: {rak_key}")
    
    d_col1, d_col2 = st.columns([1, 2])
    with d_col1:
        st.image(prod.get("image", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300"), caption=prod["item"], use_container_width=True)
    with d_col2:
        st.markdown(f"### **{prod['item']}**")
        st.write(f"📂 **Category:** {prod.get('category', 'General')}")
        st.write(f"📦 **Current Stock:** {prod['qty']} Pcs")
        st.write(f"🏷️ **E-Paper Price:** Rp {prod['price']:,}")
        
    st.divider()
    st.subheader("📈 Stock Inflow vs Outflow Chart")
    
    chart_data = {
        "Inflow": prod.get("inflow", [5, 10, 15, prod["qty"]]),
        "Outflow": prod.get("outflow", [2, 5, 10, 12])
    }
    st.line_chart(chart_data)
    
    st.stop()

# =========================================================================
# HALAMAN 2: BERANDA / DASHBOARD UTAMA
# =========================================================================

# Filter Kategori & Search Bar
filter_c1, filter_c2 = st.columns([2, 2])
with filter_c1:
    categories = [t[lang]["all_cat"]] + list(set(d.get("category", "General") for d in st.session_state.inventory.values()))
    selected_category = st.selectbox(t[lang]["cat_label"], categories)
with filter_c2:
    search_query = st.text_input(t[lang]["search_label"], "")

st.divider()

st.subheader(t[lang]["section_shelf"])

if not st.session_state.inventory:
    st.info("No products registered.")
else:
    filtered_inv = {}
    for k, v in st.session_state.inventory.items():
        match_cat = (selected_category == t[lang]["all_cat"] or v.get("category", "General") == selected_category)
        match_search = (search_query.lower() in v["item"].lower() or search_query.lower() in k.lower())
        if match_cat and match_search:
            filtered_inv[k] = v

    if not filtered_inv:
        st.warning("Product not found.")
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
                    st.caption(f"📂 {data.get('category', 'General')}")
                    
                with col2:
                    st.write(f"📦 **{t[lang]['weight_label']}**: {data['qty']} Pcs")
                    if data['qty'] <= 5:
                        st.markdown("<span style='color: #ef4444; font-weight:bold;'>⚠️ Low Stock!</span>" if lang=="EN" else "<span style='color: #ef4444; font-weight:bold;'>⚠️ Stok Menipis!</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color: #10b981; font-weight:bold;'>✔ Normal</span>" if lang=="EN" else "<span style='color: #10b981; font-weight:bold;'>✔ Aman</span>", unsafe_allow_html=True)
                    
                with col3:
                    st.write(f"🏷️ **{t[lang]['price_label']}**")
                    st.markdown(f'<div class="price-tag">Rp {data["price"]:,}</div>', unsafe_allow_html=True)
                    
                with col4:
                    detail_btn_label = "🔍 View Detail & Chart" if lang == "EN" else "🔍 Lihat Detail & Grafik"
                    if st.button(detail_btn_label, key=f"det_{rak_id}"):
                        st.session_state.selected_rak = rak_id
                        st.session_state.page = "detail"
                        st.rerun()
                        
                    popover_label = "✏️ Quick Edit & Discount" if lang == "EN" else "✏️ Edit Cepat & Diskon"
                    with st.popover(popover_label):
                        new_q = st.number_input(f"Stock ({rak_id})", min_value=0, value=data["qty"], key=f"q_{rak_id}")
                        
                        if is_privileged:
                            new_p = st.number_input(f"E-Paper Price (Rp)", min_value=0, value=int(data["price"]), step=500, key=f"p_{rak_id}")
                            st.write("Special Item Discount:")
                            d_col1, d_col2, d_col3 = st.columns(3)
                            
                            if d_col1.button("10% OFF", key=f"d10_{rak_id}"):
                                new_p = int(data["price"] * 0.9)
                                st.session_state.inventory[rak_id]["price"] = new_p
                                st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": f"[{st.session_state.user['name']}] Applied 10% discount to {rak_id}: Rp {new_p:,}"})
                                st.rerun()
                            if d_col2.button("20% OFF", key=f"d20_{rak_id}"):
                                new_p = int(data["price"] * 0.8)
                                st.session_state.inventory[rak_id]["price"] = new_p
                                st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": f"[{st.session_state.user['name']}] Applied 20% discount to {rak_id}: Rp {new_p:,}"})
                                st.rerun()
                            if d_col3.button("50% OFF", key=f"d50_{rak_id}"):
                                new_p = int(data["price"] * 0.5)
                                st.session_state.inventory[rak_id]["price"] = new_p
                                st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": f"[{st.session_state.user['name']}] Applied 50% discount to {rak_id}: Rp {new_p:,}"})
                                st.rerun()
                        else:
                            new_p = data["price"]
                            st.info("Staff mode: Price editing is restricted.")

                        if st.button("Save Changes", key=f"save_{rak_id}"):
                            st.session_state.inventory[rak_id]["qty"] = new_q
                            if is_privileged:
                                st.session_state.inventory[rak_id]["price"] = new_p
                            log_msg = f"[{st.session_state.user['name']}] Updated {rak_id}: Stock={new_q}, Price=Rp {new_p:,}"
                            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "INFO", "action": log_msg})
                            st.rerun()
                    
                    restock_val = st.number_input(f"Restock", min_value=1, max_value=100, value=10, key=f"num_{rak_id}", label_visibility="collapsed")
                    restock_btn_label = "➕ Restock" if lang == "EN" else "➕ Restock"
                    if st.button(restock_btn_label, key=f"rest_{rak_id}"):
                        st.session_state.inventory[rak_id]["qty"] += restock_val
                        st.session_state.inventory[rak_id]["outflow"].append(restock_val)
                        log_msg = f"[{st.session_state.user['name']}] Restocked +{restock_val} pcs for {data['item']} ({rak_id})"
                        st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "SUCCESS", "action": log_msg})
                        st.rerun()

                with col5:
                    st.write("")
                    if is_privileged:
                        del_label = "🗑️ Delete" if lang == "EN" else "🗑️ Hapus"
                        if st.button(del_label, key=f"del_{rak_id}", type="secondary"):
                            del st.session_state.inventory[rak_id]
                            log_msg = f"[{st.session_state.user['name']}] Product at {rak_id} deleted."
                            st.session_state.logs.insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "type": "ERROR", "action": log_msg})
                            st.rerun()
                    else:
                        st.caption("🔒 Restricted")
                        
                st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ----------------- TERMINAL AUDIT LOG -----------------
st.subheader(t[lang]["section_log"])

if is_privileged:
    terminal_text = ""
    for log in st.session_state.logs[:12]:
        log_type = log.get("type", "INFO")
        badge = f"[{log_type}]"
        terminal_text += f"{log['time']} {badge:<9} >> {log['action']}\n"

    st.markdown(f'<div class="log-terminal">{terminal_text}</div>', unsafe_allow_html=True)
else:
    st.warning(t[lang]["access_denied"])
