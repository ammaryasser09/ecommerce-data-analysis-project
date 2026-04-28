import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from app_utils import load_csv

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(page_title="Executive Insights Pro", layout="wide")

# ==========================================
# 2. LOAD DATA
# ==========================================
df = load_csv("Data Cleaned.csv")

# ==========================================
# 3. PREMIUM CSS (UPGRADED)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* GLOBAL */
.stApp {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 100%);
    font-family: 'Inter', sans-serif;
    color: #0F172A;
}

/* TITLE */
h1 {
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #4F46E5, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* SELECT BOX */
.stSelectbox > div {
    background: white;
    border-radius: 14px;
    padding: 6px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 6px 18px rgba(0,0,0,0.04);
}

/* KPI CARDS */
.stat-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 10px 25px rgba(0,0,0,0.04);
    transition: 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 35px rgba(79,70,229,0.15);
    border-color: #4F46E5;
}

.stat-val {
    font-size: 26px;
    font-weight: 800;
    color: #0F172A;
}

.stat-lbl {
    font-size: 11px;
    color: #64748B;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* CHART BOX */
.chart-wrapper {
    background: white;
    border-radius: 24px;
    padding: 24px;
    margin-top: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. HEADER
# ==========================================
st.markdown("<h1>Business Metric Explorer</h1>", unsafe_allow_html=True)

# ==========================================
# 5. COLUMN SELECTOR
# ==========================================
col_1, col_2, col_3 = st.columns([1, 2, 1])

with col_2:
    col_selector = st.selectbox("🎯 Select Metric to Analyze:", df.columns)

selected_col = df[col_selector]

st.markdown("---")

# ==========================================
# 6. NUMERIC ANALYSIS
# ==========================================
if pd.api.types.is_numeric_dtype(selected_col):

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("Mean", selected_col.mean(), "📈"),
        ("Median", selected_col.median(), "🎯"),
        ("Std Dev", selected_col.std(), "📉"),
        ("Sum", selected_col.sum(), "💰")
    ]

    for i, (label, val, icon) in enumerate(metrics):
        with [c1, c2, c3, c4][i]:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:20px">{icon}</div>
                <div class="stat-lbl">{label}</div>
                <div class="stat-val">{val:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)

    st.markdown(f"### 📊 Distribution of {col_selector}")

    fig = px.histogram(
        df,
        x=col_selector,
        marginal="violin",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 7. CATEGORICAL ANALYSIS
# ==========================================
else:

    st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)

    st.markdown(f"### 🏆 Top Categories: {col_selector}")

    data = selected_col.value_counts().head(10).reset_index()
    data.columns = [col_selector, "Count"]

    fig = px.bar(
        data,
        x=col_selector,
        y="Count",
        text_auto=True,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. INSIGHTS
# ==========================================
st.markdown('<div class="chart-wrapper">', unsafe_allow_html=True)

st.markdown("### 💡 Insights")

if pd.api.types.is_numeric_dtype(selected_col):
    st.info(f"""
    - Mean: {selected_col.mean():,.2f}
    - Median: {selected_col.median():,.2f}
    - Max: {selected_col.max():,.2f}
    - Min: {selected_col.min():,.2f}
    """)
else:
    st.success(f"Most frequent value: **{selected_col.mode()[0]}**")

st.markdown('</div>', unsafe_allow_html=True)