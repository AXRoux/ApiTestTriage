import streamlit as st
from utils.request_handler import send_request
from utils.validators import validate_url, validate_json, validate_headers

def render_request_form():
    """Render the request configuration form"""
    
    # URL input
    url = st.text_input("URL", key="url")
    
    # Method selection
    method = st.selectbox(
        "Method",
        ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        key="method"
    )
    
    # Headers input
    headers_str = st.text_area(
        "Headers (JSON format)",
        value="{}",
        key="headers",
        help="Enter headers in JSON format"
    )
    
    # Request body
    if method in ["POST", "PUT", "PATCH"]:
        body = st.text_area(
            "Request Body",
            key="body",
            help="Enter request body (JSON format for application/json)"
        )
    else:
        body = None

    if st.button("Send Request"):
        # Validate inputs
        if not validate_url(url):
            st.error("Invalid URL format")
            return
        
        if not validate_headers(headers_str):
            st.error("Invalid headers format")
            return
        
        if body and not validate_json(body):
            st.error("Invalid JSON in request body")
            return

        try:
            headers = eval(headers_str)
            response, timing = send_request(url, method, headers, body)
            
            # Store response and timing in session state
            st.session_state.response = response
            st.session_state.timing = timing
            
        except Exception as e:
            st.error(f"Request failed: {str(e)}")
