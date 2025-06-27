from flask import Flask, request, jsonify
from weather_service import get_weather

app = Flask(__name__)


@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    pincode = request.args.get('pincode')

    if city:
        result = get_weather("city", city)
    elif pincode:
        result = get_weather("pincode", pincode)
    else:
        return jsonify({"error": "Please provide either city or pincode"}), 400

    if "error" in result:
        return jsonify(result), 500

    return jsonify(result)


@app.route("/")
def welcome():
    return "<h1>Welcome to my Weather App.</h1>"


if __name__ == '__main__':
   app.run(debug=True)