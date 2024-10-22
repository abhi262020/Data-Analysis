import pandas as pd
import matplotlib.pyplot as plt

# Load the data
datapath= 'listings.csv'
data = pd.read_csv(datapath)

# Display the first few rows of the dataset
print(data.head())

# Data Cleaning
# Drop rows with missing values
data = data.dropna()

# Convert price to numeric
data['price'] = data['price'].replace('[\$,]', '', regex=True).astype(float)

# Exploratory Data Analysis
# Summary statistics
print(data.describe())

# Visualization
# Distribution of prices
plt.figure(figsize=(10, 6))
plt.hist(data['price'], bins=50, color='blue', edgecolor='black')
plt.title('Distribution of Airbnb Prices in NYC')
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.show()

# Average price by neighborhood
neighborhood_prices = data.groupby('neighbourhood')['price'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 8))
neighborhood_prices.plot(kind='bar', color='green')
plt.title('Average Airbnb Price by Neighborhood in NYC')
plt.xlabel('Neighborhood')
plt.ylabel('Average Price ($)')
plt.show()
