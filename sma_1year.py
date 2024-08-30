import pandas as pd
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
def data(ticker):
    stock = yf.Ticker(ticker)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    hist_data = stock.history(start=start_date, end=end_date)
    
    return hist_data
user_ticker = input("Enter the stock ticker symbol (e.g., AAPL for Apple or BTC-USD for bitcoin): ").upper()
print(data)
try:
    # Fetch the data
    df = data(user_ticker)
    
    # Display the data
    print(f"\nHistorical data for {user_ticker}:")
    print(df)
    
    # Optional: Save to CSV
    csv_filename = f"{user_ticker}_1year_history.csv"
    df.to_csv(csv_filename)
    print(f"\nData saved to {csv_filename}")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check if the ticker symbol is correct and try again.")

   # Make sure the DataFrame is sorted in descending order by date (most recent first, this will be my problem)
df = df.sort_index(ascending=False)

# Initialize a dictionary to store the results
sma_results = {}

# Calculate SMA for each 14-day period, starting from the most recent
for i in range(0, len(df) - 14 + 1, 14):
    # Get the closing prices for the current 14-day window
    current_closes = df['Close'].iloc[i:i+14]
    # Calculate the sum of these closing prices
    sum_of_closes = current_closes.sum()
    # Calculate the end date of this period
    end_date = df.index[i].strftime('%Y-%m-%d')
    # Calculate the start date of this period
    start_date = df.index[min(i+13, len(df)-1)].strftime('%Y-%m-%d')
    # Store the result with a date range representing the period
    sma_results[f'{start_date} to {end_date}'] = sum_of_closes

# Print all the SMA sums
for period, sum_value in sma_results.items():
    print(f"Sum of closing prices for {period}: {sum_value}")

#stopping here clean data for tensor flow but remind self to switch to classes,OOP will be better 