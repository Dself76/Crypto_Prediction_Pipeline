import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

def data(ticker):
    stock = yf.Ticker(ticker)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    hist_data = stock.history(start=start_date, end=end_date)
    return hist_data

# Fetch the data
user_ticker = input("Enter the stock ticker symbol (e.g., AAPL for Apple or BTC-USD for bitcoin): ").upper()
try:
    df = data(user_ticker)
    print(f"\nHistorical data for {user_ticker}:")
    print(df)

    # Save to CSV
    csv_filename = f"{user_ticker}_1year_history.csv"
    df.to_csv(csv_filename)
    print(f"\nData saved to {csv_filename}")

    # Sort DataFrame by date in descending order
    df = df.sort_index(ascending=False)

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    df_scaled = scaler.fit_transform(df[['Close']])

    # Convert to TensorFlow dataset
    # Assuming you want to create sequences of 14 days for a time series model
    sequence_length = 14
    dataset = tf.data.Dataset.from_tensor_slices(df_scaled)

    # Create sequences
    sequences = dataset.window(sequence_length, shift=1, drop_remainder=True)
    sequences = sequences.flat_map(lambda window: window.batch(sequence_length))

    # Prepare features and labels
    def split_input_target(chunk):
        return chunk[:-1], chunk[-1]

    sequences = sequences.map(split_input_target)

    # Shuffle and batch the dataset
    batch_size = 32
    dataset = sequences.shuffle(buffer_size=1000).batch(batch_size).prefetch(tf.data.experimental.AUTOTUNE)

    print("Data is ready for TensorFlow.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please check if the ticker symbol is correct and try again.")
