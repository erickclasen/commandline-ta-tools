#!/usr/bin/python3
import csv
import sys

def find_outliers(asset, file_time_format):
    # Map asset names to CSV column indexes based on your format
    asset_columns = {
        'BTC': 1, 'DOGE': 2, 'ETH': 3, 'FET': 4, 'ICP': 5,
        'LTC': 6, 'QNT': 7, 'RNDR': 8, 'SOL': 9, 'GRT': 10
    }

    # Ensure valid asset and file format inputs
    if asset not in asset_columns:
        print("Error: Invalid asset '{0}'.".format(asset))
        sys.exit(1)

    # Construct filename from file_time_format
    filename = "{}-prices.csv".format(file_time_format)

    # Read the CSV file
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
    except IOError:
        print("Error: File '{0}' not found.".format(filename))
        sys.exit(1)

    # Extract timestamps and asset prices
    timestamps = [row[0] for row in data[1:]]  # assuming first row is headers
    prices = [float(row[asset_columns[asset]]) for row in data[1:]]

    # Calculate price deltas (differences between consecutive prices)
    price_deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

    # Sort deltas to find 2.5th and 97.5th percentiles
    sorted_deltas = sorted(price_deltas)
    lower_bound = sorted_deltas[int(0.025 * len(sorted_deltas))]
    upper_bound = sorted_deltas[int(0.975 * len(sorted_deltas))]

    # Filter outliers
    outliers = [(i, delta) for i, delta in enumerate(price_deltas) if delta < lower_bound or delta > upper_bound]

    if outliers:
        # Print the timestamps, price deltas, and corresponding percent changes for outliers
        print("Outliers in price changes for {0} in {1} file:".format(asset, file_time_format))
        for i, delta in outliers:
            timestamp = timestamps[i + 1]  # Timestamp of current price
            previous_price = prices[i]     # Previous price
            current_price = prices[i + 1]  # Current price

            # Prevent division by zero
            if previous_price == 0:
                print("Warning: Previous price is 0 at timestamp %s. Skipping calculation." % timestamp)
                continue

            percent_change = (delta / previous_price) * 100  # Percent change from previous price

            print("{0}: Price = {1:.5f}, Price Change = {2:.5f}, (Change: {3:.5f}%)".format(
                timestamp, current_price, delta, percent_change))
    else:
        print("No outliers found in price changes for {0} in {1} file.".format(asset, file_time_format))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python find_outliers.py <asset> <file_time_format>")
        sys.exit(1)

    asset = sys.argv[1].upper()  # Asset name (e.g., BTC)
    file_time_format = sys.argv[2].lower()  # Time format (e.g., hourly, four-hour, daily, weekly)

    find_outliers(asset, file_time_format)
