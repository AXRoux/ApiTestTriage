import streamlit as st
import json
import pandas as pd
from datetime import datetime

def initialize_history():
    """Initialize request history in session state if not present"""
    if 'request_history' not in st.session_state:
        st.session_state.request_history = []

def add_to_history(request_data, response, timing):
    """Add request/response to history"""
    history_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'method': request_data['method'],
        'url': request_data['url'],
        'status_code': response.status_code,
        'response_time': f"{timing['total_time']:.3f}s",
        'request_headers': request_data['headers'],
        'request_body': request_data.get('body', ''),
        'response_headers': dict(response.headers),
        'response_body': response.text
    }
    st.session_state.request_history.insert(0, history_entry)

def export_history():
    """Export history to JSON or CSV"""
    if not st.session_state.request_history:
        st.warning("No history to export")
        return

    export_format = st.selectbox("Export Format", ["JSON", "CSV"])
    
    if st.button("Export"):
        if export_format == "JSON":
            json_str = json.dumps(st.session_state.request_history, indent=2)
            st.download_button(
                "Download JSON",
                json_str,
                "api_history.json",
                "application/json"
            )
        else:
            # Create a simplified DataFrame for CSV export
            df = pd.DataFrame([{
                'timestamp': entry['timestamp'],
                'method': entry['method'],
                'url': entry['url'],
                'status_code': entry['status_code'],
                'response_time': entry['response_time']
            } for entry in st.session_state.request_history])
            
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "api_history.csv",
                "text/csv"
            )

def render_history_viewer():
    """Render the request history viewer component"""
    initialize_history()
    
    st.subheader("Request History")
    
    # Export section
    export_history()
    
    # Display history
    for idx, entry in enumerate(st.session_state.request_history):
        with st.expander(f"[{entry['method']}] {entry['url']} - {entry['status_code']} ({entry['timestamp']})"):
            st.json({
                'Request': {
                    'Headers': entry['request_headers'],
                    'Body': entry['request_body']
                },
                'Response': {
                    'Status': entry['status_code'],
                    'Time': entry['response_time'],
                    'Headers': entry['response_headers'],
                    'Body': entry['response_body']
                }
            })
