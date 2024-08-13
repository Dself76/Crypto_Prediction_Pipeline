import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Bollinger:
    def __init__(self):
        self.df = None
        self.user_ticker = None

    def data(self, ticker):
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        hist_data = stock.history(start=start_date, end=end_date)
        return hist_data

    def fetch_data(self):
        self.user_ticker = input("Enter the stock ticker symbol (e.g., AAPL for Apple or BTC-USD for bitcoin): ").upper()
        try:
            self.df = self.data(self.user_ticker)
            print(f"\nHistorical data for {self.user_ticker}:")
            print(self.df)
            csv_filename = f"{self.user_ticker}_1year_history.csv"
            self.df.to_csv(csv_filename)
            print(f"\nData saved to {csv_filename}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please check if the ticker symbol is correct and try again.")

    def calculate_sma(self):
        last_14_closes = self.df['Close'].tail(14)
        last_15_to_28_closes = self.df['Close'].iloc[-28:-14]
        last_29_to_43_closes = self.df['Close'].iloc[-43:-28]

        sum_of_last_14_closes = last_14_closes.sum()
        sum_of_last_15_to_28_closes = last_15_to_28_closes.sum()
        sum_of_last_29_to_43_closes = last_29_to_43_closes.sum()

        print("Sum of last 14 closing prices Most CURRENT:", sum_of_last_14_closes)
        print("Sum of last 15 to 28 closing prices:", sum_of_last_15_to_28_closes)
        print("Sum of last 29 to 43 closing prices:", sum_of_last_29_to_43_closes)

        sma_14day = sum_of_last_14_closes / 14
        sma_28day = sum_of_last_15_to_28_closes / 14
        sma_43day = sum_of_last_29_to_43_closes / 14
        print(sma_14day)
        print(sma_28day)
        print(sma_43day)

    def calculate_bollinger_bands(self):
        self.df['SMA20'] = self.df['Close'].rolling(window=20).mean()
        self.df['20_day_SD'] = self.df['Close'].rolling(window=20).std()
        self.df['Upper_Band'] = self.df['SMA20'] + (self.df['20_day_SD'] * 2)
        self.df['Lower_Band'] = self.df['SMA20'] - (self.df['20_day_SD'] * 2)

        print(self.df[['Close', 'SMA20', 'Upper_Band', 'Lower_Band']].tail(20))

    def plot_bollinger_bands(self):
        plt.figure(figsize=(12,6))
        plt.plot(self.df.index, self.df['Close'], label='Close Price')
        plt.plot(self.df.index, self.df['SMA20'], label='20-day SMA')
        plt.plot(self.df.index, self.df['Upper_Band'], label='Upper Band')
        plt.plot(self.df.index, self.df['Lower_Band'], label='Lower Band')
        plt.title(f'Bollinger Bands for {self.user_ticker}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

    def run(self):
        self.fetch_data()
        if self.df is not None:
            self.calculate_sma()
            self.calculate_bollinger_bands()
            self.plot_bollinger_bands()

# Usage
bollinger = Bollinger()
bollinger.run()