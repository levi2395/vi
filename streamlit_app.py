# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import StringIO

# Cài đặt cấu hình trang
st.set_page_config(
    page_title="Streamlit Data Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tiêu đề của ứng dụng
st.title("Ứng dụng trực quan hóa dữ liệu")
st.markdown("Sử dụng các thư viện `pandas`, `matplotlib`, và `seaborn`.")

# Tải lên tệp CSV
uploaded_file = st.file_uploader("Tải lên tệp CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Đọc dữ liệu từ tệp đã tải lên
        df = pd.read_csv(uploaded_file)
        
        st.success("Tải tệp lên thành công!")

        # Hiển thị 5 dòng đầu tiên của dữ liệu
        st.subheader("Xem trước dữ liệu")
        st.dataframe(df.head())

        # Hiển thị thông tin về dữ liệu
        st.subheader("Thông tin về DataFrame")
        buffer = StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        # Lọc dữ liệu bằng thanh trượt
        st.sidebar.header("Lọc dữ liệu")
        selected_column = st.sidebar.selectbox("Chọn cột số:", df.select_dtypes(include=np.number).columns)
        
        if selected_column:
            min_val = float(df[selected_column].min())
            max_val = float(df[selected_column].max())
            filter_value = st.sidebar.slider(
                f"Lọc theo {selected_column}",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val)
            )
            df_filtered = df[(df[selected_column] >= filter_value[0]) & (df[selected_column] <= filter_value[1])]
            
            st.subheader(f"Dữ liệu đã lọc theo '{selected_column}'")
            st.dataframe(df_filtered)

            # Các biểu đồ trực quan hóa
            st.header("Trực quan hóa dữ liệu")

            # Biểu đồ 1: Biểu đồ phân bố (Histogram)
            st.subheader(f"Biểu đồ phân bố của '{selected_column}'")
            fig, ax = plt.subplots()
            sns.histplot(df_filtered[selected_column], kde=True, ax=ax)
            ax.set_title(f"Phân bố của {selected_column}")
            st.pyplot(fig)

            # Biểu đồ 2: Biểu đồ thanh (Bar Chart)
            st.subheader("Biểu đồ thanh")
            # Tìm một cột đối tượng (object) để tạo biểu đồ
            object_cols = df_filtered.select_dtypes(include=['object']).columns
            if len(object_cols) > 0:
                selected_bar_col = st.selectbox("Chọn cột cho biểu đồ thanh:", object_cols)
                if selected_bar_col:
                    fig, ax = plt.subplots()
                    df_filtered[selected_bar_col].value_counts().plot(kind='bar', ax=ax)
                    ax.set_title(f"Số lượng theo {selected_bar_col}")
                    st.pyplot(fig)
            else:
                st.info("Không tìm thấy cột đối tượng để tạo biểu đồ thanh.")
            
            # Biểu đồ 3: Biểu đồ hộp (Box Plot)
            st.subheader("Biểu đồ hộp")
            if len(object_cols) > 0:
                selected_box_col = st.selectbox("Chọn cột cho trục X của biểu đồ hộp:", object_cols)
                if selected_box_col:
                    fig, ax = plt.subplots()
                    sns.boxplot(x=selected_box_col, y=selected_column, data=df_filtered, ax=ax)
                    ax.set_title(f"Phân bố của {selected_column} theo {selected_box_col}")
                    st.pyplot(fig)
            else:
                st.info("Không tìm thấy cột đối tượng để tạo biểu đồ hộp.")

            # Biểu đồ 4: Biểu đồ mối tương quan (Heatmap)
            st.subheader("Biểu đồ mối tương quan")
            numeric_df = df_filtered.select_dtypes(include=np.number)
            if not numeric_df.empty and numeric_df.shape[1] > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
                ax.set_title("Biểu đồ mối tương quan giữa các cột số")
                st.pyplot(fig)
            else:
                st.info("Không đủ cột số để tạo biểu đồ mối tương quan.")

    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi xử lý tệp: {e}")
        st.info("Vui lòng đảm bảo tệp của bạn là CSV hợp lệ và không bị lỗi.")

