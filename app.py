import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_URL = 'https://web.blueitx.xyz/api/check_card.php'

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
    Example:
    /gates/stripe_auth/key/diwazz/cc/5273350015300245|01|28|772
    /gates/auto_shopify/key/diwazz/cc/5273350015300245|01|28|772?site=https://example.com
    """

    json_data = {
        'action': 'check_card',
        'card': cc_info,
        'gateway': gateway_name,
    }

    if gateway_name == 'auto_shopify':
        site = request.args.get('site')
        if not site:
            return jsonify({
                'error': 'Missing site parameter',
                'message': 'The "auto_shopify" gateway requires a "site" query parameter (e.g., ?site=https://example.com)'
            }), 400
        json_data['site'] = site

    try:
        response = requests.post(
            BASE_URL,
            cookies=COOKIES,
            headers=HEADERS,
            json=json_data,
            timeout=10
        )
        response.raise_for_status()

        return jsonify({
            'status': 'success',
            'gateway_response': response.json(),
            'requested_gateway': gateway_name,
            'requested_api_key': api_key,
            'requested_cc_info': cc_info
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            'status': 'error',
            'message': f'Request to external API failed: {e}',
            'requested_gateway': gateway_name,
            'requested_api_key': api_key,
            'requested_cc_info': cc_info
        }), 500

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An unexpected error occurred: {e}',
            'requested_gateway': gateway_name,
            'requested_api_key': api_key,
            'requested_cc_info': cc_info
        }), 500


# No app.run() here – gunicorn will import "app:app"
if __name__ == '__main__':
    # Optional for local dev only:
    # app.run(host='0.0.0.0', port=5000, debug=True)
    pass
