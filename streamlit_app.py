import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

st.title("Zara Sales Forecast Dashboard")

uploaded = st.file_uploader("Upload CSV data", type="csv")
if uploaded:
    df = pd.read_csv(uploaded, sep=";")
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)
    df_monthly = df.groupby('bulan')['pendapatan'].sum().reset_index()

    st.subheader("📊 Monthly Revenue")
    st.line_chart(df_monthly.set_index('bulan')['pendapatan'])

    df_monthly['bulan_num'] = np.arange(len(df_monthly))
    X, y = df_monthly[['bulan_num']], df_monthly['pendapatan']
    model = LinearRegression().fit(X, y)
    df_monthly['predicted'] = model.predict(X)

    st.subheader("🔮 Forecast Next Month")
    next_idx = df_monthly['bulan_num'].max() + 1
    forecast = model.predict([[next_idx]])[0]
    st.write(f"Projected revenue: **{forecast:,.0f} VND**")

    st.subheader("📈 Model Performance")
    mse = mean_squared_error(y, df_monthly['predicted'])
    rmse = np.sqrt(mse)
    r2 = r2_score(y, df_monthly['predicted'])
    st.write(f"- RMSE: {rmse:.2f}")
    st.write(f"- R² Score: {r2:.3f}")

    st.subheader("📉 Actual vs Forecast")
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(df_monthly['bulan'], y, marker='o', label='Actual')
    ax.plot(df_monthly['bulan'], df_monthly['predicted'], marker='x', label='Predicted')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue')
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

