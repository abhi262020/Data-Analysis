import requests
import pandas as pd

# Replace with your CoinMarketCap API key
api_key = "5a7d8162-584b-48e2-aeab-53de9f5ce32a"

def fetch_crypto_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    parameters = {
        'start': '1',
        'limit': '50',  # Get the top 50 cryptocurrencies
        'convert': 'USD',
    }

    response = requests.get(url, headers=headers, params=parameters)

    # Check status code
    if response.status_code == 200:
        try:
            data = response.json()
            df = pd.DataFrame(data["data"])  # Convert API response to a DataFrame
            return df
        except KeyError:
            print("Error: Key 'data' not found in response. Please check API structure.")
            return None
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return None

# Example usage
crypto_data = fetch_crypto_data()

if crypto_data is not None:
    # Filter for Bitcoin (BTC)
    bitcoin_data = crypto_data[crypto_data['symbol'] == 'BTC']
    if not bitcoin_data.empty:
        print(bitcoin_data)
    else:
        print("Bitcoin data not found.")
else:
    print("Failed to retrieve cryptocurrency data.")
