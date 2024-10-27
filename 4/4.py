import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('runkeeper_data.csv')

# Display the first few rows of the dataset
print(data.head())


# Check for missing values
print(data.isnull().sum())

# Fill or remove missing values
data = data.dropna(subset=['Distance (km)', 'Duration (min)', 'Date'])
data['Distance (km)'] = pd.to_numeric(data['Distance (km)'], errors='coerce')
data['Duration (min)'] = pd.to_numeric(data['Duration (min)'], errors='coerce')

# Convert 'Date' to datetime, allowing pandas to infer the format
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

# Check for rows where the date conversion failed
invalid_dates = data[data['Date'].isnull()]
print("Rows with invalid dates:")
print(invalid_dates)

# Verify data types
print(data.info())

# Create a new feature: Pace (min/km)
data['Pace (min/km)'] = data['Duration (min)'] / data['Distance (km)']

# Extract year and month from the date for aggregation
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Group by year and calculate total distance and average pace
yearly_data = data.groupby('Year').agg({'Distance (km)': 'sum', 'Pace (min/km)': 'mean'}).reset_index()

print(yearly_data)

# Barplot: Total Distance Run per Year without hue
plt.figure(figsize=(10, 6))
sns.barplot(x='Year', y='Distance (km)', data=yearly_data, palette='Blues_d')
plt.title('Total Distance Run per Year')
plt.xlabel('Year')
plt.ylabel('Distance (km)') 
plt.show()


plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='Pace (min/km)', data=yearly_data, marker='o', color='green')
plt.title('Average Running Pace Over Time')
plt.xlabel('Year')
plt.ylabel('Pace (min/km)')
plt.show()

# Group by year and month to analyze running trends
monthly_data = data.groupby(['Year', 'Month']).agg({'Distance (km)': 'sum', 'Pace (min/km)': 'mean'}).reset_index()

# Plot monthly distance
plt.figure(figsize=(12, 6))
sns.lineplot(x='Month', y='Distance (km)', hue='Year', data=monthly_data, marker='o')
plt.title('Monthly Distance Run Each Year')
plt.xlabel('Month')
plt.ylabel('Distance (km)')
plt.legend(title='Year', loc='upper right')
plt.show()

# Save the yearly data to a CSV file for a report
yearly_data.to_csv('yearly_runkeeper_report.csv', index=False)

print("Analysis complete and report generated.")

