import streamlit as st
import json

def render_response_viewer(response):
    """Render the response viewer component"""
    
    # Status code with color
    status_color = "green" if 200 <= response.status_code < 300 else "red"
    st.markdown(f"Status Code: <span style='color:{status_color}'>{response.status_code}</span>", 
               unsafe_allow_html=True)

    # Response headers
    st.subheader("Response Headers")
    st.json(dict(response.headers))

    # Response body
    st.subheader("Response Body")
    try:
        # Try to parse as JSON
        response_json = response.json()
        st.json(response_json)
    except json.JSONDecodeError:
        # If not JSON, show as text
        st.text(response.text)
