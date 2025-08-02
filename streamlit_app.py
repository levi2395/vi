# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

def create_bar_chart(df, column, title, xlabel, ylabel, rotation=0, color='skyblue'):
    """
    Tạo biểu đồ cột từ DataFrame.
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    df[column].value_counts().head(10).plot(kind='bar', ax=ax, color=color)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='x', rotation=rotation)
    st.pyplot(fig)

def create_pie_chart(df, column, title):
    """
    Tạo biểu đồ tròn từ DataFrame.
    """
    fig, ax = plt.subplots()
    df[column].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title(title)
    ax.set_ylabel('')
    st.pyplot(fig)

def create_histogram(df, column, title, xlabel, ylabel, color='orange'):
    """
    Tạo biểu đồ histogram từ DataFrame.
    """
    fig, ax = plt.subplots()
    sns.histplot(df[column], kde=True, ax=ax, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

def create_sales_volume_chart(df, groupby_col, title, xlabel, ylabel, rotation=0, color='green'):
    """
    Tạo biểu đồ doanh số trung bình.
    """
    fig, ax = plt.subplots()
    df.groupby(groupby_col)['Sales Volume'].mean().plot(kind='bar', ax=ax, color=color)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.tick_params(axis='x', rotation=rotation)
    st.pyplot(fig)

# Cấu hình trang Streamlit
st.set_page_config(page_title="Zara Data Visualization", layout="wide")
st.title("🛍️ Zara Fashion Sales Dashboard")

# Tải lên file CSV
uploaded_file = st.file_uploader("📤 Tải lên file Zara (.csv)", type=["csv"])

if uploaded_file:
    try:
        # Đọc dữ liệu từ file đã tải lên.
        # Sử dụng `StringIO` để xử lý tệp trong bộ nhớ.
        # Căn cứ vào file bạn đã gửi, dấu phân cách là ';'.
        df = pd.read_csv(uploaded_file, sep=';')
        
        st.success("Tải tệp lên thành công!")

        # Xem trước dữ liệu
        st.subheader("🔍 Xem trước dữ liệu")
        st.dataframe(df.head())

        st.subheader("📊 Biểu đồ trực quan hóa dữ liệu")

        # 1. Top 10 danh mục sản phẩm phổ biến
        create_bar_chart(df, 'Product Category', '1. Top 10 danh mục sản phẩm phổ biến', 'Danh mục sản phẩm', 'Số lượng', rotation=45, color='teal')

        # 2. Phân bố khuyến mãi (Promotion)
        create_pie_chart(df, 'Promotion', '2. Tỉ lệ khuyến mãi (Promotion)')

        # 3. Phân loại theo section (MAN, WOMAN)
        create_bar_chart(df, 'section', '3. Phân loại người mua (Section)', 'Phân loại', 'Số lượng', color='skyblue')

        # 4. Phân bố giá sản phẩm
        create_histogram(df, 'price', '4. Phân bố giá sản phẩm', 'Giá sản phẩm', 'Tần suất')

        # 5. Doanh số theo vị trí trưng bày
        create_sales_volume_chart(df, 'Product Position', '5. Doanh số theo vị trí trưng bày', 'Vị trí trưng bày', 'Doanh số trung bình', rotation=45)
        
    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi đọc file CSV: {e}")
        st.info("Vui lòng đảm bảo file CSV của bạn có dấu phân cách là ';' và chứa các cột cần thiết.")
