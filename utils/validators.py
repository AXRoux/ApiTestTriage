import json
from urllib.parse import urlparse
import re

def validate_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_json(json_str: str) -> bool:
    """Validate JSON string"""
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False

def validate_headers(headers_str: str) -> bool:
    """Validate headers format"""
    try:
        headers = json.loads(headers_str)
        return isinstance(headers, dict)
    except:
        return False
