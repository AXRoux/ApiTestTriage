import streamlit as st
import base64

def render_auth_section():
    """Render authentication configuration section"""
    auth_type = st.selectbox(
        "Authentication Type",
        ["None", "Basic Auth", "Bearer Token", "OAuth2"],
        key="auth_type"
    )

    auth_headers = {}
    
    if auth_type == "Basic Auth":
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", key="auth_username")
        with col2:
            password = st.text_input("Password", key="auth_password", type="password")
            
        if username and password:
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            auth_headers["Authorization"] = f"Basic {credentials}"
            
    elif auth_type == "Bearer Token":
        token = st.text_input("Bearer Token", key="auth_token")
        if token:
            auth_headers["Authorization"] = f"Bearer {token}"
            
    elif auth_type == "OAuth2":
        token_url = st.text_input("Token URL", key="oauth_token_url")
        client_id = st.text_input("Client ID", key="oauth_client_id")
        client_secret = st.text_input("Client Secret", key="oauth_client_secret", type="password")
        scope = st.text_input("Scope (optional)", key="oauth_scope")
        
        if token_url and client_id and client_secret:
            try:
                import requests
                data = {
                    'grant_type': 'client_credentials',
                    'client_id': client_id,
                    'client_secret': client_secret
                }
                if scope:
                    data['scope'] = scope
                    
                response = requests.post(token_url, data=data)
                if response.status_code == 200:
                    token_data = response.json()
                    if 'access_token' in token_data:
                        auth_headers["Authorization"] = f"Bearer {token_data['access_token']}"
                        st.success("OAuth2 token obtained successfully!")
                    else:
                        st.error("Access token not found in response")
                else:
                    st.error(f"Failed to obtain OAuth2 token: {response.text}")
            except Exception as e:
                st.error(f"OAuth2 error: {str(e)}")
                
    return auth_headers
