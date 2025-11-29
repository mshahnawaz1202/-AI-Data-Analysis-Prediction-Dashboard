import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import io
from utils import show_overview_cards, preprocess_data, analyze_query_and_respond

class PageManager:
    def _get_active_df(self):
        if "df" in st.session_state:
            return st.session_state.df
        else:
            st.warning("⚠️ Please upload a dataset first.")
            return None

    def display_home_page(self):
        st.title("🌟 BitBros Data Destroyer (but it actually cleans)")
        st.markdown("### Welcome to AI-Powered Data Intelligence Platform")
        col1, col2, col3 = st.columns([1, 2, 3])

        with col1:
            st.markdown("""
            ### 🚀 Key Features:
            
            **📂 Data Management**
            - Upload CSV, Excel, or JSON files
            - Automatic data type detection
            - Preview and explore your data
            
            **🧹 Data Cleaning**
            - Remove duplicate records
            - Handle missing values
            - Data type conversion
            
            **📈 Visualization**
            - Multiple chart types
            - Interactive plots
            - Custom styling
            
            **🤖 Machine Learning**
            - Regression models (predict continuous values)
            - Classification models (predict categories)
            - Model performance metrics
            
            **💬 Chat with Data**
            - Natural language queries
            - Instant insights
            - Statistical summaries
            """)

        with col3:
            st.markdown("""
            ### 📌 Quick Start
            
            1. **Upload** your data file
            2. **Clean** your data
            3. **Visualize** insights
            4. **Predict** outcomes
            5. **Chat** with your data
            
            ### 🛠️ Tech Stack
            - Streamlit
            - Pandas
            - NumPy
            - Matplotlib
            - Scikit-learn
            """)

    def display_summary_page(self):
        st.header("📊 Data Summary & Statistics")
        df = self._get_active_df()
        if df is None:
            st.stop()

        try:
            show_overview_cards(df)
            st.markdown("---")
            
            st.subheader("📈 Numerical Statistics")
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                st.dataframe(numeric_df.describe().style.format("{:.2f}"))
                st.subheader("📊 Additional Metrics")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Variance**")
                    st.dataframe(numeric_df.var().to_frame(name="Variance").style.format("{:.2f}"))
                with col2:
                    st.markdown("**Skewness**")
                    st.dataframe(numeric_df.skew().to_frame(name="Skewness").style.format("{:.2f}"))
            else:
                st.info("No numeric columns found.")

            st.subheader("🏷️ Categorical Columns")
            categorical_df = df.select_dtypes(include=['object'])
            if not categorical_df.empty:
                cat_stats = pd.DataFrame({
                    "Column": categorical_df.columns,
                    "Unique Values": [categorical_df[col].nunique() for col in categorical_df.columns],
                    "Most Frequent": [categorical_df[col].mode()[0] if not categorical_df[col].mode().empty else "N/A" for col in categorical_df.columns],
                    "Frequency": [categorical_df[col].value_counts().iloc[0] if not categorical_df.empty else 0 for col in categorical_df.columns]
                })
                st.dataframe(cat_stats)
            else:
                st.info("No categorical columns found.")
        except Exception as e:
            st.error(f"❌ Error generating summary: {str(e)}")

    def display_visualize_page(self):
        st.header("📈 Data Visualization")
        data = self._get_active_df()
        if data is None:
            st.stop()

        try:
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()

            if not numeric_cols:
                st.warning("⚠️ No numeric columns available for visualization.")
                st.stop()

            theme_colors = {
                "Blue": {"color": "#1f77b4", "edge": "#0d3c61"},
                "Green": {"color": "#2ca02c", "edge": "#145214"},
                "Purple": {"color": "#9467bd", "edge": "#4b2a6e"},
                "Orange": {"color": "#ff7f0e", "edge": "#b04e00"},
                "Dark": {"color": "#444444", "edge": "#222222"},
            }

            col_theme, col_chart = st.columns(2)
            with col_theme:
                theme = st.selectbox("🎨 Chart Theme", list(theme_colors.keys()))
            colors = theme_colors[theme]

            with col_chart:
                chart_type = st.selectbox("📊 Chart Type", ["Line", "Bar", "Scatter", "Histogram", "Box Plot", "Pie Chart"])

            if chart_type in ["Line", "Bar", "Scatter"]:
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols)
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols)
            elif chart_type in ["Histogram", "Box Plot"]:
                selected_col = st.selectbox("Select Column", numeric_cols)
            elif chart_type == "Pie Chart":
                if not categorical_cols:
                    st.warning("⚠️ No categorical columns for pie chart.")
                    st.stop()
                selected_cat = st.selectbox("Select Category", categorical_cols)

            if st.button("🎨 Generate Visualization", type="primary"):
                fig, ax = plt.subplots(figsize=(10, 6))

                if chart_type == "Bar":
                    x_data = data[x_col].head(20)
                    y_data = data[y_col].head(20)
                    ax.bar(range(len(x_data)), y_data, color=colors["color"], edgecolor=colors["edge"])
                    ax.set_xticks(range(len(x_data)))
                    ax.set_xticklabels([f"{v:.1f}" for v in x_data], rotation=45)
                    ax.set_title(f"Bar Chart: {y_col} vs {x_col}")
                elif chart_type == "Line":
                    ax.plot(data[x_col], data[y_col], color=colors["color"], linewidth=2, marker="o")
                    ax.set_title(f"Line Chart: {y_col} vs {x_col}")
                elif chart_type == "Scatter":
                    ax.scatter(data[x_col], data[y_col], color=colors["color"], alpha=0.7, s=60, edgecolor=colors["edge"])
                    ax.set_title(f"Scatter: {y_col} vs {x_col}")
                elif chart_type == "Histogram":
                    ax.hist(data[selected_col].dropna(), bins=30, color=colors["color"], edgecolor=colors["edge"], alpha=0.8)
                    ax.set_title(f"Histogram: {selected_col}")
                elif chart_type == "Box Plot":
                    ax.boxplot(data[selected_col].dropna(), patch_artist=True, boxprops=dict(facecolor=colors["color"], edgecolor=colors["edge"]))
                    ax.set_title(f"Box Plot: {selected_col}")
                elif chart_type == "Pie Chart":
                    pie_data = data[selected_cat].value_counts()
                    ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", colors=plt.cm.Set3.colors, startangle=90)
                    ax.set_title(f"Pie Chart: {selected_cat}")

                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)

                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
                st.download_button("📥 Download PNG", data=buf, file_name=f"{chart_type.replace(' ', '_')}.png", mime="image/png")
                plt.close(fig)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    def display_predict_page(self):
        st.header("🤖 Machine Learning Predictions")
        df = self._get_active_df()
        if df is None:
            st.stop()

        st.subheader("🎯 Model Configuration")
        target_col = st.selectbox("Select Target Column (what to predict)", df.columns)

        if df[target_col].dtype == object or df[target_col].nunique() < 10:
            problem_type = "Classification"
        else:
            problem_type = st.radio("Problem Type", ["Regression", "Classification"])

        X_raw = df.drop(columns=[target_col])
        y_raw = df[target_col]

        target_encoder = None
        if problem_type == "Classification" and y_raw.dtype == object:
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y_raw)
        else:
            y = y_raw.copy()

        X = preprocess_data(X_raw)

        if problem_type == "Regression":
            model_choice = st.selectbox("Model", ["Linear Regression", "Random Forest"])
        else:
            model_choice = st.selectbox("Model", ["Logistic Regression", "Random Forest"])

        test_size = st.slider("Test Size (%)", 10, 40, 20) / 100
        random_state = st.number_input("Random Seed", value=42)

        if st.button("🚀 Train Model", type="primary"):
            try:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=int(random_state))

                if problem_type == "Regression":
                    model = LinearRegression() if model_choice == "Linear Regression" else RandomForestRegressor(n_estimators=150, random_state=random_state)
                else:
                    model = LogisticRegression(max_iter=2000) if model_choice == "Logistic Regression" else RandomForestClassifier(n_estimators=150, random_state=random_state)

                model.fit(X_train, y_train)
                st.success("✅ Model trained successfully!")

                st.session_state.model = model
                st.session_state.target_encoder = target_encoder
                st.session_state.X_columns = X.columns.tolist()
                st.session_state.preprocess_func = preprocess_data
                st.session_state.target_col = target_col

                st.subheader("📊 Model Performance")
                y_pred = model.predict(X_test)
                if problem_type == "Regression":
                    r2 = r2_score(y_test, y_pred)
                    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                    st.metric("R² Score", f"{r2:.4f}")
                    st.metric("RMSE", f"{rmse:.4f}")
                else:
                    accuracy = accuracy_score(y_test, y_pred)
                    st.metric("Accuracy", f"{accuracy:.4f}")
                    st.write(pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose())

            except Exception as e:
                st.error(f"❌ Training Error: {str(e)}")

        if "model" in st.session_state:
            st.markdown("---")
            st.subheader("🔮 Predict on New Input")

            input_values = {}
            cols = st.columns(2)
            for i, col in enumerate(X_raw.columns):
                with cols[i % 2]:
                    dtype = X_raw[col].dtype
                    if dtype == object:
                        options = X_raw[col].dropna().unique().tolist()
                        input_values[col] = st.selectbox(f"Input for {col}", options, key=f"input_{col}")
                    elif dtype == bool:
                        input_values[col] = st.selectbox(f"Input for {col}", [True, False], key=f"input_{col}")
                    elif np.issubdtype(dtype, np.datetime64):
                        input_values[col] = st.date_input(f"Input for {col}", key=f"input_{col}")
                    elif np.issubdtype(dtype, np.number):
                        input_values[col] = st.number_input(f"Input for {col}", value=float(X_raw[col].mean()), key=f"input_{col}")
                    else:
                        input_values[col] = st.text_input(f"Input for {col}", key=f"input_{col}")

            if st.button("🎯 Predict"):
                try:
                    input_df = pd.DataFrame([input_values])
                    preprocess = st.session_state.preprocess_func
                    input_processed = preprocess(input_df)

                    for col in st.session_state.X_columns:
                        if col not in input_processed:
                            input_processed[col] = 0
                    input_processed = input_processed[st.session_state.X_columns]

                    prediction = st.session_state.model.predict(input_processed)[0]

                    if st.session_state.target_encoder:
                        prediction = st.session_state.target_encoder.inverse_transform([int(prediction)])[0]

                    st.success(f"🎉 Prediction: **{prediction}**")

                except Exception as e:
                    st.error(f"❌ Prediction Error: {str(e)}")

    def display_chat_page(self):
        st.header("💬 Chat with Your Data")
        st.markdown("### 🤖 Intelligent Data Assistant")
        data = self._get_active_df()
        if data is None:
            st.stop()

        try:
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [{
                    "role": "assistant",
                    "content": f"""👋 Hello! I'm your intelligent data assistant. I've analyzed your dataset:
    **📊 Quick Facts:**
    - **{len(data):,}** rows × **{len(data.columns)}** columns
    - **{len(data.select_dtypes(include=[np.number]).columns)}** numeric columns
    - **{data.isnull().sum().sum()}** missing values total
    **💡 I can help you with:**
    - Deep insights and analysis, Column-specific information, Correlation and relationship analysis, Outlier detection, Data cleaning recommendations, Feature selection for ML, Statistical summaries
    **Ask me anything!** I understand natural language queries."""
                }]

            with st.expander("💡 Example Questions"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    **📊 Analysis Questions:**
                    - "Give me insights about this data"
                    - "What can you tell me about [column]?"
                    - "Are there any outliers?"
                    - "Analyze the distribution"
                    """)
                with col2:
                    st.markdown("""
                    **🧹 Recommendations:**
                    - "What cleaning steps should I take?"
                    - "Which features are good for prediction?"
                    - "Show correlation analysis"
                    """)

            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("What is up?"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("🤔 Analyzing..."):
                        response = analyze_query_and_respond(data, prompt)
                        st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"❌ Error in chat module: {str(e)}")

    def display_about_page(self):
        st.header("ℹ️ About This Dashboard")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### 🎯 Project Overview
            This **Power BI-style Analytics Dashboard** is a comprehensive data analysis platform built with modern Python libraries. It provides end-to-end data analytics capabilities from data ingestion to machine learning predictions.
            
            ### 🛠️ Technology Stack
            - **Streamlit**: Web application framework
            - **Pandas**: Data manipulation and analysis
            - **NumPy**: Numerical computations
            - **Matplotlib**: Data visualization
            - **Scikit-learn**: Machine learning models
            
            ### ✨ Key Features
            **1. Data Management**: Support for CSV, Excel, and JSON formats.
            **2. Data Cleaning**: Duplicate removal and missing value handling.
            **3. Visualization**: Interactive charts and professional styling.
            **4. Machine Learning**: Regression and Classification models.
            **5. Interactive Chat**: Natural language queries for instant insights.
            
            ### 🎓 Use Cases
            - **Business Analytics**: Sales forecasting, customer segmentation.
            - **Data Science**: Exploratory data analysis, model prototyping.
            - **Education**: Learning data science concepts.
            
            ### 🚀 Getting Started
            1. **Upload** your dataset.
            2. **Clean** your data.
            3. **Visualize** patterns and trends.
            4. **Train** ML models for predictions.
            5. **Chat** with your data for quick insights.
            """)
        with col2:
            st.markdown("""
            ### 📌 Quick Tips
            **Data Upload**: Ensure proper formatting and remove special characters.
            **Data Cleaning**: Always backup original data and remove duplicates first.
            **Visualization**: Choose appropriate chart types and use colors meaningfully.
            **ML Predictions**: Clean data first and use 20-30% for testing.
            **Chat Feature**: Ask specific questions and use clear language.
            
            ### 📞 Support
            For issues or suggestions, check your data format and review error messages.
            
            ### 🔄 Version
            **v2.0**
            - Enhanced error handling
            - ML prediction module
            - Chat with data feature
            - Improved UI/UX
            """)
        st.markdown("---")
        st.info("💡 **Tip**: Start with the Upload page and explore your data step by step!")
