from flask import Flask, render_template, jsonify
import requests


 # Flask is used as a Python web framework for this project to facilitate the development of web applications and APIs with simplicity and flexibility.
app = Flask(__name__)

# Route to display the main webpage
@app.route('/')
def index():
    return render_template('index.html')
# Route to display the about webpage
@app.route('/about')
def about():
    return render_template('about.html')

# API route to fetch IP information
@app.route('/fetch_ip_info', methods=['GET'])
def fetch_ip_info():
    try:
        response = requests.get('https://ipapi.co/json/')
        data = response.json()

        # Retrieve IPv4 and IPv6 addresses
        ipv4 = data.get('ip', "Not available")
        ipv6 = data.get('ipv6', "Not available")
        country = data.get('country_name', "Not available")
        region = data.get('region', "Not available")
        city = data.get('city', "Not available")
        isp = data.get('org', "Not available")
        latitude = data.get('latitude', "Not available")
        longitude = data.get('longitude', "Not available")
        asn = data.get('asn', "Not available")
        country_code = data.get('country_code', "Not available")

        ip_info = {
            "ipv4": ipv4,
            "ipv6": ipv6,
            "country": country,
            "region": region,
            "city": city,
            "isp": isp,
            "latitude": latitude,
            "longitude": longitude,
            "asn": asn,
            "country_code": country_code
        }

        return jsonify(ip_info)

    except Exception as e:
        return jsonify({"error": "Error fetching IP information"}), 500

if __name__ == '__main__':
    app.run(debug=True)
