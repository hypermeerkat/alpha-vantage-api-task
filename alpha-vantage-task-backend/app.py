# Import necessary libraries and modules
from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta
from utils import calculate_daily_average, print_api_data
from dotenv import load_dotenv
import os
from flask_caching import Cache
from flask.logging import create_logger
import json

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and configure caching
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
app_logger = create_logger(app)

# Define available resources and their corresponding intervals
RESOURCE_INTERVALS = {
    'WTI': ['daily', 'weekly', 'monthly'],
    'BRENT': ['daily', 'weekly', 'monthly'],
    'NATURAL_GAS': ['daily', 'weekly', 'monthly'],
    'COPPER': ['monthly', 'quarterly', 'annual'],
    'ALUMINUM': ['monthly', 'quarterly', 'annual'],
    'WHEAT': ['monthly', 'quarterly', 'annual'],
    'CORN': ['monthly', 'quarterly', 'annual'],
    'COTTON': ['monthly', 'quarterly', 'annual'],
    'SUGAR': ['monthly', 'quarterly', 'annual'],
    'COFFEE': ['monthly', 'quarterly', 'annual'],
}

# Define the main API endpoint for calculating daily averages
@app.route('/daily_average', methods=['GET'])
def daily_average():
    try:
        # Extract query parameters from the request
        function = request.args.get('function', 'WTI')
        interval = request.args.get('interval', 'daily')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')

        # Log the received request details
        app_logger.info(f"Received request: function={function}, interval={interval}, start_date={start_date}, end_date={end_date}")

        # Validate the input parameters
        if function not in RESOURCE_INTERVALS:
            return jsonify({"error": f"Invalid resource: {function}"}), 400

        if interval not in RESOURCE_INTERVALS[function]:
            return jsonify({"error": f"Invalid interval '{interval}' for resource '{function}'. Valid intervals are: {', '.join(RESOURCE_INTERVALS[function])}"}), 400

        if not start_date or not end_date:
            return jsonify({"error": f"Start date and end date are required. Received: start_date={start_date}, end_date={end_date}"}), 400

        # Check if data is available in cache
        cache_key = f"{function}_{interval}"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            # If not in cache, fetch data from Alpha Vantage API
            url = f"https://www.alphavantage.co/query?function={function}&interval={interval}&apikey={api_key}"
            app_logger.info(f"Fetching data from Alpha Vantage API: {url}")
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Handle API errors and limits
            if 'Information' in data:
                app_logger.warning(f"API limit reached: {data['Information']}")
                return jsonify({"error": f"API limit reached or invalid key. Message: {data['Information']}"}), 429

            if 'Error Message' in data:
                app_logger.error(f"Alpha Vantage API error: {data['Error Message']}")
                return jsonify({"error": data['Error Message']}), 400

            app_logger.info("Successfully fetched data from Alpha Vantage API")
            cache.set(cache_key, json.dumps(data))
        else:
            # Use cached data if available
            app_logger.info("Using cached data")
            data = json.loads(cached_data)

        # Calculate the daily average for the specified date range
        average = calculate_daily_average(data, start_date, end_date)
        
        # Handle case where no valid data is available for the date range
        if average is None:
            app_logger.warning(f"No valid data available for the specified date range: {start_date} to {end_date}")
            return jsonify({
                "error": f"No valid data available for the specified date range: {start_date} to {end_date}. "
                        f"Available date range: {data['data'][-1]['date']} to {data['data'][0]['date']}"
            }), 400

        # Prepare the daily prices data for the response
        daily_prices = [
            {"date": entry['date'], "price": float(entry['value'])}
            for entry in data['data']
            if start_date <= entry['date'] <= end_date
        ]

        # Prepare the final result
        result = {
            "function": function,
            "interval": interval,
            "start_date": start_date,
            "end_date": end_date,
            "average_price": round(average, 2),
            "currency": "USD per unit",
            "daily_prices": daily_prices
        }
        app_logger.info(f"Returning result: {result}")
        return jsonify(result)
    except Exception as e:
        # Log any unexpected errors
        app_logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred. Please check the server logs for more information."}), 500

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)