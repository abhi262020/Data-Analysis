import requests
import pandas as pd

# Replace with your CoinMarketCap API key (avoid sharing this publicly)
api_key = "5a7d8162-584b-48e2-aeab-53de9f5ce32a"

def fetch_crypto_data(currency_symbol):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    parameters = {
        'start': '1',
        'limit': '50',
        'convert': 'USD',
        'symbol': currency_symbol,
        'sort': 'market_cap',
        'sort_dir': 'desc',
    }

    response = requests.get(url, headers=headers, params=parameters)

    # Check status code
    if response.status_code == 200:
        try:
            data = response.json()
            df = pd.DataFrame(data["data"])  # Access data using correct key
            return df
        except KeyError:
            print("Error: Key 'data' not found in response. Please check API structure.")
            return None
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return None

# Example usage
bitcoin_data = fetch_crypto_data("BTC")
if bitcoin_data is not None:
    # Process the data
    print(bitcoin_data.head())
else:
    print("Failed to retrieve Bitcoin data.")
