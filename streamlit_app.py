import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Zara Sales Dashboard", layout="wide")
sns.set(style="whitegrid")

st.title("🛍️ Zara Sales Dashboard")
st.markdown("Phân tích dữ liệu sản phẩm Zara: thương hiệu, danh mục, mùa vụ và doanh số.")

# ----------------------------
# Upload dữ liệu
# ----------------------------
st.sidebar.header("📂 Tải dữ liệu CSV")
file = st.sidebar.file_uploader("Tải file dữ liệu .csv", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.success("✅ Dữ liệu đã được tải thành công.")
    st.dataframe(df.head(), use_container_width=True)

    # Tabs phân tích
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Thương hiệu",
        "📁 Danh mục sản phẩm",
        "🌦️ Mùa vụ",
        "📈 Doanh số & Giá"
    ])

    # ====================================
    # Tab 1: Thương hiệu
    # ====================================
    with tab1:
        st.subheader("Top 10 Thương hiệu có nhiều sản phẩm nhất")
        if 'brand' in df.columns:
            brand_counts = df['brand'].value_counts().head(10)
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            sns.barplot(x=brand_counts.index, y=brand_counts.values, palette='viridis', ax=ax1)
            ax1.set_title("Top 10 Thương hiệu")
            ax1.set_ylabel("Số lượng sản phẩm")
            ax1.tick_params(axis='x', rotation=45)
            st.pyplot(fig1)
        else:
            st.warning("Không có cột 'brand' trong dữ liệu.")

    # ====================================
    # Tab 2: Danh mục sản phẩm
    # ====================================
    with tab2:
        st.subheader("Giá trung bình theo danh mục sản phẩm")
        if 'Product Category' in df.columns and 'price' in df.columns:
            avg_price = df.groupby("Product Category")['price'].mean().sort_values(ascending=False).head(10)
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            sns.barplot(x=avg_price.index, y=avg_price.values, palette='magma', ax=ax2)
            ax2.set_ylabel("Giá trung bình")
            ax2.set_xlabel("Danh mục")
            ax2.tick_params(axis='x', rotation=45)
            ax2.set_title("Top 10 Danh mục theo giá trung bình")
            st.pyplot(fig2)
        else:
            st.warning("Không tìm thấy cột 'Product Category' hoặc 'price'.")

    # ====================================
    # Tab 3: Mùa vụ
    # ====================================
    with tab3:
        st.subheader("Phân bố doanh số theo mùa vụ")
        if 'Seasonal' in df.columns and 'Sales Volume' in df.columns:
            fig3, ax3 = plt.subplots(figsize=(8, 4))
            sns.boxplot(data=df, x='Seasonal', y='Sales Volume', palette='Set2', ax=ax3)
            ax3.set_title("Boxplot doanh số theo mùa vụ")
            ax3.set_xlabel("Mùa vụ")
            ax3.set_ylabel("Sales Volume")
            st.pyplot(fig3)
        else:
            st.warning("Không tìm thấy cột 'Seasonal' hoặc 'Sales Volume'.")

    # ====================================
    # Tab 4: Doanh số & Giá theo thời gian
    # ====================================
    with tab4:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Phân phối doanh số")
            if 'Sales Volume' in df.columns:
                fig4, ax4 = plt.subplots(figsize=(8, 4))
                sns.histplot(df['Sales Volume'], kde=True, color='skyblue', ax=ax4)
                ax4.set_title("Phân phối Sales Volume")
                ax4.set_xlabel("Sales Volume")
                st.pyplot(fig4)
            else:
                st.warning("Không có cột 'Sales Volume'.")

        with col2:
            st.subheader("Xu hướng giá theo thời gian")
            if 'scraped_at' in df.columns and 'price' in df.columns:
                df['scraped_at'] = pd.to_datetime(df['scraped_at'], errors='coerce')
                price_by_time = df.groupby('scraped_at')['price'].mean().reset_index()

                fig5, ax5 = plt.subplots(figsize=(8, 4))
                sns.lineplot(data=price_by_time, x='scraped_at', y='price', marker='o', ax=ax5)
                ax5.set_title("Giá trung bình theo thời gian")
                ax5.set_ylabel("Giá trung bình")
                ax5.set_xlabel("Thời gian")
                ax5.tick_params(axis='x', rotation=45)
                st.pyplot(fig5)
            else:
                st.warning("Không tìm thấy cột 'scraped_at' hoặc 'price'.")

else:
    st.info("📌 Vui lòng tải lên file dữ liệu CSV để bắt đầu.")
