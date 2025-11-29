import streamlit as st

class UIManager:
    def __init__(self):
        self.menu_items = [
            ("🏠 Home", "home"),
            ("📂 Upload", "upload"),
            ("📊 Summary", "summary"),
            ("🧹 Clean", "clean"),
            ("Download Updated","download"),
            ("📈 Visualize", "visualize"),
            ("🤖 Predict", "predict"),
            ("💬 Chat", "chat"),
            ("ℹ️ About", "about")
        ]

    def set_page_config(self):
        st.set_page_config(page_title="Power BI Dashboard", layout="wide", page_icon="📊")

    def display_css(self):
        st.markdown("""
            <style>
            /* Main container */
            .main {
                padding: 0rem 1rem;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
            }
            
            [data-testid="stSidebar"] .css-1d391kg {
                padding-top: 2rem;
            }
            
            /* Sidebar text color */
            [data-testid="stSidebar"] * {
                color: white !important;
            }
            
            /* Button styling */
            .stButton>button {
                width: 100%;
                border-radius: 10px;
                height: 3em;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.2);
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            }
            
            /* Sidebar buttons */
            [data-testid="stSidebar"] .stButton>button {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(10px);
                margin-bottom: 0.5rem;
            }
            
            [data-testid="stSidebar"] .stButton>button:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.4);
                transform: translateX(5px);
            }
            
            /* Active page button */
            [data-testid="stSidebar"] .stButton>button[kind="primary"] {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border: none;
            }
            
            /* Metric cards */
            [data-testid="stMetricValue"] {
                font-size: 2rem;
                font-weight: 700;
                color: #1e3c72;
            }
            
            .metric-card {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(0,0,0,0.15);
            }
            
            /* Headers */
            h1 {
                color: #1e3c72;
                font-weight: 800;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            
            h2, h3 {
                color: #2a5298;
                font-weight: 700;
            }
            
            /* Dataframe styling */
            [data-testid="stDataFrame"] {
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            
            /* Input fields */
            .stTextInput>div>div>input {
                border-radius: 10px;
                border: 2px solid #667eea;
                padding: 10px;
            }
            
            .stSelectbox>div>div>select {
                border-radius: 10px;
                border: 2px solid #667eea;
            }
            
            /* File uploader */
            [data-testid="stFileUploader"] {
                border-radius: 15px;
                border: 2px dashed #667eea;
                padding: 2rem;
                background: rgba(102, 126, 234, 0.05);
            }
            
            /* Success/Error messages */
            .stSuccess {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: white;
                border-radius: 10px;
                padding: 1rem;
            }
            
            .stError {
                background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                color: white;
                border-radius: 10px;
                padding: 1rem;
            }
            
            .stWarning {
                background: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
                color: white;
                border-radius: 10px;
                padding: 1rem;
            }
            
            .stInfo {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                padding: 1rem;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
                font-weight: 600;
            }
            
            /* Chat messages */
            .chat-user {
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 15px;
                border-radius: 15px;
                margin: 10px 0;
                border-left: 4px solid #2196F3;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .chat-assistant {
                background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
                padding: 15px;
                border-radius: 15px;
                margin: 10px 0;
                border-left: 4px solid #4CAF50;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            /* Spinner */
            .stSpinner > div {
                border-top-color: #667eea !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
            }
            
            .stTabs [data-baseweb="tab"] {
                border-radius: 10px 10px 0 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-weight: 600;
            }
            
            /* Cards */
            .card {
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                margin: 10px 0;
                transition: all 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }
            
            /* Sidebar logo area */
            .sidebar-logo {
                text-align: center;
                padding: 1rem;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                margin-bottom: 1rem;
            }
            
            /* Progress bar */
            .stProgress > div > div > div {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            }
            
            /* Checkbox */
            .stCheckbox {
                color: #1e3c72;
            }
            
            /* Radio buttons */
            .stRadio > label {
                color: #1e3c72;
                font-weight: 600;
            }
            </style>
            """, unsafe_allow_html=True)

    def display_sidebar(self):
        st.sidebar.markdown("""
            <div style="text-align: center; padding: 1.5rem 0; background: rgba(255,255,255,0.1); border-radius: 15px; margin-bottom: 1rem;">
                <h1 style="color: white; font-size: 2rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">📊</h1>
                <h2 style="color: white; font-size: 1.3rem; margin: 0.5rem 0 0 0; font-weight: 700;">Power BI</h2>
                <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.3rem 0 0 0;">AI Data Intelligence</p>
            </div>
        """, unsafe_allow_html=True)

        st.sidebar.markdown("### 🧭 Navigation")

        if "page" not in st.session_state:
            st.session_state.page = "🏠 Home"

        for label, key in self.menu_items:
            is_current = st.session_state.page == label
            if st.sidebar.button(label, key=f"nav_{key}", type="primary" if is_current else "secondary"):
                st.session_state.page = label
                st.rerun()

        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Dataset Status")

        if "df" in st.session_state:
            st.sidebar.markdown("""
                <div style="background: rgba(76, 175, 80, 0.2); padding: 1rem; border-radius: 10px; border-left: 4px solid #4CAF50;">
                    <p style="margin: 0; color: white;"><strong>✅ Data Loaded</strong></p>
                </div>
            """, unsafe_allow_html=True)
            st.sidebar.metric("📝 Rows", f"{len(st.session_state.df):,}")
            st.sidebar.metric("📋 Columns", f"{len(st.session_state.df.columns)}")
            # Show cleaned status if the current df is different from the original
            if not st.session_state.df.equals(st.session_state.original_df):
                st.sidebar.markdown("""
                    <div style="background: rgba(33, 150, 243, 0.2); padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                        <p style="margin: 0; color: white; font-size: 0.9rem;"><strong>🧹 Cleaned</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            if "model" in st.session_state:
                st.sidebar.markdown("""
                    <div style="background: rgba(156, 39, 176, 0.2); padding: 0.5rem; border-radius: 8px; margin-top: 0.5rem;">
                        <p style="margin: 0; color: white; font-size: 0.9rem;"><strong>🤖 Model Ready</strong></p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.sidebar.markdown("""
                <div style="background: rgba(255, 152, 0, 0.2); padding: 1rem; border-radius: 10px; border-left: 4px solid #FF9800;">
                    <p style="margin: 0; color: white;"><strong>⚠️ No Data</strong></p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem; color: rgba(255,255,255,0.8);">Upload a file to start</p>
                </div>
            """, unsafe_allow_html=True)

        st.sidebar.markdown("---")
        st.sidebar.markdown("""
            <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 10px;">
                <p style="margin: 0; font-size: 0.9rem; color: rgba(255,255,255,0.7);">Built with ❤️</p>
                <p style="margin: 0.3rem 0 0 0; font-weight: 600; color: white;">Streamlit + ML</p>
                <p style="margin: 0.3rem 0 0 0; font-size: 0.8rem; color: rgba(255,255,255,0.6);">Version 2.0</p>
            </div>
        """, unsafe_allow_html=True)

        return st.session_state.page
