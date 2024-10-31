import streamlit as st
from components.request_form import render_request_form
from components.response_viewer import render_response_viewer
from components.performance_metrics import render_performance_metrics
from components.history_viewer import render_history_viewer
from components.health_monitor import render_health_monitor
from utils.config_manager import load_config, save_config

def main():
    st.set_page_config(
        page_title="REST API Tester",
        page_icon="🔌",
        layout="wide"
    )

    st.title("REST API Testing Tool")

    # Initialize session state
    if 'response' not in st.session_state:
        st.session_state.response = None
    if 'timing' not in st.session_state:
        st.session_state.timing = None

    # Create tabs for current request, history, and health monitoring
    tab1, tab2, tab3 = st.tabs(["Current Request", "History", "Health Monitoring"])
    
    with tab1:
        # Create two columns for the layout
        col1, col2 = st.columns([1, 1])

        with col1:
            st.header("Request Configuration")
            render_request_form()

            # Configuration management
            st.subheader("Save/Load Configuration")
            save_load_col1, save_load_col2 = st.columns(2)
            
            with save_load_col1:
                config_name = st.text_input("Configuration Name")
            
            with save_load_col2:
                if st.button("Save"):
                    save_config(config_name)
                if st.button("Load"):
                    load_config(config_name)

        with col2:
            if st.session_state.response:
                st.header("Response")
                render_response_viewer(st.session_state.response)
                render_performance_metrics(st.session_state.timing)
    
    with tab2:
        render_history_viewer()
        
    with tab3:
        render_health_monitor()

if __name__ == "__main__":
    main()
