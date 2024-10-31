import requests
import time
from typing import Dict, Any
import json

def send_request(url: str, method: str, headers: Dict[str, str], body: str = None) -> tuple:
    """
    Send HTTP request and return response with timing information
    """
    try:
        start_time = time.time()
        
        # Prepare the request
        headers = headers or {}
        if body:
            try:
                json_body = json.loads(body)
                kwargs = {'json': json_body}
            except json.JSONDecodeError:
                kwargs = {'data': body}
        else:
            kwargs = {}

        # Send the request
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs,
            timeout=30
        )
        
        end_time = time.time()
        
        timing_info = {
            'total_time': end_time - start_time,
            'status_code': response.status_code,
            'size': len(response.content)
        }

        return response, timing_info

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")
