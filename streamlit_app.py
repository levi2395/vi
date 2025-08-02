import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.title("Dự báo doanh số theo tháng — Linear Regression")

df = pd.DataFrame({
    "Tháng": [1, 2, 3, 4, 5, 6],
    "Doanh số": [10000, 15000, 17000, 16000, 18000, 20000]
})

st.subheader("Dữ liệu doanh số (thực tế)")
st.dataframe(df)

X = df[["Tháng"]]
y = df["Doanh số"]
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

fig, ax = plt.subplots()
ax.plot(df["Tháng"], y, "bo-", label="Thực tế")
ax.plot(df["Tháng"], y_pred, "kx--", label="Dự báo")
ax.set_xlabel("Tháng")
ax.set_ylabel("Doanh số")
ax.legend()
st.pyplot(fig)

st.subheader("Chỉ số đánh giá mô hình")
st.write(f"MAE: {mean_absolute_error(y, y_pred):.2f}")
st.write(f"RMSE: {np.sqrt(mean_squared_error(y, y_pred)):.2f}")
st.write(f"R²: {r2_score(y, y_pred):.2f}")

new_month = st.slider("Chọn tháng mới để dự báo", 7, 12, 7)
pred = model.predict([[new_month]])
st.success(f"Dự báo doanh số tháng {new_month}: {pred[0]:.0f}")
