import pandas as pd
import os
import yfinance as yf
import argparse

"""
import_stock_data.py

Downloads historical stock data from Yahoo Finance using a list of symbols in the "Symbols_To_Import.csv" file.

Usage: 
1. Default Date Range (2024-01-01 to 2024-11-28): Run the program without arguments
2. Custom Date Range: Specify the start and end dates using the -s (start) and -e (end) arguments
    Ex: python import_stock_data.py -s 2024-01-01 -e 2024-06-30
"""

def symbol_to_path(symbol, base_dir=os.path.join(".", "data")):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, f"{symbol}.csv")

def get_data_yf_symbol(symbol, start_date, end_date):
    """Fetch stock data (adjusted close) for the given symbol from Yahoo Finance."""
    df = yf.download(
        symbol,
        interval="1d",
        start=start_date,
        end=end_date
    )
    return df

if __name__ == '__main__':
    # Load symbols from Symbols_To_Import.csv
    symbols_df = pd.read_csv('Symbols_To_Import.csv')
    symbols = symbols_df['Symbol'].tolist()

    # Set default date range
    date_start = '2024-01-01'
    date_end = '2024-11-28'

    # Parse arguments for start and end dates if provided
    parser = argparse.ArgumentParser(
        prog='GetYFData',
        description='Download historical stock data from Yahoo Finance'
    )

    parser.add_argument('-s', action="store", dest="date_start", default=date_start)
    parser.add_argument('-e', action="store", dest="date_end", default=date_end)
    args = parser.parse_args()

    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    # Loop over all symbols
    for symbol in symbols:
        print(f"Downloading data for {symbol}...")
        df = get_data_yf_symbol(symbol, args.date_start, args.date_end)
        if not df.empty:
            df.to_csv(symbol_to_path(symbol))
            print(f"Data for {symbol} saved.")
        else:
            print(f"No data found for {symbol}.")