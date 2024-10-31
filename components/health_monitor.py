import streamlit as st
from datetime import datetime, timedelta
import time
import asyncio
import aiohttp
import json
from typing import Dict, List

class HealthMonitor:
    def __init__(self):
        if 'monitored_endpoints' not in st.session_state:
            st.session_state.monitored_endpoints = {}
        if 'health_checks' not in st.session_state:
            st.session_state.health_checks = {}

    async def check_endpoint(self, endpoint_id: str, url: str, method: str, headers: Dict, 
                           expected_status: int, timeout: int) -> Dict:
        """Perform health check for a single endpoint"""
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, headers=headers, timeout=timeout) as response:
                    end_time = time.time()
                    response_time = end_time - start_time
                    is_healthy = response.status == expected_status
                    
                    return {
                        'timestamp': datetime.now().isoformat(),
                        'status': 'healthy' if is_healthy else 'unhealthy',
                        'response_time': response_time,
                        'status_code': response.status,
                        'message': 'OK' if is_healthy else f'Expected {expected_status}, got {response.status}'
                    }
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'unhealthy',
                'response_time': time.time() - start_time,
                'status_code': None,
                'message': str(e)
            }

def render_health_monitor():
    """Render the health monitoring interface"""
    monitor = HealthMonitor()
    
    st.header("API Health Monitoring")
    
    # Add new endpoint form
    with st.expander("Add New Endpoint"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Endpoint Name", key="health_name")
            url = st.text_input("URL", key="health_url")
            method = st.selectbox("Method", ["GET", "POST", "HEAD"], key="health_method")
        
        with col2:
            expected_status = st.number_input("Expected Status Code", min_value=100, max_value=599, value=200, key="health_status")
            interval = st.number_input("Check Interval (seconds)", min_value=30, value=60, key="health_interval")
            timeout = st.number_input("Timeout (seconds)", min_value=1, value=10, key="health_timeout")
        
        headers = st.text_area("Headers (JSON)", "{}", key="health_headers")
        
        if st.button("Add Endpoint"):
            try:
                headers_dict = json.loads(headers)
                endpoint_id = f"{name}_{int(time.time())}"
                st.session_state.monitored_endpoints[endpoint_id] = {
                    'name': name,
                    'url': url,
                    'method': method,
                    'headers': headers_dict,
                    'expected_status': expected_status,
                    'interval': interval,
                    'timeout': timeout,
                    'last_check': None
                }
                st.success(f"Added endpoint: {name}")
            except json.JSONDecodeError:
                st.error("Invalid JSON in headers")
    
    # Display monitored endpoints
    if st.session_state.monitored_endpoints:
        for endpoint_id, endpoint in st.session_state.monitored_endpoints.items():
            with st.expander(f"📊 {endpoint['name']} - {endpoint['url']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                # Check if it's time to perform a health check
                current_time = datetime.now()
                last_check = endpoint.get('last_check')
                should_check = (
                    last_check is None or 
                    (current_time - datetime.fromisoformat(last_check)).total_seconds() >= endpoint['interval']
                )
                
                if should_check:
                    # Perform health check
                    check_result = asyncio.run(monitor.check_endpoint(
                        endpoint_id,
                        endpoint['url'],
                        endpoint['method'],
                        endpoint['headers'],
                        endpoint['expected_status'],
                        endpoint['timeout']
                    ))
                    
                    # Update last check time
                    st.session_state.monitored_endpoints[endpoint_id]['last_check'] = check_result['timestamp']
                    
                    # Store check result
                    if endpoint_id not in st.session_state.health_checks:
                        st.session_state.health_checks[endpoint_id] = []
                    st.session_state.health_checks[endpoint_id].append(check_result)
                    
                    # Keep only last 100 checks
                    st.session_state.health_checks[endpoint_id] = st.session_state.health_checks[endpoint_id][-100:]
                
                # Display latest status
                if endpoint_id in st.session_state.health_checks and st.session_state.health_checks[endpoint_id]:
                    latest = st.session_state.health_checks[endpoint_id][-1]
                    status_color = "green" if latest['status'] == 'healthy' else "red"
                    
                    with col1:
                        st.metric("Status", latest['status'].upper(), delta_color=status_color)
                    with col2:
                        st.metric("Response Time", f"{latest['response_time']:.3f}s")
                    with col3:
                        st.metric("Status Code", str(latest['status_code']))
                    
                    st.text(f"Last Check: {latest['timestamp']}")
                    st.text(f"Message: {latest['message']}")
                
                # Remove endpoint button
                if st.button("Remove Endpoint", key=f"remove_{endpoint_id}"):
                    del st.session_state.monitored_endpoints[endpoint_id]
                    if endpoint_id in st.session_state.health_checks:
                        del st.session_state.health_checks[endpoint_id]
                    st.experimental_rerun()
    else:
        st.info("No endpoints are being monitored. Add an endpoint to start monitoring.")
