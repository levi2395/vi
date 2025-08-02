import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Tiêu đề chính
st.title("📈 Dự báo doanh số theo tháng — Linear Regression")

# Dữ liệu mẫu
df = pd.DataFrame({
    "Tháng": [1, 2, 3, 4, 5, 6],
    "Doanh số": [10000, 15000, 17000, 16000, 18000, 20000]
})

st.subheader("📊 Dữ liệu doanh số (thực tế)")
st.dataframe(df)

# Huấn luyện mô hình
X = df[["Tháng"]]
y = df["Doanh số"]
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# Dự đoán tháng mới
st.subheader("🔍 Dự báo doanh số cho tháng tiếp theo")
new_month = st.slider("Chọn tháng mới để dự báo", 7, 12, 7)
new_pred = model.predict([[new_month]])[0]
st.success(f"📅 Dự báo doanh số tháng {new_month}: **{new_pred:,.0f}** VNĐ")

# Vẽ biểu đồ
st.subheader("📈 Biểu đồ doanh số & dự báo")
fig, ax = plt.subplots()
ax.plot(df["Tháng"], y, "o-b", label="Thực tế", linewidth=2)
ax.plot(df["Tháng"], y_pred, "--k", label="Dự báo", linewidth=2)

# Thêm điểm dự báo mới vào biểu đồ
ax.scatter(new_month, new_pred, color="red", s=100, label=f"Dự báo tháng {new_month}")
ax.set_xlabel("Tháng")
ax.set_ylabel("Doanh số (VNĐ)")
ax.set_title("Biểu đồ doanh số thực tế & dự báo")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Chỉ số đánh giá mô hình
st.subheader("📌 Chỉ số đánh giá mô hình")
st.markdown(f"""
- **MAE**: `{mean_absolute_error(y, y_pred):,.2f}`
- **RMSE**: `{np.sqrt(mean_squared_error(y, y_pred)):.2f}`
- **R² Score**: `{r2_score(y, y_pred):.2f}`
""")
