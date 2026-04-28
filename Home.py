import pandas as pd
import streamlit as st
from app_utils import load_csv
import os
import base64

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Ecommerce Analytics Pro",
    page_icon="💎",
    layout="wide",
)

# ==========================================
# 2. PREMIUM UI STYLING
# ==========================================
st.markdown("""
<style>
/* GLOBAL */
.stApp {
    background-color: #F9FAFB;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* TITLE & SUBTITLE */
.main-title {
    font-size: 54px;
    font-weight: 800;
    text-align: center;
    margin-top: 20px;
    background: linear-gradient(90deg, #4F46E5, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-title {
    color: #6B7280;
    font-size: 18px;
    text-align: center;
    margin-bottom: 30px;
}

/* HERO IMAGE */
.hero-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0 40px 0;
}

.hero-img-style {
    width: 100%;
    max-width: 500px;
    border-radius: 30px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.1);
    transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
}

.hero-img-style:hover {
    transform: translateY(-20px) scale(1.05);
    box-shadow: 0 40px 80px rgba(79, 70, 229, 0.3);
}

/* SECTION HEADER */
.section-header {
    font-size: 32px;
    font-weight: 700;
    margin: 50px 0 25px 0;
    padding-left: 15px;
    border-left: 6px solid #4F46E5;
}

/* DATA CARD (SCHEMA) */
.dict-card {
    background: white;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 20px;
    border: 1px solid #E5E7EB;
    height: 150px; /* طول موحد للبطاقات */
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
}
.dict-card:hover {
    transform: translateY(-5px);
    border-color: #4F46E5;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER
# ==========================================
st.markdown('<h1 class="main-title">Ecommerce Data Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">A professional analytics dashboard for exploring business insights</p>', unsafe_allow_html=True)

# ==========================================
# 4. HERO IMAGE (CENTERED)
# ==========================================
image_path = "س.jpeg"
empty_col1, center_col, empty_col2 = st.columns([1, 2, 1])

with center_col:
    if os.path.exists(image_path):
        def get_image_base64(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        img_base64 = get_image_base64(image_path)
        st.markdown(f"""
            <div class="hero-container">
                <img src="data:image/jpeg;base64,{img_base64}" class="hero-img-style">
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 5. DATA LOADING
# ==========================================
df = load_csv("Data Cleaned.csv")

# ==========================================
# 6. DATA OVERVIEW
# ==========================================
st.markdown('<div class="section-header">Dataset Overview</div>', unsafe_allow_html=True)
if df is not None:
    st.dataframe(df.head(15), use_container_width=True)
    st.download_button(label="📥 Download Full Dataset", data=df.to_csv(index=False).encode("utf-8"), file_name="ecommerce_dataset.csv", mime="text/csv")
else:
    st.error("❌ تعذر تحميل ملف 'Data Cleaned.csv'")

# ==========================================
# 7. TECHNICAL SCHEMA (FIXED ROWS)
# ==========================================
st.markdown('<div class="section-header">Technical Schema</div>', unsafe_allow_html=True)

DATA_DICT = {
    "order_id": ("🆔", "Unique order identifier."),
    "order_date": ("📅", "Order timestamp."),
    "order_status": ("🔄", "Current state of the order."),
    "total_amount": ("💰", "Total order value."),
    "name": ("👤", "Customer name."),
    "email": ("📧", "Customer email."),
    "gender": ("🚻", "Customer gender."),
    "city": ("🏙️", "Customer location city."),
    "signup_date": ("🆕", "User registration date."),
    "user_id": ("🔑", "Unique user ID."),
    "order_item_id": ("🔖", "Item ID in order."),
    "product_id": ("📦", "Product SKU."),
    "quantity": ("🔢", "Quantity purchased."),
    "item_price": ("💵", "Price per item."),
    "item_total": ("📊", "Total item cost."),
    "product_name": ("👕", "Product name."),
    "category": ("📂", "Product category."),
    "brand": ("✨", "Product brand."),
    "price": ("💲", "Product price."),
    "review_text": ("💬", "Customer review."),
    "rating": ("⭐", "Rating score."),
    "day": ("📆", "Order day."),
    "month": ("🌙", "Order month."),
    "weekday": ("⏳", "Weekday."),
    "year": ("🗓️", "Year."),
    "revenue": ("💎", "Revenue generated.")
}

items = list(DATA_DICT.items())
cols_per_row = 4  # عدد البطاقات في كل صف

# تقسيم العناصر إلى صفوف
for i in range(0, len(items), cols_per_row):
    row_items = items[i : i + cols_per_row]
    cols = st.columns(cols_per_row)
    
    for j, (col_name, (icon, desc)) in enumerate(row_items):
        with cols[j]:
            st.markdown(f"""
            <div class="dict-card">
                <div style="font-size:24px; margin-bottom:8px;">{icon}</div>
                <div style="color:#4F46E5; font-weight:800; font-size:13px; text-transform:uppercase;">{col_name}</div>
                <p style="color:#6B7280; font-size:11px; margin-top:5px; line-height:1.2;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)