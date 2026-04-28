import pandas as pd
import streamlit as st

def load_csv(file_path):
    """
    دالة لقراءة ملف الـ CSV والاحتفاظ به في ذاكرة التخزين المؤقت
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None