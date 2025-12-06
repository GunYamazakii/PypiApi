import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Base configuration from the provided content
BASE_URL = 'https://web.blueitx.xyz/api/check_card.php'

# WARNING: The PHPSESSID cookie is likely session-specific and will expire.
# For a real-world application, you would need a proper authentication mechanism
# or a valid, long-lived session token/API key for the external service.
COOKIES = {
    'PHPSESSID': 'r9t02lj6nbr39gqe9ap21essue',
}

HEADERS = {
    'authority': 'web.blueitx.xyz',
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://web.blueitx.xyz',
    'referer': 'https://web.blueitx.xyz/checker.php',
    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
}

@app.route('/gates/<gateway_name>/key/<api_key>/cc/<cc_info>', methods=['GET'])
def check_card(gateway_name, api_key, cc_info):
    """
    Handles the gateway check request.
    
    Example URL: /gates/stripe_auth/key/diwazz/cc/5273350015300245|01|28|772
    For auto_shopify, include a 'site' query parameter:
    Example URL: /gates/auto_shopify/key/diwazz/cc/5273350015300245|01|28|772?site=https://example.com
    """
    
    # The gateway name from the URL is used as the 'gateway' parameter in the payload
    # The 'api_key' is included in the response for tracking but not used in the external request
    
    json_data = {
        'action': 'check_card',
        'card': cc_info,
        'gateway': gateway_name,
    }
    
    # Handle the 'auto_shopify' case which requires an additional 'site' parameter
    if gateway_name == 'auto_shopify':
        site = request.args.get('site')
        if not site:
            return jsonify({
                'error': 'Missing site parameter',
                'message': 'The "auto_shopify" gateway requires a "site" query parameter (e.g., ?site=https://example.com)'
            }), 400
        json_data['site'] = site
    
    try:
        # Make the POST request to the external API
        response = requests.post(
            BASE_URL, 
            cookies=COOKIES, 
            headers=HEADERS, 
            json=json_data,
            timeout=10 # Set a timeout for the external request
        )
        
        # Check for successful response from the external API
        response.raise_for_status()
        
        # Return the JSON response from the external API
        return jsonify({
            'status': 'success',
            'gateway_response': response.json(),
            'requested_gateway': gateway_name,
            'requested_api_key': api_key,
            'requested_cc_info': cc_info
        })

    except requests.exceptions.RequestException as e:
        # Handle request errors (e.g., connection, timeout, HTTP errors)
        return jsonify({
            'status': 'error',
            'message': f'Request to external API failed: {e}',
            'requested_gateway': gateway_name,
            'requested_api_key': api_key,
            'requested_cc_info': cc_info
        }), 500
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({
            'status': 'error',
            'message': f'An unexpected error occurred: {e}',
            'requested_gateway': gateway_name,
            'requested_api_key': api_key,
            'requested_cc_info': cc_info
        }), 500

if __name__ == '__main__':
    # For local testing, you can run: python app.py
    # app.run(debug=True)
    # Note: Running on a public host requires a different setup, 
    # but for the sandbox environment, we will just provide the file.
    pass
