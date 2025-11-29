import streamlit as st
import pandas as pd
import numpy as np
import io

class DataManager:
    def display_upload_page(self):
        st.header("📂 Upload Your Dataset")

        file = st.file_uploader(
            "Choose a file",
            type=["csv", "xlsx", "json"],
            help="Upload CSV, Excel, or JSON files"
        )

        if file:
            try:
                if file.name.endswith(".csv"):
                    df = pd.read_csv(file)
                    st.success(f"✅ Successfully loaded CSV file: {file.name}")
                elif file.name.endswith(".xlsx"):
                    df = pd.read_excel(file)
                    st.success(f"✅ Successfully loaded Excel file: {file.name}")
                elif file.name.endswith(".json"):
                    df = pd.read_json(file)
                    st.success(f"✅ Successfully loaded JSON file: {file.name}")
                else:
                    st.error("❌ Unsupported file format")
                    st.stop()

                st.session_state.df = df
                st.session_state.original_df = df.copy()

                st.subheader("📋 Data Overview")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", f"{df.shape[0]:,}")
                with col2:
                    st.metric("Columns", f"{df.shape[1]}")
                with col3:
                    st.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")

                st.subheader("👀 Data Preview")
                st.dataframe(df.head(10))

                st.subheader("🔍 Column Information")
                info_df = pd.DataFrame({
                    "Column": df.columns,
                    "Type": df.dtypes.astype(str),
                    "Non-Null": df.count(),
                    "Null Count": df.isnull().sum(),
                    "Null %": (df.isnull().sum() / len(df) * 100).round(2),
                    "Unique": df.nunique()
                })
                st.dataframe(info_df)

            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                st.info("💡 Please ensure your file is properly formatted.")
        else:
            st.info("👆 Upload a file to get started")

    
    def display_clean_page(self):
        st.header("🧹 Data Cleaning Tools")

        if "df" not in st.session_state:
            st.warning("⚠️ Please upload data first")
            st.stop()

        try:
            df = st.session_state.df.copy()
            st.subheader("📋 Original Data Preview")
            st.dataframe(df.head())

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔧 Cleaning Options")
                remove_dup = st.checkbox("Remove Duplicate Rows")
                handle_missing = st.selectbox(
                    "Handle Missing Values",
                    ["None", "Drop rows with any missing", "Drop rows with all missing", 
                     "Fill with mean (numeric only)", "Fill with median (numeric only)", "Fill with mode (all types)"]
                )

            with col2:
                st.subheader("📊 Data Quality")
                duplicates = df.duplicated().sum()
                missing = df.isnull().sum().sum()
                st.metric("Duplicate Rows", duplicates)
                st.metric("Total Missing Values", missing)

            if st.button("🚀 Apply Cleaning", type="primary"):
                cleaned_df = df.copy()
                changes = []

                if remove_dup and duplicates > 0:
                    before_dup = len(cleaned_df)
                    cleaned_df = cleaned_df.drop_duplicates()
                    changes.append(f"✅ Removed {before_dup - len(cleaned_df)} duplicate rows")

                if handle_missing != "None":
                    missing_before = cleaned_df.isnull().sum().sum()
                    if handle_missing == "Drop rows with any missing":
                        before = len(cleaned_df)
                        cleaned_df = cleaned_df.dropna()
                        changes.append(f"✅ Dropped {before - len(cleaned_df)} rows with missing values")
                    elif handle_missing == "Drop rows with all missing":
                        before = len(cleaned_df)
                        cleaned_df = cleaned_df.dropna(how='all')
                        changes.append(f"✅ Dropped {before - len(cleaned_df)} rows with all missing values")
                    else:
                        for col in cleaned_df.columns:
                            if cleaned_df[col].isnull().any():
                                if handle_missing == "Fill with mean (numeric only)" and np.issubdtype(cleaned_df[col].dtype, np.number):
                                    cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)
                                elif handle_missing == "Fill with median (numeric only)" and np.issubdtype(cleaned_df[col].dtype, np.number):
                                    cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
                                elif handle_missing == "Fill with mode (all types)":
                                    mode_val = cleaned_df[col].mode()
                                    if not mode_val.empty:
                                        cleaned_df[col] = cleaned_df[col].fillna(mode_val[0])
                        missing_after = cleaned_df.isnull().sum().sum()
                        if missing_after < missing_before:
                            changes.append(f"✅ Handled {missing_before - missing_after} missing values using: {handle_missing}")

                # Update the main dataframe to the cleaned version
                st.session_state.df = cleaned_df

                st.success("Data cleaning completed!")
                for change in changes:
                    st.write(change)

                st.subheader("✨ Cleaned Data Preview")
                st.dataframe(cleaned_df.head())

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Original Rows", len(st.session_state.original_df))
                with col2:
                    st.metric("Cleaned Rows", len(cleaned_df))

        except Exception as e:
            st.error(f"❌ Error during cleaning: {str(e)}")

    def display_download_page(self):
        st.header("📥 Download & Export Data")

        if "df" not in st.session_state:
            st.warning("⚠️ No data available to download. Please upload a file first.")
            return

        df = st.session_state.df

        st.subheader("📊 Current Data Overview")
        st.metric("Rows", f"{len(df):,}")
        st.metric("Columns", f"{len(df.columns)}")
        st.metric("Missing Values", f"{df.isnull().sum().sum():,}")

        st.subheader("📝 Data Preview")
        st.dataframe(df.head(10))

        st.subheader("⚙️ Select Download Format")
        download_format = st.selectbox("Choose a format", ["CSV", "Excel", "JSON"])

        if download_format == "CSV":
            data = df.to_csv(index=False).encode('utf-8')
            mime = "text/csv"
            file_ext = "csv"
        elif download_format == "Excel":
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='CleanedData')
            data = output.getvalue()
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            file_ext = "xlsx"
        elif download_format == "JSON":
            data = df.to_json(orient="records", indent=4).encode('utf-8')
            mime = "application/json"
            file_ext = "json"
        
        st.download_button(
            label=f"📥 Download as {download_format}",
            data=data,
            file_name=f"processed_data.{file_ext}",
            mime=mime,
            type="primary"
        )
