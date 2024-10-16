import pandas as pd
import sys

def find_outliers(asset, file_time_format):
    # Map asset names to CSV column indexes based on your format
    asset_columns = {
        'BTC': 1, 'DOGE': 2, 'ETH': 3, 'FET': 4, 'ICP': 5,
        'LTC': 6, 'QNT': 7, 'SOL': 8, 'GRT': 9
    }
    
    # Ensure valid asset and file format inputs
    if asset not in asset_columns:
        print(f"Error: Invalid asset '{asset}'.")
        sys.exit(1)
    
    # Construct filename from file_time_format
    filename = f"{file_time_format}-prices.csv"
    
    # Read the CSV file
    try:
        data = pd.read_csv(filename, header=None)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    
    # Extract the column corresponding to the asset
    asset_col_index = asset_columns[asset]
    prices = data.iloc[:, asset_col_index]
    
    # Calculate the price deltas (difference between consecutive prices)
    price_deltas = prices.diff().dropna()  # drop the first NaN value caused by diff()
    
    # Calculate the 2.5th and 97.5th percentiles of price deltas
    lower_bound = price_deltas.quantile(0.025)
    upper_bound = price_deltas.quantile(0.975)
    
    # Filter outliers: those that are below the lower bound or above the upper bound
    outliers = price_deltas[(price_deltas < lower_bound) | (price_deltas > upper_bound)]
    
    if not outliers.empty:
        # Print the timestamps, price deltas, and corresponding percent changes for outliers
        print(f"Outliers in price changes for {asset} in {file_time_format} file:")
        for index, delta in outliers.items():
            timestamp = data.iloc[index, 0]  # Get the timestamp from the first column
            previous_price = prices.iloc[index - 1]  # Get the previous price
            current_price = prices.iloc[index]  # Get the current price
            percent_change = (delta / previous_price) * 100  # Percent change from previous price
            # Print the output with rounded values
            print(f"{timestamp}: Price = {current_price:.5f}, Price Change = {delta:.5f} (Change: {percent_change:.2f}%)")
    else:
        print(f"No outliers found in price changes for {asset} in {file_time_format} file.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python find_outliers.py <asset> <file_time_format>")
        sys.exit(1)
    
    asset = sys.argv[1].upper()  # Asset name (e.g., BTC)
    file_time_format = sys.argv[2].lower()  # Time format (e.g., hourly, four-hour, daily, weekly)
    
    find_outliers(asset, file_time_format)

