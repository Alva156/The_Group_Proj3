from flask import Flask, render_template, jsonify, request
import requests
from dotenv import load_dotenv
import os
import ipaddress

# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve the ipinfo.io API key from environment variables
IPINFO_API_KEY = os.getenv("IPINFO_API_KEY")

# Route to display the main webpage
@app.route('/')
def index():
    return render_template('index.html', api_key=IPINFO_API_KEY)

# Route to display the about webpage
@app.route('/about')
def about():
    return render_template('about.html')

# API route to fetch IP information
@app.route('/fetch_ip_info', methods=['GET'])
def fetch_ip_info():
    # Get the type of IP (default is ipv4)
    ip_type = request.args.get('type', 'ipv4').lower()
    
    # Use the general URL that works for both IPv4 and IPv6
    url = f"https://ipinfo.io/json?token={IPINFO_API_KEY}"

    try:
        # Fetch IP information from ipinfo.io
        response = requests.get(url)

        if response.status_code != 200:
            return jsonify({"error": f"Failed to fetch IP info. Status code: {response.status_code}"}), 500

        data = response.json()
        ip = data.get('ip', "Not available")
        
        # Determine the IP type (ipv4 or ipv6)
        ip_type = 'ipv6' if ipaddress.ip_address(ip).version == 6 else 'ipv4'

        ip_info = {
            "ip": ip,
            "hostname": data.get('hostname', "Not available"),
            "city": data.get('city', "Not available"),
            "region": data.get('region', "Not available"),
            "country": data.get('country', "Not available"),
            "loc": data.get('loc', "Not available"),
            "org": data.get('org', "Not available"),
            "postal": data.get('postal', "Not available"),
            "country_code": data.get('country', "Not available"),
            "ip_type": ip_type  # Add the detected IP type to the response
        }

        return jsonify({"ip_info": ip_info})

    except requests.exceptions.RequestException:
        return jsonify({"error": "Network error occurred while fetching IP information"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
