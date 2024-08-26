import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

class SMA:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.df = None
        self.sma_results = {}

    def fetch_data(self):
        stock = yf.Ticker(self.ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        self.df = stock.history(start=start_date, end=end_date)
        return self.df

    def calculate_sma(self, days=14, periods=3):
        if self.df is None:
            raise ValueError("Data not fetched. Call fetch_data() first.")
        
        self.df = self.df.sort_index(ascending=False)
        
        for i in range(periods):
            start_idx = i * days
            end_idx = start_idx + days
            
            period_closes = self.df['Close'].iloc[start_idx:end_idx]
            sum_of_closes = period_closes.sum()
            average = sum_of_closes / days
            
            period_label = f'Days {start_idx+1} to {end_idx}'
            start_date = self.df.index[end_idx - 1].strftime('%Y-%m-%d')
            end_date = self.df.index[start_idx].strftime('%Y-%m-%d')
            
            self.sma_results[period_label] = {
                'date_range': f'{start_date} to {end_date}',
                'sum': sum_of_closes,
                'average': average
            }

    def display_results(self):
        for period, data in self.sma_results.items():
            print(f"{period} ({data['date_range']}):")
            print(f"  Sum: {data['sum']:.2f}")
            print(f"  Average: {data['average']:.2f}")
            print()

    def save_to_csv(self):
        csv_filename = f"{self.ticker}_1year_history.csv"
        self.df.to_csv(csv_filename)
        print(f"Data saved to {csv_filename}")

# Usage example:
if __name__ == "__main__":
    user_ticker = input("Enter the stock ticker symbol (e.g., AAPL for Apple or BTC-USD for bitcoin): ")
    
    try:
        sma = SMA(user_ticker)
        sma.fetch_data()
        sma.calculate_sma(days=14, periods=3)
        sma.display_results()
        sma.save_to_csv()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check if the ticker symbol is correct and try again.")
