import functions_framework
import json

@functions_framework.http
def test_function(request):
    """Minimal test function"""
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    result = {
        'status': 'success',
        'message': 'Test function working',
        'timestamp': '2024-12-14'
    }
    
    return (json.dumps(result), 200, headers)
