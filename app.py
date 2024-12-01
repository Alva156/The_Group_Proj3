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
    ip_type = request.args.get('type', '').lower()  # Get the IP type from the request (IPv4 or IPv6)
    url = f"https://ipinfo.io/json?token={IPINFO_API_KEY}"

    try:
        # Fetch the IP info from ipinfo.io
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch IP information."}), 500

        data = response.json()
        ip = data.get("ip", "Not available")

        # Validate the IP type
        try:
            ip_obj = ipaddress.ip_address(ip)
            if (ip_type == "ipv4" and ip_obj.version != 4) or (ip_type == "ipv6" and ip_obj.version != 6):
                return jsonify({
                
                    "ip": "Not available",
                     "hostname": "Not available",
                    "city": "Not available",
                    "region": "Not available",
                    "country": "Not available",
                    "loc": "Not available", 
                    "org": "Not available",
                    "postal": "Not available",
                   
                }), 200
        except ValueError:
            return jsonify({"error": "Invalid IP address received from the API."}), 500

        # Return details if the IP matches the selected type
        return jsonify({
            "ip": ip,
            "hostname": data.get("hostname", "Not available"),
            "city": data.get("city", "Not available"),
            "region": data.get("region", "Not available"),
            "country": data.get("country", "Not available"),
            "loc": data.get("loc", "Not available"),
            "org": data.get("org", "Not available"),
            "postal": data.get("postal", "Not available")
        })
    except requests.RequestException:
        return jsonify({"error": "Network error occurred while fetching IP information."}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)