import streamlit as st
import warnings
from ui_manager import UIManager
from data_manager import DataManager
from page_manager import PageManager

warnings.filterwarnings('ignore')



class MainApp:
    def __init__(self):
        self.ui_manager = UIManager()
        self.data_manager = DataManager()
        self.page_manager = PageManager()

    def run(self):
        self.ui_manager.set_page_config()
        self.ui_manager.display_css()
        
        page = self.ui_manager.display_sidebar()

        if page == "🏠 Home":
            self.page_manager.display_home_page()
        elif page == "📂 Upload":
            self.data_manager.display_upload_page()
        elif page == "📊 Summary":
            self.page_manager.display_summary_page()
        elif page == "🧹 Clean":
            self.data_manager.display_clean_page()
        elif page == "Download Updated":
            self.data_manager.display_download_page()
        elif page == "📈 Visualize":
            self.page_manager.display_visualize_page()
        elif page == "🤖 Predict":
            self.page_manager.display_predict_page()
        elif page == "💬 Chat":
            self.page_manager.display_chat_page()
        elif page == "ℹ️ About":
            self.page_manager.display_about_page()

if __name__ == "__main__":
    app = MainApp()
    app.run()