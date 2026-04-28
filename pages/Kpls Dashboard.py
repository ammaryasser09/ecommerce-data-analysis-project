import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app_utils import load_csv
import os
import base64

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Executive Ecommerce Dashboard", layout="wide")

# تحميل البيانات
df = load_csv("Data Cleaned.csv")

# ألوان الهوية البصرية
PRIMARY_COLOR = "#4F46E5"
SECONDARY_COLOR = "#EC4899"
BG_COLOR = "#F3F4F6"

if df is not None:
    # تجهيز البيانات
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # --- CSS ADVANCED STYLING (Glassmorphism + Hover Animations) ---
    st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_COLOR}; font-family: 'Plus Jakarta Sans', sans-serif; }}
    
    /* Chart Container Hover */
    .stPlotlyChart {{
        border-radius: 20px;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .stPlotlyChart:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }}

    /* KPI CARDS */
    .metric-card {{
        background: white;
        padding: 20px;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        border: 1px solid #E5E7EB;
        transition: all 0.4s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-10px);
        border-color: {PRIMARY_COLOR};
        box-shadow: 0 25px 50px rgba(79, 70, 229, 0.1);
    }}
    .metric-value {{
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .metric-label {{ font-size: 13px; color: #6B7280; font-weight: 600; text-transform: uppercase; }}

    /* Insights Section Style */
    .insight-box {{
        background: #FEF2F2;
        border-left: 5px solid #EF4444;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown('<h1 style="text-align:center;">📊 Strategic Business Dashboard</h1>', unsafe_allow_html=True)
    st.write("##")

    # ==========================================
    # 🔥 1. KPIs SECTION (5 CARDS)
    # ==========================================
    k1, k2, k3, k4, k5 = st.columns(5)
    
    kpis = [
        ("Total Revenue", f"${df['revenue'].sum():,.0f}", "💰"),
        ("Total Orders", f"{df['order_id'].nunique():,}", "📦"),
        ("Total Customers", f"{df['user_id'].nunique():,}", "👤"),
        ("Avg Rating", f"{df['rating'].mean():.2f}", "⭐"),
        ("Units Sold", f"{df['quantity'].sum():,}", "🛒")
    ]
    
    for i, col in enumerate([k1, k2, k3, k4, k5]):
        label, val, icon = kpis[i]
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:20px;">{icon}</div>
                    <p class="metric-label">{label}</p>
                    <p class="metric-value">{val}</p>
                </div>
            """, unsafe_allow_html=True)

    st.write("##")

    # ==========================================
    # 📊 2. SALES TREND (Timeline)
    # ==========================================
    st.subheader("📈 Revenue Growth (Monthly)")
    df['month_year'] = df['order_date'].dt.to_period('M').astype(str)
    trend = df.groupby('month_year')['revenue'].sum().reset_index()
    fig_trend = px.line(trend, x='month_year', y='revenue', markers=True, line_shape='spline',
                        color_discrete_sequence=[PRIMARY_COLOR])
    fig_trend.update_layout(hovermode="x unified", template="plotly_white")
    st.plotly_chart(fig_trend, use_container_width=True)

    # ==========================================
    # 🏆 3. TOP PRODUCTS & CATEGORIES
    # ==========================================
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader("🥇 Top 10 Products by Revenue")
        top_prods = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False).head(10).reset_index()
        st.plotly_chart(px.bar(top_prods, x='revenue', y='product_name', orientation='h', 
                               color='revenue', color_continuous_scale='Viridis'), use_container_width=True)
    
    with col_p2:
        st.subheader("📂 Revenue by Category")
        cat_rev = df.groupby('category')['revenue'].sum().sort_values(ascending=False).reset_index()
        st.plotly_chart(px.pie(cat_rev, values='revenue', names='category', hole=0.4), use_container_width=True)

    # ==========================================
    # 👥 4. CUSTOMER INSIGHTS
    # ==========================================
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        st.subheader("💰 Top Spending Customers")
        top_cust = df.groupby('name')['revenue'].sum().sort_values(ascending=False).head(5).reset_index()
        st.plotly_chart(px.bar(top_cust, x='name', y='revenue', color_discrete_sequence=[SECONDARY_COLOR]), use_container_width=True)

    with col_c2:
        st.subheader("🚻 Gender Split")
        st.plotly_chart(px.pie(df, names='gender', color_discrete_sequence=[PRIMARY_COLOR, SECONDARY_COLOR]), use_container_width=True)

    with col_c3:
        st.subheader("🏙️ Top Cities")
        city_data = df['city'].value_counts().head(5).reset_index()
        st.plotly_chart(px.bar(city_data, x='city', y='count', color_discrete_sequence=['#6366F1']), use_container_width=True)

    # ==========================================
    # ⭐ 5 & 6. RATINGS & BRAND PERFORMANCE
    # ==========================================
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.subheader("✨ Brand Revenue Performance")
        brand_perf = df.groupby('brand')['revenue'].sum().sort_values(ascending=False).head(8).reset_index()
        st.plotly_chart(px.funnel(brand_perf, y='brand', x='revenue'), use_container_width=True)

    with col_r2:
        st.subheader("⭐ Distribution of Ratings")
        st.plotly_chart(px.histogram(df, x='rating', color_discrete_sequence=['#FBBF24']), use_container_width=True)

    # ==========================================
    # 📉 7. CRITICAL INSIGHTS & OUTLIERS
    # ==========================================
    st.markdown("---")
    st.subheader("🕵️ Business Insights & Data Outliers")
    
    # حساب نسبة الإلغاء
    cancel_rate = (len(df[df['order_status'] == 'cancelled']) / len(df)) * 100
    
    i1, i2, i3 = st.columns(3)
    
    with i1:
        st.markdown(f"""
            <div class="insight-box">
                <h4 style="color:#B91C1C;margin:0;">🚫 Cancellation Rate</h4>
                <p style="font-size:24px; font-weight:bold; margin:5px 0;">{cancel_rate:.2f}%</p>
                <small>Keep an eye on fulfillment issues.</small>
            </div>
        """, unsafe_allow_html=True)

    with i2:
        # المنتجات ذات التقييم المنخفض
        low_rated = df.groupby('product_name')['rating'].mean().sort_values().head(3)
        st.markdown('<div class="insight-box" style="border-left-color:#F59E0B; background:#FFFBEB;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#92400E;margin:0;">⚠️ Low Rated Products</h4>', unsafe_allow_html=True)
        for name, r in low_rated.items():
            st.write(f"- {name[:20]}... ({r:.1f}⭐)")
        st.markdown('</div>', unsafe_allow_html=True)

    with i3:
        # اكتشاف الـ Outliers (الطلبات الضخمة جداً)
        q_high = df['revenue'].quantile(0.99)
        outliers_count = len(df[df['revenue'] > q_high])
        st.markdown('<div class="insight-box" style="border-left-color:#10B981; background:#ECFDF5;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#065F46;margin:0;">💎 High-Value Outliers</h4>', unsafe_allow_html=True)
        st.write(f"Found **{outliers_count}** orders exceeding ${q_high:,.0f}.")
        st.write("These are your VIP transactions.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("❌ تعذر تحميل 'Data Cleaned.csv'. تأكد من وجود الملف في المجلد.")