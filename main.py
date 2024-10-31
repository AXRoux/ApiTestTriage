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
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Load custom CSS
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Custom header with embedded SVG and creator attribution
    st.markdown(
        """
        <div class="main-header">
            <svg width="50" height="50" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <rect x="10" y="10" width="80" height="80" rx="10" fill="#FF4B4B"/>
                <path d="M30 50h40M50 30v40" stroke="white" stroke-width="8" stroke-linecap="round"/>
            </svg>
            <div>
                <h1>REST API Testing Tool</h1>
                <p>Test, monitor, and analyze your API endpoints</p>
            </div>
            <div class="creator-info">
                <p>Created by <a href="https://www.linkedin.com/in/rachel-chen" target="_blank">Rachel Chen</a></p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state
    if 'response' not in st.session_state:
        st.session_state.response = None
    if 'timing' not in st.session_state:
        st.session_state.timing = None

    # Create tabs with custom styling
    tabs = st.tabs([
        "🔧 Current Request",
        "📜 History",
        "🔍 Health Monitoring"
    ])
    
    with tabs[0]:
        # Main content columns
        left_col, right_col = st.columns([1, 1])

        with left_col:
            # Request Configuration Section
            st.markdown("<div class='form-section'>", unsafe_allow_html=True)
            st.subheader("Request Configuration")
            render_request_form()
            st.markdown("</div>", unsafe_allow_html=True)

            # Configuration Management Section
            st.markdown("<div class='form-section'>", unsafe_allow_html=True)
            st.subheader("Configuration Management")
            config_name = st.text_input("Configuration Name")
            
            if st.button("💾 Save Configuration"):
                save_config(config_name)
            if st.button("📂 Load Configuration"):
                load_config(config_name)
            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            if st.session_state.response:
                st.markdown("<div class='response-section'>", unsafe_allow_html=True)
                st.subheader("Response")
                render_response_viewer(st.session_state.response)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
                render_performance_metrics(st.session_state.timing)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    """
                    <div class="empty-state">
                        <h3>No Response Yet</h3>
                        <p>Configure and send a request to see the response here.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with tabs[1]:
        render_history_viewer()
        
    with tabs[2]:
        render_health_monitor()

if __name__ == "__main__":
    main()
