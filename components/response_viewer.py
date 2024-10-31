import streamlit as st
import json

def render_response_viewer(response):
    """Render the response viewer component with enhanced styling"""
    
    # Status code with badge styling
    status_code = response.status_code
    if 200 <= status_code < 300:
        badge_color = "green"
        badge_text = "Success"
    elif 300 <= status_code < 400:
        badge_color = "blue"
        badge_text = "Redirect"
    elif 400 <= status_code < 500:
        badge_color = "orange"
        badge_text = "Client Error"
    else:
        badge_color = "red"
        badge_text = "Server Error"

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div style="background-color: {badge_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 1rem;">
                {status_code}
            </div>
            <div style="color: {badge_color}; font-weight: bold;">
                {badge_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Response headers with collapsible section
    with st.expander("Response Headers", expanded=False):
        headers_dict = dict(response.headers)
        st.json(headers_dict)

    # Response body with proper formatting
    st.subheader("Response Body")
    try:
        # Try to parse as JSON for pretty formatting
        response_json = response.json()
        st.json(response_json)
    except json.JSONDecodeError:
        # If not JSON, show as text with proper formatting
        if response.text.strip():
            if response.headers.get('content-type', '').startswith('text/html'):
                st.code(response.text, language='html')
            elif response.headers.get('content-type', '').startswith('text/xml'):
                st.code(response.text, language='xml')
            else:
                st.code(response.text, language='text')
        else:
            st.info("Empty response body")
