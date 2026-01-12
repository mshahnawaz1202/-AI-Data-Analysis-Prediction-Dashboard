# AI-Powered Data Intelligence Platform

This project is a comprehensive, AI-powered data analysis and business intelligence platform built with Streamlit. It provides an end-to-end workflow for data professionals, from uploading and cleaning data to visualization, machine learning, and interactive querying through a natural language chat interface.

## 🚀 Key Features

- **📂 Smart Data Upload**: Ingest data from various formats including CSV, Excel, and JSON.
- **📊 Automated Summary**: Get instant statistical and structural summaries of your dataset.
- **🧹 Advanced Cleaning Tools**: Interactively handle duplicates and missing values with multiple strategies.
- **📈 Interactive Visualizations**: Generate a wide range of plots (Bar, Line, Scatter, etc.) with customizable themes.
- **🤖 Integrated Machine Learning**: Train, evaluate, and predict with regression and classification models directly in the app.
- **💬 Chat with Your Data**: An intelligent assistant that answers natural language questions about your dataset, providing instant insights and analysis.
- **📥 Data Export**: Download your cleaned and processed data for offline use.

## 🛠️ Tech Stack

- **Framework**: Streamlit
- **Data Manipulation**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Data Visualization**: Matplotlib

## 📦 Installation

Ensure you have Python 3.8+ installed. Clone the repository and install the required dependencies using pip.

```bash
pip install streamlit pandas numpy scikit-learn matplotlib openpyxl
```

## 🏃‍♀️ How to Run

To run the application, navigate to the project directory in your terminal and execute the following command:

```bash
streamlit run d:/AI/main.py
```

Your default web browser will open with the application running at `http://localhost:8501`.

---

## 📂 File Structure

The project is organized into a modular, class-based structure to ensure scalability and maintainability.

```
d:/AI/
├── main.py           # Main application entry point. Orchestrates the app flow.
├── ui_manager.py     # Manages all UI components, including the sidebar and CSS styling.
├── data_manager.py   # Handles data I/O: uploading, cleaning, and downloading.
├── page_manager.py   # Contains the logic and content for each distinct page.
├── utils.py          # Stores helper functions used across different modules (e.g., preprocessing).
└── README.md         # This documentation file.
```

---

## 🌊 Project Flow

The application follows a logical, user-centric flow, managed by a central controller in `main.py`.

1.  **Initialization (`main.py`)**:
    - When the app starts, `main.py` creates an instance of `MainApp`.
    - The `MainApp` class initializes three key managers: `UIManager`, `DataManager`, and `PageManager`.

2.  **UI Rendering (`ui_manager.py`)**:
    - The `UIManager` sets the page configuration (title, layout) and injects custom CSS for styling.
    - It then renders the main navigation sidebar. The user's page selection is stored in `st.session_state.page`.

3.  **Page Routing (`main.py`)**:
    - The `run()` method in `MainApp` checks the value of `st.session_state.page`.
    - Based on the selected page, it calls the appropriate method from either `PageManager` or `DataManager` to render the content.

4.  **User Journey & Data Flow**:

    - **`📂 Upload` (`data_manager.py`)**:
        - The user uploads a file (CSV, Excel, JSON).
        - `DataManager.display_upload_page()` reads the file into a Pandas DataFrame.
        - The original DataFrame is stored in `st.session_state.df` for future use.

    - **`🧹 Clean` (`data_manager.py`)**:
        - The user selects cleaning options (e.g., remove duplicates, handle missing values).
        - `DataManager.display_clean_page()` applies these transformations.
        - The resulting cleaned DataFrame is stored in `st.session_state.cleaned_df`.

    - **`📊 Summary`, `📈 Visualize`, `🤖 Predict`, `💬 Chat` (`page_manager.py`)**:
        - When the user navigates to one of these pages, the corresponding method in `PageManager` is called.
        - Each method first calls `_get_active_df()` to retrieve the most up-to-date DataFrame (preferring `cleaned_df` if it exists).
        - **Summary**: Displays statistical overviews using functions from `utils.py`.
        - **Visualize**: Renders plots based on user selections.
        - **Predict**: Uses `preprocess_data()` from `utils.py` to prepare data, trains a scikit-learn model, and displays performance.
        - **Chat**: Uses `analyze_query_and_respond()` from `utils.py` to process natural language queries against the active DataFrame.

5.  **Helper Functions (`utils.py`)**:
    - This file contains stateless, reusable functions that are imported by other modules.
    - `preprocess_data()`: A crucial function used by the **Predict** page to prepare data for machine learning.
    - `analyze_query_and_respond()`: The core logic behind the **Chat** page's AI capabilities.

This modular architecture ensures that each part of the application has a single responsibility, making the code clean, easy to debug, and simple to extend.

---



