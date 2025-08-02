# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="Zara Sales Forecast", layout="centered")

st.title("📈 Zara Sales Forecast Dashboard")

st.markdown("""
Ứng dụng dự báo doanh thu bán hàng Zara theo tháng.
- Upload file dữ liệu (*.csv)
- Trực quan hóa dữ liệu
- Dự báo doanh thu tháng tiếp theo
""")

# 1. Upload file
uploaded_file = st.file_uploader("📂 Tải lên file Zara CSV", type="csv")

if uploaded_file:
    # 2. Đọc dữ liệu
    df = pd.read_csv(uploaded_file, sep=";")
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df['bulan'] = df['tanggal'].dt.to_period('M').astype(str)

    st.subheader("🧾 Dữ liệu đầu vào")
    st.dataframe(df.head())

    # 3. Doanh thu theo tháng
    df_monthly = df.groupby('bulan')['pendapatan'].sum().reset_index()
    df_monthly['bulan_num'] = np.arange(len(df_monthly))

    st.subheader("📊 Doanh thu theo Tháng")
    st.line_chart(df_monthly.set_index('bulan')['pendapatan'])

    # 4. Huấn luyện mô hình Linear Regression
    X = df_monthly[['bulan_num']]
    y = df_monthly['pendapatan']
    model = LinearRegression()
    model.fit(X, y)
    df_monthly['predicted'] = model.predict(X)

    # 5. Dự báo tháng tiếp theo
    next_index = df_monthly['bulan_num'].max() + 1
    next_month = pd.Period(df_monthly['bulan'].iloc[-1], freq='M') + 1
    forecast = model.predict([[next_index]])[0]

    st.subheader("🔮 Dự báo doanh thu tháng kế tiếp")
    st.write(f"📅 Tháng: **{next_month}**")
    st.write(f"💰 Dự báo doanh thu: **{forecast:,.0f} VND**")

    # 6. Đánh giá mô hình
    st.subheader("📈 Đánh giá mô hình")
    rmse = np.sqrt(mean_squared_error(y, df_monthly['predicted']))
    r2 = r2_score(y, df_monthly['predicted'])
    st.metric("RMSE", f"{rmse:,.2f}")
    st.metric("R² Score", f"{r2:.3f}")

    # 7. Biểu đồ Thực tế vs Dự báo
    st.subheader("📉 Thực tế vs Dự báo")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df_monthly['bulan'], y, marker='o', label='Thực tế')
    ax.plot(df_monthly['bulan'], df_monthly['predicted'], marker='x', label='Dự báo')
    ax.set_xlabel("Tháng")
    ax.set_ylabel("Doanh thu")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.info("Vui lòng tải file CSV để bắt đầu.")
