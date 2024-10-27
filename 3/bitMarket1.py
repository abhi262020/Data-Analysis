import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Replace with your CoinMarketCap API key
api_key = "5a7d8162-584b-48e2-aeab-53de9f5ce32a"

# Function to fetch cryptocurrency data
def fetch_crypto_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=50&convert=USD"
    headers = {"X-CMC_PRO_API_KEY": api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    df = pd.json_normalize(data["data"])
    return df

# Fetch data for cryptocurrencies
crypto_data = fetch_crypto_data()

# Filter data for Bitcoin and Ethereum
crypto_data_filtered = crypto_data[crypto_data["symbol"].isin(["BTC", "ETH"])]

# Extract necessary columns for analysis
crypto_data_filtered = crypto_data_filtered[["symbol", "quote.USD.price", "quote.USD.market_cap", "quote.USD.volume_24h", "last_updated"]]
crypto_data_filtered.rename(columns={"quote.USD.price": "price_usd", "quote.USD.market_cap": "market_cap_usd", "quote.USD.volume_24h": "volume_24h", "last_updated": "date"}, inplace=True)

# Convert 'date' to datetime format
crypto_data_filtered["date"] = pd.to_datetime(crypto_data_filtered["date"])

# Explore the data
print(crypto_data_filtered.describe())

# Correlation analysis on numeric columns
numeric_data = crypto_data_filtered[["price_usd", "market_cap_usd", "volume_24h"]]
correlation = numeric_data.corr()
sns.heatmap(correlation, annot=True)
plt.show()

# Time series analysis (Bitcoin vs Ethereum)
plt.figure(figsize=(12, 6))
btc_data = crypto_data_filtered[crypto_data_filtered["symbol"] == "BTC"]
eth_data = crypto_data_filtered[crypto_data_filtered["symbol"] == "ETH"]
plt.plot(btc_data["date"], btc_data["price_usd"], label="Bitcoin")
plt.plot(eth_data["date"], eth_data["price_usd"], label="Ethereum")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.title("Bitcoin vs. Ethereum Price Over Time")
plt.show()

# Predictive model using K-Fold Cross-Validation
kf = KFold(n_splits=2)  # Using 2 splits because we have only 2 data points

mse_list = []

X = crypto_data_filtered[["market_cap_usd"]]
y = crypto_data_filtered["price_usd"]

for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    mse_list.append(mse)

print("Mean Squared Error for each fold:", mse_list)
