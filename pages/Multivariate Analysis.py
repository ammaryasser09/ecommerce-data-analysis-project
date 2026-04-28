import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from app_utils import load_csv

# ==========================================
# 1. PAGE CONFIG & PREMIUM STYLING
# ==========================================
st.set_page_config(page_title="Multivariate Intelligence Pro", layout="wide")

# ألوان الهوية البصرية (Indigo & Rose)
PRIMARY_COLOR = "#4F46E5"
SECONDARY_COLOR = "#EC4899"
BG_COLOR = "#F8FAFC" 

df = load_csv("Data Cleaned.csv")

if df is not None:
    # تجهيز البيانات وتفادي أي تكرار في الأسماء
    df['order_date'] = pd.to_datetime(df['order_date'])
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    all_cols = df.columns.tolist()

    # --- CSS المطور (Glassmorphism + Smooth Transitions) ---
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    .stApp {{ background-color: {BG_COLOR}; font-family: 'Plus Jakarta Sans', sans-serif; }}
    
    /* Card Design */
    .glass-card {{
        background: white;
        padding: 30px;
        border-radius: 28px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 25px;
    }}

    /* Control Panel Design */
    .config-panel {{
        background: #ffffff;
        padding: 25px;
        border-radius: 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }}
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: #F1F5F9;
        padding: 8px;
        border-radius: 16px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 12px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: white !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }}

    /* Header Title */
    .main-title {{
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #1E293B 0%, #4F46E5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }}

    /* Insight Pills */
    .insight-pill {{
        background: #F1F5F9;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid {PRIMARY_COLOR};
    }}
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown('<h1 class="main-title" style="text-align:center;">🧠 Multivariate Intelligence</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#64748B; font-size:18px; margin-bottom:40px;">Deep dive into cross-variable correlations and patterns</p>', unsafe_allow_html=True)

    # ==========================================
    # 2. CONTROL PANEL (إصلاح مشكلة التكرار والانهيار)
    # ==========================================
    st.markdown('<div class="config-panel">', unsafe_allow_html=True)
    st.markdown('<p style="font-weight:600; color:#1E293B; margin-bottom:15px;">🛠️ Engine Configuration</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 1, 1, 0.8])
    
    with c1:
        x_ax = st.selectbox("📍 X-Axis (Dimension)", all_cols, index=all_cols.index('category') if 'category' in all_cols else 0)
    with c2:
        # تأكيد اختيار عمود مختلف افتراضياً لتجنب Duplicate Error
        y_default = 'revenue' if 'revenue' in num_cols else num_cols[0]
        y_ax = st.selectbox("📊 Y-Axis (Measure)", num_cols, index=num_cols.index(y_default))
    with c3:
        color_ax = st.selectbox("🎨 Segment By", [None] + cat_cols, index=cat_cols.index('gender')+1 if 'gender' in cat_cols else 0)
    with c4:
        st.write("") 
        show_trend = st.toggle("📈 Show Trendline", value=False) # False لتجنب خطأ statsmodels لو مش مثبتة
        show_points = st.toggle("📍 Raw Points", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 3. ANALYTICS ENGINE (The Fix Logic)
    # ==========================================
    
    # 1. حل مشكلة اختيار نفس العمود (Duplicate Error)
    if x_ax == y_ax:
        st.warning(f"💡 **Discovery Mode:** Selected same variable for both axes. Showing distribution of **{x_ax}**.")
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig = px.histogram(df, x=x_ax, color=color_ax, marginal="box", 
                           template="plotly_white", 
                           color_discrete_sequence=[PRIMARY_COLOR, SECONDARY_COLOR])
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        tab1, tab2, tab3 = st.tabs(["🚀 Discovery Canvas", "🔥 Correlation Matrix", "🕸️ Feature Overlap"])
        
        with tab1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            try:
                if x_ax in cat_cols:
                    # Box Plot للفئات
                    fig = px.box(df, x=x_ax, y=y_ax, color=color_ax, 
                                 points="all" if show_points else "outliers", 
                                 notched=True,
                                 color_discrete_sequence=px.colors.qualitative.Prism)
                else:
                    # Scatter Plot للأرقام
                    fig = px.scatter(df, x=x_ax, y=y_ax, color=color_ax, 
                                     trendline="ols" if show_trend else None,
                                     opacity=0.6,
                                     template="plotly_white")
                
                fig.update_layout(height=600, font_family="Plus Jakarta Sans", margin=dict(t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
                
            except ImportError:
                st.error("⚠️ Trendline (OLS) requires `statsmodels` library. Please run `pip install statsmodels` or disable trendline.")
                # رسم بدون تريند لاين عشان البرنامج مايقفش
                fig = px.scatter(df, x=x_ax, y=y_ax, color=color_ax, opacity=0.6, template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # --- Smart Insights Pills ---
            st.markdown('<p style="font-weight:600; color:#1E293B;">🔍 Automated Insights</p>', unsafe_allow_html=True)
            i1, i2, i3 = st.columns(3)
            with i1:
                st.markdown('<div class="insight-pill">', unsafe_allow_html=True)
                if x_ax in num_cols:
                    corr = df[x_ax].corr(df[y_ax])
                    st.write(f"**Relationship Strength:** {'Strong' if abs(corr)>0.7 else 'Moderate' if abs(corr)>0.4 else 'Weak'}")
                    st.write(f"Correlation: {corr:.2f}")
                else:
                    st.write(f"**Analysis Mode:** Categorical comparison across {x_ax}")
                st.markdown('</div>', unsafe_allow_html=True)
            with i2:
                st.markdown('<div class="insight-pill">', unsafe_allow_html=True)
                st.write(f"**Average {y_ax}:**")
                st.write(f"Value: {df[y_ax].mean():,.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
            with i3:
                st.markdown('<div class="insight-pill">', unsafe_allow_html=True)
                outliers = len(df[df[y_ax] > (df[y_ax].mean() + 2*df[y_ax].std())])
                st.write(f"**Volatility Check:**")
                st.write(f"{outliers} points above 2-std dev")
                st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            corr_m = df[num_cols].corr()
            fig_corr = px.imshow(corr_m, text_auto=".2f", color_continuous_scale='RdBu_r')
            st.plotly_chart(fig_corr, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig_mat = px.scatter_matrix(df, dimensions=num_cols[:4], color=color_ax, opacity=0.4)
            fig_mat.update_layout(height=800)
            st.plotly_chart(fig_mat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Dataset not found! Please check 'Data Cleaned.csv'.")