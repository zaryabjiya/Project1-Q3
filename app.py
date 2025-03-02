import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="🧹 Data Sweeper", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
        .stApp {
            background-color: black;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧹 Datasweeper Sterling Integrator By Zaryab Irfan 🚀")
st.write("🔄 Transform your files between CSV and Excel formats with built-in data cleaning and visualization. 📊")

uploading_files = st.file_uploader("📂 Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploading_files:
    for file in uploading_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        st.write(f"🔍 **Preview of {file.name}:**")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"🧼 Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"🩹 Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values filled!")

        # Column Selection
        st.subheader("📊 Select Columns to Keep")
        columns = st.multiselect(f"🎯 Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Shape Check
        st.write(f"📏 **Data shape after processing:** {df.shape}")
        if df.empty:
            st.write("⚠ No data available after processing! Skipping visualization.")
            continue

        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show visualization for {file.name}"):
            numeric_df = df.select_dtypes(include='number')
            if not numeric_df.empty:
                st.bar_chart(numeric_df)
            else:
                st.write("⚠ No numeric data available for visualization.")

        # Conversion Options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"📤 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"📥 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ 🎉 All files processed successfully! 🚀")


