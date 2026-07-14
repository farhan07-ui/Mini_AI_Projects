import streamlit as st
import os
from src.agent import FinanceAgent

st.set_page_config(page_title="Local Private Finance AI", page_icon="💰", layout="centered")

# --- SIDEBAR FOR UPLOADS ---
with st.sidebar:
    st.header("📂 Data Management")
    uploaded_file = st.file_uploader("Upload your transactions.csv", type=["csv"])
    
    if uploaded_file is not None:
        # Save the uploaded file locally to the data/ folder
        os.makedirs("data", exist_ok=True)
        with open("data/transactions.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Successfully loaded transactions.csv!")

st.title("💰 Local Private Finance AI")
st.caption("All data remains strictly local on your machine. Powered by Ollama.")

import pandas as pd
import plotly.express as px # Run "pip install plotly" in your VS Code terminal

# Check if CSV exists and display a mini dashboard
csv_path = "data/transactions.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = [col.lower().strip() for col in df.columns]
    
    # 1. Metric Display Cards
    if "amount" in df.columns:
        total = df["amount"].sum()
        st.metric(label="Total Expenses This Month", value=f"${total:,.2f}")
        
    # 2. Interactive Expense Pie Chart
    if "category" in df.columns and "amount" in df.columns:
        fig = px.pie(df, values="amount", names="category", title="Spending Breakdown")
        st.plotly_chart(fig, use_container_width=True)
        # (Keep the rest of your app.py session state and chat history logic here!)