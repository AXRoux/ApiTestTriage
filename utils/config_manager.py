import streamlit as st
import json
from typing import Dict

def save_config(name: str) -> None:
    """Save current request configuration"""
    if not name:
        st.error("Please provide a configuration name")
        return

    config = {
        'url': st.session_state.get('url', ''),
        'method': st.session_state.get('method', 'GET'),
        'headers': st.session_state.get('headers', '{}'),
        'body': st.session_state.get('body', '')
    }

    # Store in session state
    if 'saved_configs' not in st.session_state:
        st.session_state.saved_configs = {}
    
    st.session_state.saved_configs[name] = config
    st.success(f"Configuration '{name}' saved successfully!")

def load_config(name: str) -> None:
    """Load saved request configuration"""
    if not name:
        st.error("Please provide a configuration name")
        return

    configs = st.session_state.get('saved_configs', {})
    if name not in configs:
        st.error(f"Configuration '{name}' not found")
        return

    config = configs[name]
    st.session_state.url = config['url']
    st.session_state.method = config['method']
    st.session_state.headers = config['headers']
    st.session_state.body = config['body']
    
    st.success(f"Configuration '{name}' loaded successfully!")
